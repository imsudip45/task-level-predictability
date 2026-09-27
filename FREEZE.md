# Freeze

This snapshot records the measurement frozen on 26 September 2026. It does not refit the selector and it does not rerun primitives to improve results.

| Identifier | What it freezes |
| --- | --- |
| FPS-1 | Fingerprint measurement rules |
| FPS-2 | Candidate list after BFCL-simple was removed |
| EP-1 | Evaluation protocol: rows, metrics, classifier, SMS rule |
| ST-1 | Selector target |
| SD-1 | Selector design and the fitted ridge result in `results/raw/selector_sd1.json` |

The public copy is a reproduction package for that freeze. Scores in `results/raw/` are the copied outputs. `scripts/verify_snapshot.py` checks that those bytes are intact. It does not recompute them.
