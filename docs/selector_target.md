# Selector target

Freeze id: **ST-1**. Date: 2026-09-26.

EP-1, FPS-1, FPS-2, the numerical fingerprint, the schema manifest, and the D/G pin are not edited. No score is recomputed. No selector is fit. Novelty stays **MODIFY**.

This document defines what a later selector is accountable for. It does not choose a model, a loss, or a weight.

## Primary target

Formulation B is the training target. For each eligible task–primitive pair, the selector predicts the measured performance vector

\[
Y_{t,p} = (Q_{t,p},\ C^{\mathrm{train}}_{t,p},\ C^{\mathrm{infer}}_{t,p},\ C^{\mathrm{api}}_{t,p},\ L^{p50}_{t,p},\ L^{p95}_{t,p},\ V_{t,p})
\]

from the FPS-1 fingerprint of task \(t\) and the identity of primitive \(p\). The same fingerprint is used for every primitive on \(t\). The primitive identity says which slot is being predicted. It is not a score.

| Coordinate | Stored field | Unit | Better |
| --- | --- | --- | --- |
| \(Q\) | `Q_macro_f1` | macro-F1 on the frozen eval rows | higher |
| \(C^{\mathrm{train}}\) | `C_train_seconds` | seconds | lower |
| \(C^{\mathrm{infer}}\) | `C_infer_seconds` | seconds on the frozen eval rows | lower |
| \(C^{\mathrm{api}}\) | `C_api_usd` | dollars | lower |
| \(L^{p50}\) | `L_p50_ms` | milliseconds per example | lower |
| \(L^{p95}\) | `L_p95_ms` | milliseconds per example | lower |
| \(V\) | `invalid_outputs / n_eval` | share of eval rows | lower |

\(V\) is the invalid-output rate under the pin: after stripping whitespace and one matching pair of surrounding quotes, the output was not exactly one legal label. Those rows are already wrong inside \(Q\). \(V\) stays a separate coordinate because a legal wrong label and an output that is not a label are different failures, and \(Q\) does not say which one occurred.

The source rows are the 25 eligible pairs in `performance_matrix.md`. An ineligible pair has no target. The rule primitive is eligible on SMS Spam only. A missing coordinate is not filled with zero. A measured zero stays zero: training seconds for R, D, and G are 0 because those primitives were not fit on the task, and API dollars are 0 because no API was called.

## What is not the target

- A single primitive id, including \(\arg\max_p Q_{t,p}\).
- Accuracy. It remains stored beside \(Q\) and is not predicted.
- Model-load seconds. EP-1 keeps them outside \(L\).
- The device, the eval count, the benchmark name, and the dataset id. Eval count is the denominator of \(V\) and the scale of \(C^{\mathrm{infer}}\). It is not a feature and not a prediction.
- Any coordinate of \(Y\) for the task being predicted.
- A utility scalar. The three FPS-1 scenarios are applied after a vector is predicted. This freeze does not add a weight on \(V\), and it does not refit the FPS-1 weights to the matrix.

\(C^{\mathrm{infer}}\) is the total for that task's frozen eval set. PubMedQA has 500 eval rows and the other tasks have 1,000, so total inference seconds are comparable across primitives on one task and are not a per-decision cost. Per-decision latency is \(L^{p50}\) and \(L^{p95}\).

\(L\) and \(C^{\mathrm{infer}}\) were measured on the device recorded in the matrix. R, C, and D are CPU. G is the GTX 1650 Ti in float16. The target does not rescale those times onto one device.

\(C^{\mathrm{api}}\) is 0 on every measured pair. The coordinate stays. A constant is reported as a constant.

## How a choice is made

A scenario reads a complete predicted vector and then chooses. It is not the label the selector is trained to emit.

FPS-1 already names the only scenarios:

- Quality only: cost weight 0, latency weight 0.
- Equal weights after min-max normalization within a task.
- Cost and latency each weighted equally with quality.

Normalization constants, when a scenario needs them, come from selector-training tasks only. They are not taken from the task being scored, and they are not taken from ESCI.

The chosen primitive is reported with its full vector, including \(V\). A quality-only winner whose invalid rate is 1 remains the quality-only winner. The vector shows the contract failure. This freeze does not delete that primitive after the fact.

Pareto dominance, when reported, uses all seven coordinates: higher \(Q\), and lower cost, latency, and \(V\), with at least one strict difference. Dominance on this matrix is dominance on this measurement rig. It is not a hardware-neutral ranking.

Formulation A, a classifier of the winning primitive under one named scenario, is a second analysis. Its label is computed from the vector. It is not ST-1's training target.

## Rows a later fit may use

Selector-training targets are the eligible pairs on Banking77, CLINC150 plus, Civil Comments, SMS Spam, LEDGAR, PubMedQA fold 0, and VitaminC. That is 22 pairs: one rule, and C, D, and G on each of the seven tasks.

ESCI's three measured vectors stay in the matrix. They are not fitting rows. They remain the e-commerce holdout.

Features stay inside the FPS-1 registry. Test labels, test scores, and any primitive's \(Y\) on the task being predicted are excluded.

## What this freeze does not do

It does not fit a selector, choose a model class, transform a coordinate, run leave-one-family-out, or run leave-one-domain-out. Seven tasks and a rule on one of them still cannot support a generalization claim. The scarcity grid is still an intervention, not a feature and not a target.
