# Selector fit under SD-1

Date: 2026-09-26. The fit is `src/selector/fit_sd1.py`. The numbers are `results/raw/selector_sd1.json`.

ST-1 and SD-1 were not edited. No primitive was rerun. The rule, the classifier, and Laya stay on CPU. Qwen stays on the GTX 1650 Ti in float16. Latency is the latency of that deployment. It is not a hardware-normalized comparison. Novelty stays **MODIFY**.

Standardization uses the population standard deviation of the training tasks in that fit. A zero-variance column is set to zero. `Ridge(alpha=1.0)` was not searched.

## What the fit can support

Seven selector-training tasks do not support a generalization claim. The question this fit can answer is whether the frozen fingerprint reduces held-out absolute error relative to the primitive mean, one coordinate at a time, and whether that changes a later policy.

## Vector error

Each cell is the mean absolute error across the eligible primitives both predictors could fill. A negative difference means the ridge prediction was closer. API dollars are 0 for both predictors on every task, so that coordinate is a tie at error 0. It is not a success.

| Holdout | Task | Q ridge | Q mean | V ridge | V mean |
| --- | --- | ---: | ---: | ---: | ---: |
| Intent | Banking77 | 0.2112 | 0.1090 | 0.1713 | 0.0725 |
| Intent | CLINC150 plus | 0.1623 | 0.1232 | 0.2483 | 0.1495 |
| Verification | PubMedQA | 0.2583 | 0.2785 | 0.0792 | 0.0420 |
| Verification | VitaminC | 0.2096 | 0.2688 | 0.2839 | 0.1503 |
| Moderation | Civil Comments | 0.2075 | 0.1880 | 0.3333 | 0.2366 |
| Security | SMS Spam | 0.2271 | 0.2619 | 0.2832 | 0.1426 |
| Business / legal | LEDGAR | 0.1562 | 0.1684 | 0.1131 | 0.1188 |
| E-commerce | ESCI | 0.1024 | 0.2825 | 0.0444 | 0.1199 |

On macro-F1 the ridge error is smaller on five tasks and larger on three: both intent tasks and Civil Comments. On the invalid rate the ridge error is smaller on two tasks, LEDGAR and ESCI, and larger on the other six.

The three tasks where Qwen's invalid rate is extreme are predicted in the wrong direction. Held-out Qwen validity was 0.514 on Banking77, 0.745 on CLINC150 plus, and 1 on Civil Comments. The ridge predictions were −0.009, −0.073, and −0.039 before the unit-interval clip, and 0 after it. The primitive mean predicted about 0.29 on the intent tasks and 0.29 on Civil Comments. The mean is closer because it keeps the average Qwen failure. The fingerprint shift removes it.

On the fit that uses all seven selector-training tasks, the largest macro-F1 coefficients are the primitive indicators: Qwen −0.385 and Laya −0.134, against an intercept of 0.593. The largest fingerprint coefficient on that coordinate is normalized entropy, −0.065. The invalid-rate model is the same shape: the Qwen indicator is +0.306 and the largest fingerprint coefficient is mean label cosine, +0.113. The fingerprint is a small shared shift. Invalid outputs in this matrix belong to Qwen. A shift applied to every primitive cannot raise Qwen's invalid rate without also raising the classifier and Laya, whose invalid rates are 0. The frozen design has no product between a fingerprint column and a primitive indicator.

The verification holdout removes both `paired_text` training tasks. The relation bit then has no variance, and that column is zeroed. The structural feature that distinguishes the held-out family is absent from that fit.

Median-latency error is smaller for the ridge model on four tasks and smaller for the mean on four. Those errors are hundreds of milliseconds. They describe the recorded execution environment. They do not establish which primitive is intrinsically faster, and they are not why macro-F1 and validity fail. Those two coordinates do not depend on moving the classifier or Laya onto the GPU.

Training-seconds error at task level includes the definitional zeros for the rule, Laya, and Qwen. The classifier-only training-seconds errors are in the JSON under `C_train_classifier_only`.

## Policies

On every held-out task, and on all four vector policies, the ridge vector and the primitive mean selected the same primitive. That primitive was the classifier.

The measured oracle, using the same rules on the measured vector, also selects the classifier except in three cases:

- Highest macro-F1 on PubMedQA selects Laya. Measured macro-F1 is 0.3128 for Laya and 0.2691 for the classifier.
- Highest macro-F1 on Civil Comments selects Laya. Measured macro-F1 is 0.7367 for Laya and 0.6298 for the classifier.
- Lowest median latency on SMS Spam selects the rule, at 0.020 ms against the classifier's 0.188 ms. The security holdout has no rule row in training, so neither predictor offers a rule. The fold records the rule slot as unpredictable.

Equal weights and shared weights select the classifier on every task, including the oracle. After min-max scaling on the training tasks, Laya's latency occupies the top of the range. The gap between the rule and the classifier is negligible beside it, and the classifier has higher macro-F1 on SMS Spam.

ESCI is the domain holdout. Ridge reduced macro-F1 error from 0.2825 to 0.1024 and invalid-rate error from 0.1199 to 0.0444. Every vector policy still selects the classifier, which is also the oracle's selection. The closer vector did not change the decision.

## Frozen reading

This section freezes the interpretation. It does not change a score, a coefficient, a holdout, or SD-1. A fingerprint-by-primitive product is not added. Ridge is not retuned. No primitive is rerun.

The result is narrower than the original hypothesis. With these seven training tasks and this frozen fingerprint, the fingerprint did not carry enough transferable information to beat the primitive mean consistently, and it never changed the downstream primitive relative to that mean.

Prediction accuracy is not decision usefulness. Ridge reduced error on some coordinates and some tasks. Under every vector policy it still selected the classifier, which is what the primitive mean selected. The measured oracle differs in only the three cases already listed. ESCI is not evidence that the selector generalized to e-commerce. On that domain holdout the fingerprint model reduced macro-F1 error from 0.2825 to 0.1024 and invalid-rate error from 0.1199 to 0.0444, and the downstream primitive stayed the classifier, which was also the oracle's selection.

The verification holdout is a feature-coverage fact. Removing PubMedQA and VitaminC removes every `paired_text` training task, so that bit is zeroed. The fit cannot use a structural property that the training fold does not contain. That is separate from ridge being a weak function class.

SD-1 has no fingerprint-by-primitive interaction. A fingerprint fact that means "Qwen behaves differently on this kind of task" cannot be expressed. The shared shift moves every primitive together. That limitation is recorded. It is not repaired in this experiment.

What this pilot establishes:

- The measured matrix shows that the four primitives do not behave alike across these tasks.
- Qwen's invalid rate is its own outcome. It runs from 0.023 on VitaminC and 0.025 on SMS Spam to 1 on Civil Comments.
- The pre-specified shared-shift ridge model does not reliably beat the primitive mean at this sample size.
- Where the vector was closer, the primitive chosen by the frozen policies did not change.

What this pilot does not establish:

- That a task fingerprint cannot predict primitive performance. Seven training tasks cannot support that claim.
- That the classifier is universally best. The oracle selects Laya on PubMedQA and Civil Comments, and the rule on SMS Spam under lowest median latency.
- That the CPU/GPU split caused the selector result. Macro-F1 and the invalid rate do not depend on that split.

FPS-1 already classed eight tasks as a measurement drill, not as evidence that a fingerprint generalizes. Three of the five selector-training families contain one task, so those family holdouts are single-task holdouts. The stage of the work is a completed pilot. It is not a publishable answer to the question of whether task fingerprints predict primitive behavior on unseen families. Novelty stays **MODIFY**. Scopus was not searched. Semantic Scholar was not searched.
