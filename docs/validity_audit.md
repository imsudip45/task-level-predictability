# Validity audit of the primitive scores

Date: 2026-09-26. No new model was run. No selector was fit.

## What was saved

R, C, and D produced zero invalid outputs on every scored task. Their macro-F1 is a score over legal labels.

G did not. Invalid means the stripped output was not exactly one label from that task's legal set. Those rows are wrong for macro-F1, and the count is stored separately.

| Task | G invalid / eval | Share invalid |
| --- | ---: | ---: |
| SMS Spam | 25 / 1,000 | 0.025 |
| PubMedQA fold 0 | 174 / 500 | 0.348 |
| Banking77 | 514 / 1,000 | 0.514 |
| CLINC150 plus | 745 / 1,000 | 0.745 |
| LEDGAR | 86 / 1,000 | 0.086 |
| Civil Comments | 1,000 / 1,000 | 1.000 |
| VitaminC | 23 / 1,000 | 0.023 |
| ESCI | 32 / 1,000 | 0.032 |

Civil Comments macro-F1 is 0 because every output was invalid. That is a measured failure of the one-label rule, not a hand-entered zero.

The invalid strings themselves were not saved. This audit cannot say whether Qwen emitted explanations, extra words, or the wrong label spelling. A later pass can store the raw strings. It should not change the pin in order to raise the score.

## What this does to Q

On Banking77 and CLINC150 plus, most of G's errors are invalid outputs. Macro-F1 there is mostly a parse result. On SMS, VitaminC, and ESCI, invalids are rare, so macro-F1 is mostly the legal predictions. Those two situations should not be averaged into one "G quality" number without the invalid rate beside it.

## What this does to L and C

R, C, and D latencies are CPU. G latencies are the GTX 1650 Ti in float16. A smaller G latency is not evidence that the generative model is cheaper in general. API dollars are 0 for every pair because no API was called. Training seconds for R, D, and G are 0 because those primitives were not fit on the task. Cfull and C100k training seconds are the only non-zero training costs.

## Selector

A selector is not fit in this audit. Seven selector-training tasks remain. G's quality is not comparable across tasks until the invalid rate is part of the vector. ESCI stays out of selector training.
