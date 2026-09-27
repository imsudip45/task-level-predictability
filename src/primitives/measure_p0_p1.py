"""Score the rule and the conventional classifier under EP-1.

Does not fit a selector. Does not call a generative model or a decision model.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fingerprint"))
import compute_static_fingerprint as fp

ROOT = fp.ROOT
RAW = fp.RAW
OUT = ROOT / "results" / "raw"
RULE = ROOT / "configs" / "sms_rule.txt"
RULE_SHA = "264e288b89a430005de7b72fdfeb77862e46b23b7415c76df285e4e5e1a7f992"
EVAL_CAP = 1000
TRAIN_CAP = 100_000
RESULT = OUT / "performance_p0_p1.json"


def task_rng(prefix: str, task: str) -> np.random.Generator:
    digest = hashlib.sha256(f"{prefix}-{task}".encode()).digest()[:8]
    return np.random.default_rng(int.from_bytes(digest, "little"))


def choose_eval(n: int, task: str) -> list[int]:
    if n <= EVAL_CAP:
        return list(range(n))
    rng = task_rng("eval-20260926", task)
    return sorted(int(i) for i in rng.choice(n, size=EVAL_CAP, replace=False))


def stratified_cap(labels: list[str], task: str) -> list[int]:
    if len(labels) <= TRAIN_CAP:
        return list(range(len(labels)))
    rng = task_rng("traincap-20260927", task)
    by: dict[str, list[int]] = {}
    for i, y in enumerate(labels):
        by.setdefault(y, []).append(i)
    raw = {k: TRAIN_CAP * len(v) / len(labels) for k, v in by.items()}
    floors = {k: int(math.floor(v)) for k, v in raw.items()}
    left = TRAIN_CAP - sum(floors.values())
    order = sorted(by, key=lambda k: (raw[k] - floors[k], k), reverse=True)
    for k in order:
        if left <= 0:
            break
        floors[k] += 1
        left -= 1
    chosen = []
    for k, idxs in by.items():
        take = min(floors[k], len(idxs))
        pick = rng.choice(len(idxs), size=take, replace=False)
        chosen.extend(idxs[int(j)] for j in pick)
    return sorted(chosen)


def take(xs, idx):
    return [xs[i] for i in idx]


def score_classifier(task: str, train_x, train_y, eval_x, eval_y, already_capped: bool = False) -> dict:
    if already_capped:
        condition = "C100k"
        x_fit, y_fit = train_x, train_y
    else:
        cap = stratified_cap(train_y, task)
        condition = "Cfull" if len(cap) == len(train_y) else "C100k"
        x_fit, y_fit = take(train_x, cap), take(train_y, cap)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=30000, sublinear_tf=True)
    t0 = time.perf_counter()
    x_train = vectorizer.fit_transform(x_fit)
    clf = LogisticRegression(solver="saga", C=1.0, max_iter=200)
    clf.fit(x_train, y_fit)
    train_s = time.perf_counter() - t0
    x_eval = vectorizer.transform(eval_x)
    lat = []
    pred = []
    t1 = time.perf_counter()
    for row in x_eval:
        a = time.perf_counter()
        pred.append(clf.predict(row)[0])
        lat.append((time.perf_counter() - a) * 1000)
    infer_s = time.perf_counter() - t1
    lat_a = np.asarray(lat)
    return {
        "primitive": condition,
        "Q_macro_f1": float(f1_score(eval_y, pred, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(eval_y, pred)),
        "C_train_seconds": train_s,
        "C_infer_seconds": infer_s,
        "C_api_usd": 0.0,
        "L_p50_ms": float(np.percentile(lat_a, 50, method="linear")),
        "L_p95_ms": float(np.percentile(lat_a, 95, method="linear")),
        "n_train_fit": len(y_fit),
        "n_eval": len(eval_y),
        "invalid_outputs": 0,
    }


def score_rule(eval_x, eval_y) -> dict:
    raw = RULE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != RULE_SHA:
        raise SystemExit("sms rule hash mismatch")
    pattern = raw.decode("utf-8")
    if pattern.endswith("\n"):
        pattern = pattern[:-1]
    rx = __import__("re").compile(pattern)
    lat = []
    pred = []
    t1 = time.perf_counter()
    for text in eval_x:
        a = time.perf_counter()
        pred.append("spam" if rx.search(text) else "ham")
        lat.append((time.perf_counter() - a) * 1000)
    infer_s = time.perf_counter() - t1
    lat_a = np.asarray(lat)
    return {
        "primitive": "R",
        "Q_macro_f1": float(f1_score(eval_y, pred, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(eval_y, pred)),
        "C_train_seconds": 0.0,
        "C_infer_seconds": infer_s,
        "C_api_usd": 0.0,
        "L_p50_ms": float(np.percentile(lat_a, 50, method="linear")),
        "L_p95_ms": float(np.percentile(lat_a, 95, method="linear")),
        "n_train_fit": 0,
        "n_eval": len(eval_y),
        "invalid_outputs": 0,
        "rule_sha256": RULE_SHA,
    }


def subset(texts, labels, task):
    idx = choose_eval(len(texts), task)
    return take(texts, idx), take(labels, idx), idx


def load_banking():
    train_x, train_y = fp.read_banking()
    texts, labels = [], []
    import csv
    with (RAW / "banking77_test.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
        header = next(reader)
        if header != ["text", "category"]:
            raise SystemExit(f"banking test header {header}")
        for row in reader:
            texts.append(row[0])
            labels.append(row[1])
    if len(texts) != 3080:
        raise SystemExit(f"banking test {len(texts)}")
    return train_x, train_y, texts, labels


def load_clinc():
    train_x, train_y = fp.read_clinc()
    legal = fp.class_names(fp.CARD_DIR / "clinc_oos.json", "plus", "intent")
    table = pq.read_table(RAW / "clinc_plus_test.parquet", columns=["text", "intent"])
    texts = table.column("text").to_pylist()
    labels = [legal[i] for i in table.column("intent").to_pylist()]
    return train_x, train_y, texts, labels


def load_civil():
    # Training labels and a later text gather for the cap only.
    labels = []
    files = sorted((RAW / "civil").glob("*.parquet"))
    for path in files:
        table = pq.read_table(path, columns=["toxicity"])
        labels.extend("toxic" if v >= 0.5 else "nontoxic" for v in table.column("toxicity").to_pylist())
    cap = stratified_cap(labels, "civil_comments_binary")
    wanted = set(cap)
    texts = []
    seen = 0
    grabbed = {}
    for path in files:
        table = pq.read_table(path, columns=["text"])
        for text in table.column("text").to_pylist():
            if seen in wanted:
                grabbed[seen] = "" if text is None else text
            seen += 1
    train_x = [grabbed[i] for i in cap]
    train_y = [labels[i] for i in cap]
    test = pq.read_table(RAW / "civil_test.parquet", columns=["text", "toxicity"])
    ev_x = [("" if t is None else t) for t in test.column("text").to_pylist()]
    ev_y = ["toxic" if v >= 0.5 else "nontoxic" for v in test.column("toxicity").to_pylist()]
    return train_x, train_y, ev_x, ev_y


def load_sms():
    legal = fp.class_names(fp.CARD_DIR / "sms_spam.json", "plain_text", "label")
    table = pq.read_table(RAW / "sms_train.parquet", columns=["sms", "label"])
    texts = table.column("sms").to_pylist()
    labels = [legal[i] for i in table.column("label").to_pylist()]
    train_idx = set(json.loads((ROOT / "data" / "fingerprint" / "sms_train_indices.json").read_text(encoding="utf-8")))
    tr_x = [texts[i] for i in range(len(texts)) if i in train_idx]
    tr_y = [labels[i] for i in range(len(texts)) if i in train_idx]
    te_x = [texts[i] for i in range(len(texts)) if i not in train_idx]
    te_y = [labels[i] for i in range(len(texts)) if i not in train_idx]
    return tr_x, tr_y, te_x, te_y


def esci_texts(which: str):
    import pyarrow.parquet as pq
    examples = pq.read_table(
        RAW / "esci_official" / "examples.parquet",
        columns=["query", "product_id", "product_locale", "esci_label", "large_version", "split"],
    ).to_pydict()
    name_of = {"E": "Exact", "S": "Substitute", "C": "Complement", "I": "Irrelevant"}
    rows = []
    for i, (loc, big, split, lab) in enumerate(
        zip(examples["product_locale"], examples["large_version"], examples["split"], examples["esci_label"])
    ):
        if loc == "us" and int(big) == 1 and split == which:
            rows.append((examples["query"][i], examples["product_id"][i], name_of[lab]))
    return rows


def attach_products(rows, folders):
    needed = {(pid, "us") for _, pid, _ in rows}
    found = {}
    for folder in folders:
        for path in sorted(folder.glob("*.parquet")):
            table = pq.read_table(
                path,
                columns=["product_id", "product_locale", "product_title", "product_description", "product_bullet_point"],
            )
            prod = table.to_pydict()
            for i, pid in enumerate(prod["product_id"]):
                key = (pid, prod["product_locale"][i])
                if key in needed and key not in found:
                    found[key] = (prod["product_title"][i], prod["product_description"][i], prod["product_bullet_point"][i])
            if len(found) == len(needed):
                break
    texts, labels = [], []
    missing = 0
    for query, pid, lab in rows:
        hit = found.get((pid, "us"))
        if hit is None:
            missing += 1
            continue
        title, desc, bullets = hit
        texts.append(fp.blank_join([query, title, desc, bullets]))
        labels.append(lab)
    if missing:
        raise SystemExit(f"esci missing product text {missing} of {len(rows)}")
    return texts, labels


def load_esci():
    train_rows = esci_texts("train")
    labels_only = [lab for _, _, lab in train_rows]
    cap = stratified_cap(labels_only, "esci_en_us_task2")
    train_keep = [train_rows[i] for i in cap]
    test_rows = esci_texts("test")
    ev_idx = choose_eval(len(test_rows), "esci_en_us_task2")
    test_keep = [test_rows[i] for i in ev_idx]
    folders = [RAW / "esci", RAW / "esci_test"]
    tr_x, tr_y = attach_products(train_keep, folders)
    te_x, te_y = attach_products(test_keep, folders)
    return tr_x, tr_y, te_x, te_y, ev_idx


def load_ledgar():
    legal = fp.ledgar_names()
    train_x, train_y = fp.read_ledgar(legal)
    table = pq.read_table(RAW / "ledgar_test.parquet", columns=["text", "label"])
    texts = table.column("text").to_pylist()
    labels = [legal[i] for i in table.column("label").to_pylist()]
    return train_x, train_y, texts, labels


def load_pubmed():
    texts, labels, meta = fp.pubmed_split()
    # Rebuild the official test half with the same seed, without using dev as test.
    import random
    from functools import reduce

    random.seed(0)
    dataset = json.loads((RAW / "ori_pqal.json").read_text(encoding="utf-8"))

    def split_label(pmids, fold):
        random.shuffle(pmids)
        num_split = math.ceil(len(pmids) / fold)
        return [pmids[i * num_split : (i + 1) * num_split] if i < fold - 1 else pmids[i * num_split :] for i in range(fold)]

    def split(data, fold):
        add = lambda xs: reduce(lambda a, b: a + b, xs)
        label2pmid = {"yes": [], "no": [], "maybe": []}
        for pmid, info in data.items():
            label2pmid[info["final_decision"]].append(pmid)
        parts = {k: split_label(v, fold) for k, v in label2pmid.items()}
        output = []
        for i in range(fold):
            pmids = add([v[i] for v in parts.values()])
            output.append({pmid: data[pmid] for pmid in pmids})
        if len(output[-1]) != len(output[0]):
            for i in range(fold - 1):
                picked = random.choice(list(output[i]))
                output[-1][picked] = output[i][picked]
                output[i].pop(picked)
        return output

    _, testset = split(dataset, 2)
    ev_x, ev_y = [], []
    for info in testset.values():
        ev_x.append(fp.blank_join([info["QUESTION"], *info["CONTEXTS"]]))
        ev_y.append(info["final_decision"])
    if len(ev_y) != meta["test"]:
        raise SystemExit("pubmed test recount mismatch")
    return texts, labels, ev_x, ev_y


def load_vitamin():
    def read(name):
        xs, ys = [], []
        with zipfile.ZipFile(RAW / "vitaminc.zip") as zf:
            with zf.open(name) as f:
                for line in f:
                    row = json.loads(line)
                    xs.append(fp.blank_join([row["claim"], row["evidence"]]))
                    ys.append(row["label"])
        return xs, ys
    train_x, train_y = read("vitaminc/train.jsonl")
    ev_x, ev_y = read("vitaminc/test.jsonl")
    cap = stratified_cap(train_y, "vitaminc")
    return take(train_x, cap), take(train_y, cap), ev_x, ev_y


LOADERS = {
    "banking77": load_banking,
    "clinc_oos_plus": load_clinc,
    "civil_comments_binary": load_civil,
    "sms_spam": load_sms,
    "esci_en_us_task2": load_esci,
    "ledgar": load_ledgar,
    "pubmedqa_fold0": load_pubmed,
    "vitaminc": load_vitamin,
}


def store(task, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    existing = []
    if RESULT.exists():
        existing = json.loads(RESULT.read_text(encoding="utf-8"))
    existing = [r for r in existing if r["task"] != task]
    existing.extend(rows)
    RESULT.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def run(task: str):
    loaded = LOADERS[task]()
    if task == "esci_en_us_task2":
        train_x, train_y, ev_x, ev_y, idx = loaded
    else:
        train_x, train_y, ev_x, ev_y = loaded
        ev_x, ev_y, idx = subset(ev_x, ev_y, task)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{task}_eval_indices.json").write_text(json.dumps(idx), encoding="utf-8")
    rows = []
    if task == "sms_spam":
        rows.append({"task": task, **score_rule(ev_x, ev_y)})
    capped = task in {"civil_comments_binary", "esci_en_us_task2", "vitaminc"}
    rows.append({"task": task, **score_classifier(task, train_x, train_y, ev_x, ev_y, already_capped=capped)})
    store(task, rows)
    for row in rows:
        print(task, row["primitive"], round(row["Q_macro_f1"], 4), row["n_eval"], row["n_train_fit"])


if __name__ == "__main__":
    for task in sys.argv[1:]:
        run(task)
