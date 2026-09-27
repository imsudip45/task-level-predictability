"""Static fingerprint for the eight FPS-2 candidates.

Reads training rows only. Does not read test files. Does not train a model.
Even-count medians are the mean of the two central values.
Percentiles use numpy percentile, method='linear'.
Normalized entropy is Shannon entropy in nats divided by ln(K).
Length samples for Civil Comments and ESCI are a simple random sample of
20,000 training-row indices from numpy.random.default_rng(20260926).
SMS training rows are a per-label shuffle with that same generator, in sorted
label order, keeping floor(0.8 * n_class) rows for training.
PubMedQA follows preprocess/split_dataset.py with random.seed(0), fold 0.
"""

from __future__ import annotations

import csv
import json
import math
import sys
import zipfile
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import torch
from transformers import AutoModel, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "fingerprint"
CARD_DIR = ROOT / "literature" / "raw" / "datasets"
LEDGAR_CARD = CARD_DIR / "lex_glue.json"
SEED = 20260926
LENGTH_SAMPLE = 20_000

CIVIL_LABELS = ("nontoxic", "toxic")


def norm_label(name: str) -> str:
    return name.lower().replace("_", " ").replace("-", " ")


def entropy_stats(counts: list[int]) -> dict:
    k = len(counts)
    total = sum(counts)
    h = 0.0
    for c in counts:
        if c:
            p = c / total
            h -= p * math.log(p)
    mn = min(counts)
    mx = max(counts)
    ratio = None if mn == 0 else mx / mn
    ordered = sorted(counts)
    mid = k // 2
    if k % 2:
        median = float(ordered[mid])
    else:
        median = (ordered[mid - 1] + ordered[mid]) / 2
    return {
        "k": k,
        "n": total,
        "min_per_class": mn,
        "median_per_class": median,
        "max_per_class": mx,
        "max_min_ratio": ratio,
        "normalized_entropy": h / math.log(k),
    }


def length_stats(lengths: np.ndarray) -> dict:
    return {
        "n_lengths": int(lengths.size),
        "median_tokens": float(np.percentile(lengths, 50, method="linear")),
        "p95_tokens": float(np.percentile(lengths, 95, method="linear")),
    }


def tokenize_lengths(tokenizer, texts: list[str], batch: int = 256) -> np.ndarray:
    out = np.empty(len(texts), dtype=np.int32)
    for start in range(0, len(texts), batch):
        piece = texts[start : start + batch]
        encoded = tokenizer(
            piece,
            add_special_tokens=False,
            padding=False,
            truncation=False,
            verbose=False,
        )
        for i, ids in enumerate(encoded["input_ids"]):
            out[start + i] = len(ids)
    return out


def mean_pool(hidden, mask):
    mask = mask.unsqueeze(-1).expand(hidden.size()).float()
    return (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)


def label_similarity(tokenizer, model, names: list[str]) -> dict:
    cleaned = [norm_label(n) for n in names]
    batch = tokenizer(cleaned, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**batch).last_hidden_state
        emb = mean_pool(hidden, batch["attention_mask"])
        emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    sim = emb @ emb.T
    k = len(names)
    vals = [float(sim[i, j]) for i in range(k) for j in range(i + 1, k)]
    return {
        "label_names_normalized": cleaned,
        "mean_pairwise_cosine": float(np.mean(vals)),
        "min_pairwise_cosine": float(np.min(vals)),
        "n_pairs": len(vals),
    }


def count_vector(labels: list[str], legal: list[str]) -> list[int]:
    index = {name: i for i, name in enumerate(legal)}
    counts = [0] * len(legal)
    for label in labels:
        if label not in index:
            raise SystemExit(f"unexpected label {label!r}")
        counts[index[label]] += 1
    return counts


def class_names(card_path: Path, config: str | None, feature: str) -> list[str]:
    card = json.loads(card_path.read_text(encoding="utf-8"))
    info = card["cardData"]["dataset_info"]
    configs = info if isinstance(info, list) else [info]
    if config is None:
        chosen = configs[0]
    else:
        chosen = next(c for c in configs if c.get("config_name") == config)
    for feat in chosen["features"]:
        if feat["name"] == feature:
            names = feat["dtype"]["class_label"]["names"]
            if isinstance(names, dict):
                return [names[str(i)] for i in range(len(names))]
            return list(names)
    raise SystemExit(f"missing {feature} in {card_path.name}")
    index = {name: i for i, name in enumerate(legal)}
    counts = [0] * len(legal)
    for label in labels:
        if label not in index:
            raise SystemExit(f"unexpected label {label!r}; legal={legal[:8]}...")
        counts[index[label]] += 1
    return counts


def read_banking() -> tuple[list[str], list[str]]:
    path = RAW / "banking77_train.csv"
    texts, labels = [], []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
        header = next(reader)
        if header != ["text", "category"]:
            raise SystemExit(f"banking header {header}")
        for row in reader:
            text, label = row
            texts.append(text)
            labels.append(label)
    if len(texts) != 10003:
        raise SystemExit(f"banking train rows {len(texts)}")
    return texts, labels


def read_clinc() -> tuple[list[str], list[str]]:
    legal = class_names(CARD_DIR / "clinc_oos.json", "plus", "intent")
    table = pq.read_table(RAW / "clinc_plus_train.parquet", columns=["text", "intent"])
    texts = table.column("text").to_pylist()
    labels = [legal[i] for i in table.column("intent").to_pylist()]
    if len(texts) != 15250:
        raise SystemExit(f"clinc plus train rows {len(texts)}")
    return texts, labels


def read_sms() -> tuple[list[str], list[str], list[int]]:
    legal = class_names(CARD_DIR / "sms_spam.json", "plain_text", "label")
    table = pq.read_table(RAW / "sms_train.parquet", columns=["sms", "label"])
    texts = table.column("sms").to_pylist()
    labels = [legal[i] for i in table.column("label").to_pylist()]
    if len(texts) != 5574:
        raise SystemExit(f"sms rows {len(texts)}")
    legal = sorted(set(labels))
    rng = np.random.default_rng(SEED)
    keep = []
    for label in legal:
        idx = [i for i, y in enumerate(labels) if y == label]
        order = rng.permutation(len(idx))
        n_train = (len(idx) * 4) // 5
        if len(idx) >= 2:
            n_train = min(max(n_train, 1), len(idx) - 1)
        chosen = [idx[int(i)] for i in order[:n_train]]
        keep.extend(chosen)
    keep.sort()
    train_texts = [texts[i] for i in keep]
    train_labels = [labels[i] for i in keep]
    return train_texts, train_labels, keep


def read_ledgar(legal: list[str]) -> tuple[list[str], list[str]]:
    table = pq.read_table(RAW / "ledgar_train.parquet", columns=["text", "label"])
    texts = table.column("text").to_pylist()
    raw = table.column("label").to_pylist()
    if len(texts) != 60000:
        raise SystemExit(f"ledgar train rows {len(texts)}")
    if raw and isinstance(raw[0], int):
        labels = [legal[i] for i in raw]
    else:
        labels = [str(x) for x in raw]
    return texts, labels


def ledgar_names() -> list[str]:
    return class_names(LEDGAR_CARD, "ledgar", "label")


def blank_join(parts: list[str]) -> str:
    return "\n\n".join("" if part is None else str(part) for part in parts)


def parquet_paths(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.parquet"))


def civil_pass(tokenizer) -> tuple[dict, np.ndarray]:
    labels = []
    n = 0
    files = parquet_paths(RAW / "civil")
    for path in files:
        table = pq.read_table(path, columns=["toxicity"])
        labels.extend(table.column("toxicity").to_pylist())
        n += table.num_rows
    if n != 1804874:
        raise SystemExit(f"civil train rows {n}")
    if any(v is None or (isinstance(v, float) and math.isnan(v)) for v in labels):
        raise SystemExit("civil toxicity has nulls")
    y = ["toxic" if v >= 0.5 else "nontoxic" for v in labels]
    counts = count_vector(y, list(CIVIL_LABELS))
    rng = np.random.default_rng(SEED)
    chosen = set(int(i) for i in rng.choice(n, size=LENGTH_SAMPLE, replace=False))
    texts = []
    seen = 0
    for path in files:
        table = pq.read_table(path, columns=["text"])
        for text in table.column("text").to_pylist():
            if seen in chosen:
                texts.append("" if text is None else text)
            seen += 1
    if len(texts) != LENGTH_SAMPLE:
        raise SystemExit(f"civil sample {len(texts)}")
    return entropy_stats(counts), tokenize_lengths(tokenizer, texts)


def esci_pass(tokenizer) -> tuple[dict, np.ndarray, list[str]]:
    examples = pq.read_table(
        RAW / "esci_official" / "examples.parquet",
        columns=["query", "product_id", "product_locale", "esci_label", "large_version", "split"],
    )
    rows = examples.to_pydict()
    name_of = {"E": "Exact", "S": "Substitute", "C": "Complement", "I": "Irrelevant"}
    kept = []
    labels = []
    for i, (loc, big, split, lab) in enumerate(
        zip(rows["product_locale"], rows["large_version"], rows["split"], rows["esci_label"])
    ):
        if loc == "us" and int(big) == 1 and split == "train":
            kept.append(i)
            labels.append(name_of[lab])
    if len(labels) != 1393063:
        raise SystemExit(f"esci us task2 train rows {len(labels)}")
    legal = ["Exact", "Substitute", "Complement", "Irrelevant"]
    counts = count_vector(labels, legal)
    rng = np.random.default_rng(SEED)
    chosen = {int(i) for i in rng.choice(len(kept), size=LENGTH_SAMPLE, replace=False)}
    needed = {}
    for pos in chosen:
        src = kept[pos]
        needed[(rows["product_id"][src], rows["product_locale"][src])] = rows["query"][src]
    products_found = {}
    for path in sorted((RAW / "esci").glob("*.parquet")):
        table = pq.read_table(
            path,
            columns=["product_id", "product_locale", "product_title", "product_description", "product_bullet_point"],
        )
        prod = table.to_pydict()
        for i, pid in enumerate(prod["product_id"]):
            key = (pid, prod["product_locale"][i])
            if key in needed and key not in products_found:
                products_found[key] = (
                    prod["product_title"][i],
                    prod["product_description"][i],
                    prod["product_bullet_point"][i],
                )
        if len(products_found) == len(needed):
            break
    found = products_found
    texts = []
    for pos in sorted(chosen):
        src = kept[pos]
        key = (rows["product_id"][src], rows["product_locale"][src])
        title, desc, bullets = found[key]
        texts.append(blank_join([rows["query"][src], title, desc, bullets]))
    if len(texts) != LENGTH_SAMPLE:
        raise SystemExit(f"esci sample {len(texts)} found {len(found)}")
    return entropy_stats(counts), tokenize_lengths(tokenizer, texts), legal


def pubmed_split() -> tuple[list[str], list[str], dict]:
    import random

    random.seed(0)
    dataset = json.loads((RAW / "ori_pqal.json").read_text(encoding="utf-8"))
    # Official split_dataset.py, copied in structure.
    from functools import reduce

    def split_label(pmids, fold):
        random.shuffle(pmids)
        num_all = len(pmids)
        num_split = math.ceil(num_all / fold)
        output = []
        for i in range(fold):
            if i == fold - 1:
                output.append(pmids[i * num_split :])
            else:
                output.append(pmids[i * num_split : (i + 1) * num_split])
        return output

    def split(data, fold):
        add = lambda xs: reduce(lambda a, b: a + b, xs)
        label2pmid = {"yes": [], "no": [], "maybe": []}
        for pmid, info in data.items():
            label2pmid[info["final_decision"]].append(pmid)
        label2pmid = {k: split_label(v, fold) for k, v in label2pmid.items()}
        output = []
        for i in range(fold):
            pmids = add([v[i] for _, v in label2pmid.items()])
            output.append({pmid: data[pmid] for pmid in pmids})
        if len(output[-1]) != len(output[0]):
            for i in range(fold - 1):
                pmids = list(output[i])
                picked = random.choice(pmids)
                output[-1][picked] = output[i][picked]
                output[i].pop(picked)
        return output

    cv_set, testset = split(dataset, 2)
    cv_sets = split(cv_set, 10)
    train = {}
    for i in range(10):
        if i != 0:
            train.update(cv_sets[i])
    dev = cv_sets[0]
    texts, labels = [], []
    for info in train.values():
        contexts = info.get("CONTEXTS")
        if contexts is None:
            raise SystemExit(f"pubmed keys {sorted(info.keys())}")
        texts.append(blank_join([info["QUESTION"], *contexts]))
        labels.append(info["final_decision"])
    meta = {
        "train": len(train),
        "dev_fold0": len(dev),
        "test": len(testset),
        "train_pmids": list(train.keys()),
    }
    return texts, labels, meta


def vitamin_rows() -> tuple[list[str], list[str]]:
    zpath = RAW / "vitaminc.zip"
    texts, labels = [], []
    with zipfile.ZipFile(zpath) as zf:
        names = [n for n in zf.namelist() if n.endswith(".jsonl") and "train" in n.lower() and "test" not in n.lower() and "dev" not in n.lower()]
        if len(names) != 1:
            raise SystemExit(f"vitaminc train files {names}")
        with zf.open(names[0]) as f:
            for line in f:
                row = json.loads(line)
                if "claim" not in row or "evidence" not in row or "label" not in row:
                    raise SystemExit(f"vitaminc keys {sorted(row.keys())}")
                texts.append(blank_join([row["claim"], row["evidence"]]))
                labels.append(row["label"])
    return texts, labels


def pack(name, texts, labels, legal, tokenizer, model, extra=None, lengths=None, imbalance=None):
    if imbalance is None:
        imbalance = entropy_stats(count_vector(labels, legal))
    if lengths is None:
        lengths = tokenize_lengths(tokenizer, texts)
    row = {
        "candidate": name,
        "structural": extra or {},
        "imbalance": imbalance,
        "length": length_stats(lengths),
        "label_similarity": label_similarity(tokenizer, model, legal),
    }
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tok_name = "bert-base-uncased"
    enc_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(tok_name)
    enc_tok = AutoTokenizer.from_pretrained(enc_name)
    model = AutoModel.from_pretrained(enc_name)
    model.eval()

    rows = []

    texts, labels = read_banking()
    legal = sorted(set(labels))
    if len(legal) != 77:
        raise SystemExit(f"banking k {len(legal)}")
    rows.append(pack("banking77", texts, labels, legal, tokenizer, model, {"input_structure": "free_text", "evidence_required": False, "external_knowledge_required": False, "relation_code": "utterance", "documented_shift": "none_documented", "selector_training": True, "rules": False}))

    texts, labels = read_clinc()
    legal = sorted(set(labels))
    if len(legal) != 151:
        raise SystemExit(f"clinc k {len(legal)}")
    rows.append(pack("clinc_oos_plus", texts, labels, legal, tokenizer, model, {"input_structure": "free_text", "evidence_required": False, "external_knowledge_required": False, "relation_code": "utterance", "documented_shift": "unspecified", "selector_training": True, "rules": False}))

    imb, lengths = civil_pass(tokenizer)
    rows.append({
        "candidate": "civil_comments_binary",
        "structural": {"input_structure": "free_text", "evidence_required": False, "external_knowledge_required": False, "relation_code": "utterance", "documented_shift": "unspecified", "selector_training": True, "rules": False, "length_sample": LENGTH_SAMPLE, "declared_binary_names": list(CIVIL_LABELS)},
        "imbalance": imb,
        "length": length_stats(lengths),
        "label_similarity": label_similarity(enc_tok, model, list(CIVIL_LABELS)),
    })

    texts, labels, sms_idx = read_sms()
    legal = sorted(set(labels))
    (OUT / "sms_train_indices.json").write_text(json.dumps(sms_idx), encoding="utf-8")
    rows.append(pack("sms_spam", texts, labels, legal, tokenizer, model, {"input_structure": "free_text", "evidence_required": False, "external_knowledge_required": False, "relation_code": "utterance", "documented_shift": "none_documented", "selector_training": True, "rules": True, "n_train_indices": len(sms_idx)}))

    if "--esci-only" in sys.argv:
        imb, lengths, esci_names = esci_pass(tokenizer)
        existing = json.loads((OUT / "fingerprint.json").read_text(encoding="utf-8"))
        existing["candidates"] = [c for c in existing["candidates"] if c["candidate"] != "esci_en_us_task2"]
        existing["candidates"].insert(4, {
            "candidate": "esci_en_us_task2",
            "structural": {"input_structure": "text_plus_evidence", "evidence_required": True, "external_knowledge_required": False, "relation_code": "paired_text", "documented_shift": "query_grouped", "selector_training": False, "rules": False, "length_sample": LENGTH_SAMPLE},
            "imbalance": imb,
            "length": length_stats(lengths),
            "label_similarity": label_similarity(enc_tok, model, esci_names),
        })
        (OUT / "fingerprint.json").write_text(json.dumps(existing, indent=2), encoding="utf-8")
        print("esci", imb["n"], round(imb["normalized_entropy"], 4), round(length_stats(lengths)["median_tokens"], 2))
        return

    if "--no-esci" not in sys.argv:
        imb, lengths, esci_names = esci_pass(tokenizer)
        rows.append({
            "candidate": "esci_en_us_task2",
            "structural": {"input_structure": "text_plus_evidence", "evidence_required": True, "external_knowledge_required": False, "relation_code": "paired_text", "documented_shift": "query_grouped", "selector_training": False, "rules": False, "length_sample": LENGTH_SAMPLE},
            "imbalance": imb,
            "length": length_stats(lengths),
            "label_similarity": label_similarity(enc_tok, model, esci_names),
        })

    legal = ledgar_names()
    texts, labels = read_ledgar(legal)
    rows.append(pack("ledgar", texts, labels, legal, tokenizer, model, {"input_structure": "free_text", "evidence_required": False, "external_knowledge_required": False, "relation_code": "utterance", "documented_shift": "unspecified", "selector_training": True, "rules": False}))

    texts, labels, meta = pubmed_split()
    (OUT / "pubmedqa_fold0_train_pmids.json").write_text(json.dumps(meta["train_pmids"]), encoding="utf-8")
    legal = ["yes", "no", "maybe"]
    row = pack("pubmedqa_fold0", texts, labels, legal, tokenizer, model, {"input_structure": "text_plus_evidence", "evidence_required": True, "external_knowledge_required": False, "relation_code": "paired_text", "documented_shift": "unspecified", "selector_training": True, "rules": False, "split_counts": {k: meta[k] for k in ("train", "dev_fold0", "test")}})
    rows.append(row)

    texts, labels = vitamin_rows()
    legal = sorted(set(labels))
    rows.append(pack("vitaminc", texts, labels, legal, tokenizer, model, {"input_structure": "text_plus_evidence", "evidence_required": True, "external_knowledge_required": False, "relation_code": "paired_text", "documented_shift": None, "selector_training": True, "rules": False, "n_train_observed": len(texts)}))

    from huggingface_hub import model_info

    payload = {
        "freeze": "numerical fingerprint",
        "protocol": "FPS-1 measurements, FPS-2 candidate list",
        "numpy": np.__version__,
        "torch": torch.__version__,
        "tokenizer_revision": model_info(tok_name).sha,
        "encoder_revision": model_info(enc_name).sha,
        "median_rule": "even n: mean of the two central ranks; numpy percentile linear for the reported median and p95",
        "entropy": "nats divided by ln(K)",
        "tokenizer": tok_name,
        "encoder": enc_name,
        "candidates": rows,
    }
    (OUT / "fingerprint.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("wrote", OUT / "fingerprint.json")
    for row in rows:
        imb = row["imbalance"]
        ln = row["length"]
        print(row["candidate"], imb["n"], imb["k"], round(imb["normalized_entropy"], 4), round(ln["median_tokens"], 2), round(ln["p95_tokens"], 2))


if __name__ == "__main__":
    main()
