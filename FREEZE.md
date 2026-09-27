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
