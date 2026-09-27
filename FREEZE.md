# Frozen Research Snapshot

This repository is a public snapshot of the experiment identified by:

- FPS-1
- FPS-2
- EP-1
- ST-1
- SD-1

Freeze date: 2026-09-26

## Freeze policy

The published numerical results are copied from the frozen experiment. They are not recomputed during repository preparation.

No selector hyperparameter was retuned after observing the predictive results.

No primitive was rerun to improve its result.

No additional interaction terms were added after observing Table 4.

No additional experiment is required to interpret this snapshot.

The copied scores remain at `results/raw/` because the measurement and selector scripts resolve that directory. `scripts/verify_snapshot.py` checks those bytes. It does not refit the selector.

## Manuscript release

Git tag `paper-v1.0` is the repository state prepared for the arXiv submission. It identifies the final PDF, LaTeX source, figures, frozen results, and documentation together.

The experiment freeze date stays 2026-09-26. This tag does not refit the selector, rerun a primitive, or change a reported number.

Commits before `paper-v1.0` are development history. The tag is the release that produced the paper.
