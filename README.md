# Task-Level Predictability for Heterogeneous Decision Primitives

**An eight-task pilot of task-level predictability for heterogeneous decision primitives**

[Paper PDF](paper/main.pdf) ·
[ORCID: Sudip Niroula](https://orcid.org/0009-0009-8886-114X) ·
[ORCID: Mandip Pokharel](https://orcid.org/0009-0000-9454-7012)

## Research status

**Status:** Frozen pilot / public research snapshot

The experiment is complete and the reported results are frozen. This repository accompanies the manuscript and supports inspection of the published analysis.

Future experiments, if any, should be treated as separate versions or follow-up studies rather than modifications of these frozen results.

## Overview

This repository contains the frozen research artifacts for an eight-task pilot study asking whether measurable properties of a bounded decision task, computed before primitive evaluation, can predict the quality and operational behavior of different computational primitives.

The evaluated primitive families are:

- deterministic rule
- conventional TF-IDF + logistic-regression classifier
- typed decision model (Laya)
- generative language model (Qwen2.5-0.5B-Instruct)

The study predicts a seven-coordinate performance profile:

- macro-F1
- local training time
- local inference time
- API cost
- p50 latency
- p95 latency
- invalid-output rate

## Main findings

In this frozen eight-task pilot:

- the task fingerprint was closer than the primitive-specific mean on macro-F1 for 5 of 8 held-out tasks;
- it was closer on invalid-output rate for 2 of 8 tasks;
- all vector-based policies selected the conventional classifier on every held-out task;
- on the ESCI e-commerce holdout, macro-F1 prediction error decreased from 0.2825 to 0.1024 and invalid-rate error from 0.1199 to 0.0444, without changing the selected primitive;
- Qwen's invalid-output rate ranged from 0.023 to 1.000 across the evaluated tasks.

## Interpretation

This repository does not present a validated routing system.

The experiment found substantial task-dependent variation among the evaluated implementations, but the frozen fingerprint did not reliably improve prediction over the primitive-specific training-fold mean.

The study therefore should be read as a measurement pilot rather than as evidence that task fingerprints are generally predictive.

The repository also does not claim that the classifier is universally best, that the reported latencies are hardware-normalized, or that one Laya checkpoint or one Qwen checkpoint represents its model family.

## Repository contents

| Path | Purpose |
| --- | --- |
| `paper/` | Manuscript, LaTeX source, and frozen figures |
| `results/raw/` | Frozen measured scores, selector output, and evaluation-row indices |
| `data/fingerprint/` | Public task fingerprint and training-row identifiers |
| `src/` | Measurement and selector source code |
| `configs/` | Frozen SMS rule |
| `docs/` | Dataset, protocol, pin, and reproducibility documentation |
| `scripts/` | Figure redraw and snapshot verification |

`results/raw/` keeps that name because `src/selector/fit_sd1.py` and `src/primitives/measure_p0_p1.py` resolve it. These files are frozen derived results, not a dump of benchmark text. Renaming the directory would require editing those scientific scripts, so the path is unchanged.

## Data availability

Raw benchmark texts are not redistributed in this repository.

The experiments use publicly available benchmark datasets obtained from their respective official sources. Users must obtain those datasets independently and comply with their applicable licenses and terms.

This repository contains derived task-level artifacts such as fingerprints, indices, measured scores, counts, latencies, and configuration information, subject to the exclusions documented in `LICENSES.md`.

Dataset sources, splits, transformations, and the C100k cap are in [docs/datasets.md](docs/datasets.md).

## Hardware and runtime conditions

The frozen measurements were produced under the following conditions:

| Primitive | Device |
| --- | --- |
| Rule | CPU |
| TF-IDF + logistic regression | CPU |
| Laya | CPU |
| Qwen2.5-0.5B-Instruct | NVIDIA GTX 1650 Ti, float16 |

Latency excludes model-load time.

These measurements are deployment-specific and are not intended as hardware-normalized comparisons of intrinsic primitive speed.

API cost is zero because no API was called.

## Inspect the published analysis

```bash
python scripts/verify_snapshot.py
```

That command checks repository integrity. It does not recompute scores.

Redrawing Figures 1–5 needs matplotlib and numpy:

```bash
pip install -r requirements-figures.txt
python scripts/make_figures.py
```

`scripts/make_figures.py` redraws Figures 1–5 from the frozen JSON artifacts. It does not refit the selector or rerun any primitive.

Re-running the full measurement requires obtaining the original datasets and satisfying their licenses and preprocessing requirements. That is not the default command.

The manuscript is [paper/main.pdf](paper/main.pdf). The public repository is https://github.com/imsudip45/task-level-predictability. No DOI is assigned.

## Licenses

MIT applies to source code and scripts only. The manuscript, documentation, figures, and derived research artifacts are CC BY 4.0. Datasets, Qwen, Laya, and tokenizers keep their own licenses. See [LICENSES.md](LICENSES.md).

## Citation

See [CITATION.cff](CITATION.cff). Version 1.0.0, released 2026-09-27. The experiment freeze date is 2026-09-26.

Sudip Niroula and Mandip Pokharel. *An eight-task pilot of task-level predictability for heterogeneous decision primitives.* 2026.
