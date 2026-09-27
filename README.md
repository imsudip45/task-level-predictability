# Task-level predictability

Can a static fingerprint of a task predict which decision primitive will be closer on quality and on invalid outputs, before that primitive is run on the task?

This repository is the frozen eight-task pilot. The primitives are a written SMS rule, a TF-IDF logistic-regression classifier, Laya, and Qwen2.5-0.5B-Instruct. The selector is a ridge model fit under SD-1. ESCI is scored and is held out of every selector fit.

On the held-out tasks, the ridge predictor was closer than the training-fold mean on macro-F1 for 5 of 8 tasks, and closer on the invalid rate for 2 of 8 tasks. The classifier was the primitive selected on every held-out task. On ESCI, ridge reduced macro-F1 error from 0.2825 to 0.1024 and invalid-rate error from 0.1199 to 0.0444, and the selected primitive stayed the classifier.

## What this repository does not claim

- Task fingerprints are generally predictive.
- The classifier is universally best.
- The experiment is a validated routing system.
- The reported latencies are hardware-normalized.
- One Laya checkpoint or one Qwen checkpoint represents its model family.

## Hardware

The rule, the classifier, and Laya ran on CPU. Qwen ran in float16 on a GTX 1650 Ti.

## Repository

https://github.com/imsudip45/task-level-predictability

No DOI is assigned.

## Layout

| Path | Contents |
| --- | --- |
| `paper/main.pdf` | Built manuscript |
| `paper/latex/` | LaTeX sources and the five figure PDFs |
| `paper/figures/` | The same figure bytes |
| `results/raw/` | Frozen performance JSON, selector JSON, and evaluation-row indices |
| `data/fingerprint/` | Frozen fingerprint and training-row identifiers |
| `src/` | Selector fit, primitive measurement, and fingerprint code |
| `configs/sms_rule.txt` | Frozen SMS rule |
| `docs/` | Protocol records and dataset sources |
| `scripts/verify_snapshot.py` | Integrity check |
| `scripts/make_figures.py` | Redraws figures from `results/raw/` |

## Check the snapshot

```bash
python scripts/verify_snapshot.py
```

That script checks files, hashes, JSON, and freeze identifiers. It does not recompute scores.

Redrawing the figures needs matplotlib and numpy:

```bash
pip install -r requirements-figures.txt
python scripts/make_figures.py
```

`scripts/make_figures.py` reads `results/raw/` and writes `paper/latex/figures/`, then copies those PDF bytes to `paper/figures/`. It does not refit the selector and it does not run inference.

Full primitive reruns need the original datasets and are not the default command. Raw benchmark text is not in this repository. See `docs/datasets.md`.

## Licenses

MIT applies to source code and scripts only. The paper, documentation, figures, and derived research artifacts are CC BY 4.0. Datasets, Qwen, Laya, and tokenizers keep their own licenses. See `LICENSES.md`.

## Citation

See `CITATION.cff`. Version 1.0.0, released 2026-09-26.

Sudip Niroula and Mandip Pokharel. *An eight-task pilot of task-level predictability for heterogeneous decision primitives.* 2026.
