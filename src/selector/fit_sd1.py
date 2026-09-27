"""Fit SD-1. Does not rescore primitives or edit a freeze."""

import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge

ROOT = Path(__file__).resolve().parents[2]
FP = ROOT / "data" / "fingerprint" / "fingerprint.json"
P0 = ROOT / "results" / "raw" / "performance_p0_p1.json"
DG = ROOT / "results" / "raw" / "performance_dg.json"
OUT = ROOT / "results" / "raw" / "selector_sd1.json"

COORDS = ["Q", "C_train", "C_infer", "C_api", "L_p50", "L_p95", "V"]
CLIP_UNIT = {"Q", "V"}
CLIP_NONNEG = {"C_train", "C_infer", "L_p50", "L_p95"}
ORDER = ["R", "C", "D", "G"]
FEATS = [
    "log10_n",
    "log10_k",
    "entropy",
    "log10_max_min",
    "log10_min_per_class",
    "log10_median_per_class",
    "log10_median_tokens",
    "log10_p95_tokens",
    "mean_cosine",
    "min_cosine",
    "paired",
]

HOLDOUTS = [
    ("Intent", ["banking77", "clinc_oos_plus"]),
    ("Verification", ["pubmedqa_fold0", "vitaminc"]),
    ("Moderation", ["civil_comments_binary"]),
    ("Security", ["sms_spam"]),
    ("Business / legal", ["ledgar"]),
    ("E-commerce", ["esci_en_us_task2"]),
]


def primitive(name):
    if name in ("Cfull", "C100k"):
        return "C"
    return name


def load():
    fp = json.loads(FP.read_text(encoding="utf-8"))
    tasks = {}
    for row in fp["candidates"]:
        imb = row["imbalance"]
        length = row["length"]
        sim = row["label_similarity"]
        rel = row["structural"]["relation_code"]
        x = np.array(
            [
                np.log10(imb["n"]),
                np.log10(imb["k"]),
                imb["normalized_entropy"],
                np.log10(imb["max_min_ratio"]),
                np.log10(imb["min_per_class"]),
                np.log10(imb["median_per_class"]),
                np.log10(length["median_tokens"]),
                np.log10(length["p95_tokens"]),
                sim["mean_pairwise_cosine"],
                sim["min_pairwise_cosine"],
                1.0 if rel == "paired_text" else 0.0,
            ],
            dtype=float,
        )
        tasks[row["candidate"]] = {
            "x": x,
            "selector_training": bool(row["structural"]["selector_training"]),
            "pairs": {},
        }
    for blob in (P0, DG):
        for row in json.loads(blob.read_text(encoding="utf-8")):
            p = primitive(row["primitive"])
            y = {
                "Q": row["Q_macro_f1"],
                "C_train": row["C_train_seconds"],
                "C_infer": row["C_infer_seconds"],
                "C_api": row["C_api_usd"],
                "L_p50": row["L_p50_ms"],
                "L_p95": row["L_p95_ms"],
                "V": row["invalid_outputs"] / row["n_eval"],
            }
            tasks[row["task"]]["pairs"][p] = y
    return tasks


def scaler(tasks, names):
    mat = np.vstack([tasks[t]["x"] for t in names])
    mu = mat.mean(axis=0)
    sd = mat.std(axis=0)
    return mu, sd


def standardize(x, mu, sd):
    z = np.zeros_like(x)
    ok = sd > 0
    z[ok] = (x[ok] - mu[ok]) / sd[ok]
    return z


def design(z, prim, seen):
    cols = [z]
    for p in ("D", "G", "R"):
        if p in seen:
            cols.append(np.array([1.0 if prim == p else 0.0]))
    return np.concatenate(cols)


def clip_pred(coord, value):
    if coord in CLIP_UNIT:
        return float(np.clip(value, 0.0, 1.0))
    if coord in CLIP_NONNEG:
        return float(max(value, 0.0))
    return float(value)


def fit_predict(tasks, train_names, test_names):
    seen = {p for t in train_names for p in tasks[t]["pairs"]}
    mu, sd = scaler(tasks, train_names)
    zero_cols = [FEATS[i] for i in range(len(FEATS)) if sd[i] == 0]

    def rows(names, prims=None):
        xs, ys, keys = [], [], []
        for t in names:
            z = standardize(tasks[t]["x"], mu, sd)
            for p, y in tasks[t]["pairs"].items():
                if prims is not None and p not in prims:
                    continue
                if p not in seen:
                    continue
                xs.append(design(z, p, seen))
                ys.append(y)
                keys.append((t, p))
        return np.vstack(xs), ys, keys

    x_all, y_all, _ = rows(train_names)
    models = {}
    for coord in COORDS:
        if coord == "C_api":
            continue
        if coord == "C_train":
            x_c = np.vstack([standardize(tasks[t]["x"], mu, sd) for t in train_names])
            target = np.array([tasks[t]["pairs"]["C"]["C_train"] for t in train_names])
            model = Ridge(alpha=1.0, fit_intercept=True)
            model.fit(x_c, target)
            models[coord] = model
            continue
        target = np.array([y[coord] for y in y_all])
        model = Ridge(alpha=1.0, fit_intercept=True)
        model.fit(x_all, target)
        models[coord] = model

    means = {}
    for p in seen:
        bucket = [tasks[t]["pairs"][p] for t in train_names if p in tasks[t]["pairs"]]
        means[p] = {c: float(np.mean([y[c] for y in bucket])) for c in COORDS}
        means[p]["C_api"] = 0.0
        if p != "C":
            means[p]["C_train"] = 0.0

    ranges = {}
    for coord in ("Q", "C_infer", "L_p50"):
        vals = [tasks[t]["pairs"][p][coord] for t in train_names for p in tasks[t]["pairs"]]
        ranges[coord] = {"min": float(min(vals)), "max": float(max(vals))}

    learned = {}
    baseline = {}
    raw = {}
    unpredictable = []
    for t in test_names:
        z = standardize(tasks[t]["x"], mu, sd)
        for p in tasks[t]["pairs"]:
            if p not in seen:
                unpredictable.append([t, p])
                continue
            pred = {}
            unclipped = {}
            for coord in COORDS:
                if coord == "C_api":
                    value = 0.0
                elif coord == "C_train" and p != "C":
                    value = 0.0
                elif coord == "C_train":
                    value = float(models[coord].predict(z.reshape(1, -1))[0])
                else:
                    value = float(models[coord].predict(design(z, p, seen).reshape(1, -1))[0])
                unclipped[coord] = value
                pred[coord] = clip_pred(coord, value)
            learned[(t, p)] = pred
            raw[(t, p)] = unclipped
            baseline[(t, p)] = dict(means[p])

    coef = {}
    for coord, model in models.items():
        names = list(FEATS)
        for p in ("D", "G", "R"):
            if p in seen and coord != "C_train":
                names.append(p)
        if coord == "C_train":
            names = list(FEATS)
        coef[coord] = {
            "intercept": float(model.intercept_),
            "coef": {n: float(c) for n, c in zip(names, model.coef_)},
        }

    return {
        "seen": sorted(seen),
        "zero_variance": zero_cols,
        "n_train_pairs": int(sum(len(tasks[t]["pairs"]) for t in train_names)),
        "ranges": ranges,
        "learned": learned,
        "baseline": baseline,
        "raw": raw,
        "unpredictable": unpredictable,
        "coef": coef,
        "train_tasks": list(train_names),
    }


def scale(value, spec):
    span = spec["max"] - spec["min"]
    if span == 0:
        return 0.0
    return (value - spec["min"]) / span


def utility(vec, ranges, shared):
    q = scale(vec["Q"], ranges["Q"])
    c = scale(vec["C_infer"], ranges["C_infer"])
    ell = scale(vec["L_p50"], ranges["L_p50"])
    if shared:
        return q - 0.5 * c - 0.5 * ell
    return q - c - ell


def choose(cands, score, higher):
    best_p, best_s = None, None
    for p in ORDER:
        if p not in cands:
            continue
        s = score(p)
        if best_p is None or (higher and s > best_s) or ((not higher) and s < best_s):
            best_p, best_s = p, s
    return best_p


def policies(tasks, test_names, fit):
    out = []
    for t in test_names:
        eligible = list(tasks[t]["pairs"])
        predicted = [p for p in eligible if (t, p) in fit["learned"]]
        sources = {
            "learned": fit["learned"],
            "mean": fit["baseline"],
            "oracle": { (t, p): tasks[t]["pairs"][p] for p in eligible },
        }

        def fixed(name):
            if name == "mask":
                return "R" if "R" in eligible else "C"
            return name

        row = {"task": t, "fixed": {}, "vector": {}}
        for name, prim in (("G", "G"), ("C", "C"), ("D", "D"), ("mask", "mask")):
            chosen = fixed(prim)
            row["fixed"][name] = chosen
        for policy in ("max_Q", "min_L_p50", "equal", "shared"):
            row["vector"][policy] = {}
            for source, table in sources.items():
                cands = eligible if source == "oracle" else predicted

                def score(p, policy=policy, table=table):
                    vec = table[(t, p)]
                    if policy == "max_Q":
                        return vec["Q"]
                    if policy == "min_L_p50":
                        return vec["L_p50"]
                    return utility(vec, fit["ranges"], shared=(policy == "shared"))

                higher = policy != "min_L_p50"
                chosen = choose(cands, score, higher)
                oracle = row["vector"][policy].get("oracle")
                row["vector"][policy][source] = chosen
                if source != "oracle":
                    row["vector"][policy][source + "_matches_oracle"] = chosen == row["vector"][policy]["oracle"] if "oracle" in row["vector"][policy] else None
            # oracle is filled last if iteration order is learned, mean, oracle.
            # Recompute matches after all sources exist.
            oracle_choice = row["vector"][policy]["oracle"]
            for source in ("learned", "mean"):
                row["vector"][policy][source + "_matches_oracle"] = row["vector"][policy][source] == oracle_choice
        measured = {}
        for label, prim in row["fixed"].items():
            measured[label] = tasks[t]["pairs"][prim]
        for policy, sources_out in row["vector"].items():
            measured[policy] = {
                s: tasks[t]["pairs"][sources_out[s]]
                for s in ("learned", "mean", "oracle")
            }
        row["measured"] = {
            k: {c: measured[k][c] for c in COORDS} if k in row["fixed"] else {
                s: {c: measured[k][s][c] for c in COORDS} for s in ("learned", "mean", "oracle")
            }
            for k in list(row["fixed"]) + list(row["vector"])
        }
        out.append(row)
    return out


def errors(tasks, fit):
    by_task = {}
    pairs = []
    for (t, p), pred in fit["learned"].items():
        actual = tasks[t]["pairs"][p]
        base = fit["baseline"][(t, p)]
        cell = {
            "task": t,
            "primitive": p,
            "abs": {},
            "actual": actual,
            "learned": pred,
            "raw": fit["raw"][(t, p)],
            "mean": base,
        }
        for c in COORDS:
            cell["abs"][c] = {
                "learned": abs(pred[c] - actual[c]),
                "mean": abs(base[c] - actual[c]),
            }
        pairs.append(cell)
        by_task.setdefault(t, []).append(cell)
    summary = []
    for t, cells in by_task.items():
        row = {"task": t, "n_pairs": len(cells)}
        for c in COORDS:
            row[c] = {
                "learned": float(np.mean([cell["abs"][c]["learned"] for cell in cells])),
                "mean": float(np.mean([cell["abs"][c]["mean"] for cell in cells])),
            }
            row[c]["learned_minus_mean"] = row[c]["learned"] - row[c]["mean"]
        c_cells = [cell for cell in cells if cell["primitive"] == "C"]
        if c_cells:
            row["C_train_classifier_only"] = {
                "learned": c_cells[0]["abs"]["C_train"]["learned"],
                "mean": c_cells[0]["abs"]["C_train"]["mean"],
            }
        summary.append(row)
    return summary, pairs


def main():
    tasks = load()
    pool = [name for name, row in tasks.items() if row["selector_training"]]
    assert "esci_en_us_task2" not in pool
    assert sum(len(tasks[t]["pairs"]) for t in pool) == 22
    folds = []
    for family, held in HOLDOUTS:
        train = [t for t in pool if t not in held]
        assert "esci_en_us_task2" not in train
        fit = fit_predict(tasks, train, held)
        summary, pairs = errors(tasks, fit)
        folds.append(
            {
                "holdout": family,
                "held_out": held,
                "train_tasks": fit["train_tasks"],
                "n_train_pairs": fit["n_train_pairs"],
                "seen_primitives": fit["seen"],
                "zero_variance_features": fit["zero_variance"],
                "unpredictable": fit["unpredictable"],
                "ranges": fit["ranges"],
                "task_mae": summary,
                "pairs": pairs,
                "policies": policies(tasks, held, fit),
                "coefficients": fit["coef"] if family == "E-commerce" else None,
            }
        )
        if family != "E-commerce":
            folds[-1].pop("coefficients")
    security = next(f for f in folds if f["holdout"] == "Security")
    assert security["unpredictable"] == [["sms_spam", "R"]]
    OUT.write_text(json.dumps({"freeze": "SD-1", "alpha": 1.0, "std": "ddof0", "folds": folds}, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
