"""Render numerical_fingerprint_manifest.md from fingerprint.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
src = json.loads((ROOT / "data" / "fingerprint" / "fingerprint.json").read_text(encoding="utf-8"))
rows = src["candidates"]
if len(rows) != 8:
    raise SystemExit(f"expected 8 candidates, found {len(rows)}")

def fnum(x, nd=4):
    if x is None:
        return "undefined"
    if isinstance(x, float):
        return f"{x:.{nd}f}".rstrip("0").rstrip(".") if nd > 2 else f"{x:.{nd}f}"
    return str(x)

lines = []
lines.append("# Numerical fingerprint manifest")
lines.append("")
lines.append("Date: 2026-09-26. Generated from `research/data/fingerprint/fingerprint.json`.")
lines.append("")
lines.append("FPS-1 and FPS-2 are unchanged. The schema manifest is unchanged. This file is the measurement record.")
lines.append("")
lines.append("No primitive was run. Test files were not read, except that the official PubMedQA script's test half was counted and not tokenized.")
lines.append("")
lines.append(f"Tokenizer: `{src['tokenizer']}` revision `{src['tokenizer_revision']}`.")
lines.append(f"Label encoder: `{src['encoder']}` revision `{src['encoder_revision']}`.")
lines.append(f"Normalized entropy is Shannon entropy in nats divided by ln(K). {src['median_rule']}.")
lines.append("")
lines.append("Scopus was not searched. Semantic Scholar was not searched. Novelty remains **MODIFY**.")
lines.append("")
lines.append("ESCI is measured and held out of selector training. The scarcity grid is not in this table.")
lines.append("")
lines.append("| Candidate | Train rows | K | Norm. entropy | Max/min | Median tokens | P95 tokens | Mean label cosine | Min label cosine | Relation | Selector training |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |")
for c in rows:
    i, L, s, sim = c["imbalance"], c["length"], c["structural"], c["label_similarity"]
    ratio = "undefined" if i["max_min_ratio"] is None else f"{i['max_min_ratio']:.3f}"
    lines.append(
        "| {name} | {n} | {k} | {h:.4f} | {ratio} | {med:.1f} | {p95:.1f} | {mean:.4f} | {mn:.4f} | {rel} | {sel} |".format(
            name=c["candidate"],
            n=i["n"],
            k=i["k"],
            h=i["normalized_entropy"],
            ratio=ratio,
            med=L["median_tokens"],
            p95=L["p95_tokens"],
            mean=sim["mean_pairwise_cosine"],
            mn=sim["min_pairwise_cosine"],
            rel=s["relation_code"],
            sel="no" if not s["selector_training"] else "yes",
        )
    )
lines.append("")
lines.append("## Notes fixed before these numbers were used")
lines.append("")
lines.append("- Banking77's official CSV header is `text`, `category`. The loader calls the second field `label`. The category strings are the labels that were embedded.")
lines.append("- Civil Comments length uses 20,000 training rows drawn with `numpy` `default_rng(20260926)`. Imbalance uses all 1,804,874 training rows. Declared names for the thresholded classes are `nontoxic` and `toxic`.")
lines.append("- ESCI row identity and labels come from the official examples file: English (US), `large_version` 1, `split` train, 1,393,063 rows. Length uses 20,000 of those rows. Product title, description, and bullets for that sample were read from the tasksource copy of those three fields, keyed by product id and locale. The tasksource train split itself was not the row set.")
lines.append("- SMS training size is the 80 percent side. Indices are in `sms_train_indices.json`.")
lines.append("- PubMedQA fold 0 from `split_dataset.py` with `random.seed(0)` is 450 train, 50 dev, 500 test. PMIDs are in `pubmedqa_fold0_train_pmids.json`.")
lines.append("- VitaminC training rows are 370,653, matching Table 2. The article-grouped shift code stays blank.")
lines.append("- `schema_choice` has no candidate.")
lines.append("")
lines.append("## Structural codes")
lines.append("")
lines.append("| Candidate | Structure | Evidence | External knowledge | Documented shift | Rules |")
lines.append("| --- | --- | --- | --- | --- | --- |")
for c in rows:
    s = c["structural"]
    shift = s.get("documented_shift")
    shift_s = "blank" if shift is None else str(shift)
    lines.append(
        f"| {c['candidate']} | {s['input_structure']} | {s['evidence_required']} | {s['external_knowledge_required']} | {shift_s} | {s['rules']} |"
    )
lines.append("")
out = ROOT / "docs" / "numerical_fingerprint_manifest.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
