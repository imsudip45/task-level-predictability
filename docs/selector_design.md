# Selector design

Freeze id: **SD-1**. Date: 2026-09-26.

ST-1 is frozen and is not edited. The target remains

\[
Y_{t,p} = (Q,\ C^{\mathrm{train}},\ C^{\mathrm{infer}},\ C^{\mathrm{api}},\ L^{p50},\ L^{p95},\ V)
\]

EP-1, FPS-1, FPS-2, the numerical fingerprint, the schema manifest, and the D/G pin are not edited. No selector is fit. Novelty stays **MODIFY**.

The model answers: given the FPS-1 fingerprint and a primitive identity, what measured behavior does that primitive have on that task? A later scenario may read those predictions. The scenario is not the training label.

## Learned model

One model class. Seven separate ridge regressions, one per coordinate, so the unit of latency cannot dominate the fit of macro-F1 or the invalid rate. There is no joint loss and no weight among coordinates.

Each regression is `Ridge(alpha=1.0)` with an intercept, after the numeric fingerprint columns are standardized. The penalty is fixed here. It is not searched. Primitive indicators are not standardized.

Standardization uses the tasks in that fit only. The held-out task, and ESCI, do not enter the means or the scales. A scale of zero leaves that column at zero.

Predictions are returned in the original units. \(Q\) and \(V\) are then clipped to \([0,1]\). Training seconds, inference seconds, and both latencies are clipped at 0. Those bounds are the bounds of the measurements. They are not thresholds chosen from the matrix.

No product between a fingerprint column and a primitive indicator. The fingerprint shifts every primitive alike. The primitive indicator is an intercept shift from the classifier.

### Rows

A fit uses eligible pairs from the tasks designated as its training tasks. ESCI is never one of those tasks. The rule row exists only when SMS Spam is in the training tasks.

### Features

Numeric columns, in this order, from the frozen fingerprint only:

- \(\log_{10}\) of training rows
- \(\log_{10}\) of \(K\)
- normalized entropy
- \(\log_{10}\) of the max/min class count
- \(\log_{10}\) of the minimum rows per class
- \(\log_{10}\) of the median rows per class
- \(\log_{10}\) of the median WordPiece length
- \(\log_{10}\) of the P95 WordPiece length
- mean label-name cosine
- minimum label-name cosine
- 1 if the relation code is `paired_text`, otherwise 0

The logarithms are there because those fingerprint columns already span orders of magnitude. Entropy and the cosines stay as recorded. The same transform is used for every task.

Primitive identity is an indicator, with the classifier as the reference level. Indicators for the decision model, the generative model, and the rule are included only when that primitive has at least one training row in the fit.

Columns that are not features:

- External knowledge is false on every candidate.
- Input structure and evidence required make the same split of these candidates as the relation code. The relation bit is the one that enters.
- Documented shift is `unspecified` on four selector-training tasks and blank on VitaminC. It stays in the fingerprint record and does not enter the fit.
- The rules flag is true only on SMS Spam. The primitive mask already decides eligibility. The flag is not a feature.
- Family name, dataset id, benchmark name, device, and eval count are not features.
- No coordinate of \(Y\) is a feature.

### Two coordinates that are not regressions

API dollars are 0 on every measured pair. That coordinate is predicted as 0. It is not passed through ridge.

R, D, and G are not fit on the task. Their training seconds are predicted as 0 from that definition. The training-seconds regression is fit only on classifier rows.

### When a primitive was not seen

If the training tasks contain no row for a primitive, that fit has no coefficient for it. The model does not copy another primitive's prediction. On the security-family holdout, SMS Spam is absent, so the rule slot is unpredictable. The fold records that fact.

## Vector baseline

The null predictor ignores the fingerprint. For each primitive that appears in the training tasks, it predicts the arithmetic mean of that primitive's measured coordinate on those tasks. The same definitional zeros apply to API dollars and to training seconds of R, D, and G. An unseen primitive is not predicted.

The learned model is useful only if it reduces held-out error against this mean, coordinate by coordinate. A single summed score is not the comparison.

## What is scored first

On each held-out task, for each coordinate, absolute error of the learned prediction and of the primitive mean, on every eligible pair that both predictors can fill. The task-level number is the mean of those absolute errors across the eligible primitives. The seven coordinates stay separate. ESCI is scored the same way, after one fit on all 22 selector-training pairs.

## Policies

Policies run after a vector exists. They are not training labels. Always-G, always-C, always-D, and the mask default do not read a vector. The mask default selects the rule when it is eligible and the classifier otherwise.

The other four policies read a vector from the learned model, from the primitive mean, or from the measured vector. The measured vector is an oracle reference. It is not a predictor.

- Highest macro-F1.
- Lowest latency p50.
- Equal weights: \(U = \tilde{Q} - \tilde{C}^{\mathrm{infer}} - \tilde{L}^{p50}\).
- Shared weights: \(U = \tilde{Q} - \tfrac{1}{2}\tilde{C}^{\mathrm{infer}} - \tfrac{1}{2}\tilde{L}^{p50}\).

\(\tilde{Q}\), \(\tilde{C}^{\mathrm{infer}}\), and \(\tilde{L}^{p50}\) are min-max scaled with the minimum and maximum of the measured coordinate on the training tasks of that fit. The held-out task does not supply those constants. ESCI does not supply them. A zero range makes that term 0. A value outside the training range is left outside it.

FPS-1 names min-max within a task. ST-1 forbids taking the constants from the task being scored. The choice is still among the primitives on one task. The constants follow ST-1.

Latency p50 is the per-decision cost these policies read. API dollars do not vary. Training seconds are zero for every primitive that is not the classifier. Inference seconds remain in the vector and in the equal-weight and shared-weight utilities. The invalid rate is not given a weight. The chosen primitive is reported with its measured vector, including \(V\).

Ties break in the order rule, classifier, decision model, generative model.

A policy that reads a vector may select only a primitive whose vector was predicted. Always-C, always-D, and always-G ignore that restriction because they name one eligible primitive.

The outcome of a policy is the measured vector of the primitive it selected. That vector is reported next to the measured vector of the primitive the same policy selects from the oracle. Those two vectors are not collapsed into one regret.

## Holdouts

Family labels are the Family column already written in `dataset_screening.md`. They are not features.

| Holdout | Tasks removed together | Training tasks that remain |
| --- | --- | --- |
| Intent | Banking77, CLINC150 plus | Civil Comments, SMS Spam, LEDGAR, PubMedQA, VitaminC |
| Verification | PubMedQA, VitaminC | Banking77, CLINC150 plus, Civil Comments, SMS Spam, LEDGAR |
| Moderation | Civil Comments | the other six |
| Security | SMS Spam | the other six |
| Business / legal | LEDGAR | the other six |
| E-commerce | ESCI | all seven selector-training tasks |

ESCI is the e-commerce holdout. It is measured, and it is absent from every fit, every primitive mean, every standardization, and every utility range. A random 70/15/15 split of tasks is not run. Seven tasks do not fill those fractions.

## What this freeze does not do

It does not fit the ridge models, compute the primitive means, or apply the policies. Seven tasks and a rule on one of them still cannot support a generalization claim. The scarcity grid remains an intervention.
