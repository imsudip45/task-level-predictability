# Reproducibility

This page is the public map of the freeze. It does not recompute scores.

## Identifiers

FPS-1, FPS-2, EP-1, ST-1, and SD-1. Freeze date: 2026-09-26. See `FREEZE.md`.

## What to run first

```bash
python scripts/verify_snapshot.py
```

The check confirms the copied files, the SMS rule hash, JSON parsing, freeze identifiers, and the absence of benchmark-text fields in the public JSON. It does not refit the selector.

## Figures

```bash
pip install -r requirements-figures.txt
python scripts/make_figures.py
```

`scripts/make_figures.py` redraws Figures 1–5 from `results/raw/`. It writes `paper/latex/figures/` and copies those PDF bytes to `paper/figures/`. It does not refit the selector or rerun any primitive.

## Frozen outputs

| Artifact | Path |
| --- | --- |
| Rule and classifier scores | `results/raw/performance_p0_p1.json` |
| Laya and Qwen scores | `results/raw/performance_dg.json` |
| Selector fit | `results/raw/selector_sd1.json` |
| Evaluation-row indices | `results/raw/*_eval_indices.json` |
| Task fingerprint | `data/fingerprint/fingerprint.json` |
| SMS training indices | `data/fingerprint/sms_train_indices.json` |
| PubMedQA fold-0 training PMIDs | `data/fingerprint/pubmedqa_fold0_train_pmids.json` |
| SMS rule | `configs/sms_rule.txt` |

The directory is `results/raw/` because the selector and primitive scripts resolve that path. The files are frozen derived results.

## Protocol records

The manuscript names these records. They are copied here unchanged:

- `docs/numerical_fingerprint_manifest.md`
- `docs/performance_matrix.md`
- `docs/selector_results.md`
- `docs/selector_target.md`
- `docs/selector_design.md`
- `docs/evaluation_protocol.md`
- `docs/task_fingerprint_spec.md`
- `docs/primitive_pins.md`
- `docs/validity_audit.md`
- `docs/datasets.md`

## Full measurement

Re-running the primitives requires the original datasets, their licenses, and the preprocessing stated in `docs/datasets.md` and `docs/evaluation_protocol.md`. Raw text is not in this repository. A full rerun is not the default command.

The SMS rule SHA-256, including the trailing newline, is `264e288b89a430005de7b72fdfeb77862e46b23b7415c76df285e4e5e1a7f992`.
