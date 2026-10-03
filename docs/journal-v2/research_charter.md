# Journal V2 research charter

Status: Design charter for review; not a completed preregistration or experimental result.
Date: 2026-10-03.
Audit reference: commit 6ace961fd93df746f33663fa89395ea65080a221.

## 1. Purpose and continuity

Preserve the original scientific focus: task-level predictability of heterogeneous bounded-decision systems. System selection is a downstream test of prediction value, not a replacement topic. No production application or cloud deployment is required; evaluation is offline. Preserve paper-v1.0 as the historical pilot. Do not reinterpret pilot results as confirmatory evidence for this study.

Primary scientific question: How well can task characteristics available before candidate evaluation predict quality and operational behavior across heterogeneous bounded-decision systems on unseen task groups?

Decision-value question: Do those predictions improve system choice compared with fixed defaults and simple task-based heuristics?

## 2. Scope and units

Restrict the study to text inputs requiring exactly one categorical decision from a known finite label set. Exclude open-ended generation, multilabel prediction, and token-level labeling from confirmatory scope.

A task comprises a source dataset, label definition, permitted training information, and evaluation protocol. A candidate is a complete pipeline, including preprocessing, training or prompting policy, decoding, output adapter, and failure handling; it is not merely a model name.

System families to represent conceptually are classical classifiers, fine-tuned encoders, and generative language models, with constrained and unconstrained output mechanisms distinguished. Deterministic heuristics are comparison candidates where applicable. Specific systems and portfolio size remain undecided.

A task group comprises datasets sharing a base corpus, derived variants, or identified substantial source overlap. Group membership must be established before outcome-based selection. Report nominal tasks and independent source groups separately; grouping reduces leakage but does not prove statistical independence.

The selector makes one candidate choice per task and operating scenario. Query-level routing is a distinct decision problem, not interchangeable with this primary track.

## 3. Information boundary

For the primary track, task descriptors may use only explicitly permitted training data, label descriptions, and scenario metadata. Labeled training examples may be available; this is not a claim of zero-label learning. Candidate performance on the new task, candidate predictions on its evaluation examples, and evaluation labels are unavailable to the selector.

No portfolio candidate may be run on the new task to generate selector inputs in the primary track. Any future landmarking or probing track must be separately specified, budgeted, and reported.

The researcher evaluates candidates to construct benchmark outcomes, but hides held-out outcomes from selector fitting and selection. Candidate adaptation occurs only after selection conceptually and uses its permitted training split. Benchmark execution may evaluate every candidate for scoring without exposing those results to the selector.

## 4. Outcome definitions

Quality: predictive performance on all designated evaluation examples under a prespecified metric and failure policy. Invalid or missing outputs must not be silently discarded. Conditional performance on valid outputs may be diagnostic only.

Contract failure: inability to emit exactly one permitted label in the required representation under the specified output and failure policy. Separate raw output compliance, adapter transformations, and end-to-end successful delivery. A valid but incorrect label is a quality error, not a contract violation. Record exceptions, refusals, and timeouts separately as well as their specified end-to-end treatment.

Latency: elapsed time to obtain a usable decision under a fixed measurement scenario. Separate setup/training time from inference time; specify batching, concurrency, warm-up, retries, and timeout handling later.

Cost: documented resource or monetary expenditure under a stated accounting boundary. Local computation is not automatically zero cost. Keep setup, adaptation, descriptor extraction, selector inference, and per-decision costs distinguishable.

Operational outcomes are conditional on the later-fixed hardware, software, provider, and workload scenario. Task descriptors alone do not imply hardware-independent latency or price predictions.

## 5. Estimands

Scientific estimand: held-out group-average prediction loss for each outcome and its paired difference against a training-only outcome-prediction baseline. Lower loss is better. Outcome-specific losses and numerical decision thresholds must be fixed before confirmatory evaluation. Do not combine unlike prediction losses into an arbitrary overall score.

Decision estimand: for a later-prespecified scenario objective J to maximize, define R(t,s) = max over eligible candidates a of J(t,a,s) minus J(t,selected,s). This is hindsight benchmark regret, not guaranteed population-optimal regret. Report uncertainty from finite measurements.

For baseline b, define Delta_b as the group-weighted average of R_b minus R_selector. Positive Delta_b indicates reduced regret. Average within each group first, then equally across groups, unless a different weighting target is justified and frozen in advance. Text-example count must not determine group weight by accident.

Selection must use predicted or permitted quantities, never realized test feasibility. When constraints apply, report realized constraint violations separately from regret. Do not silently exclude infeasible choices or tasks with no feasible candidate. The scoring and fallback rules for those cases must be resolved before experiments.

No utility weights, resource thresholds, deployment volumes, or feasibility penalties are chosen here. If total economic benefit is claimed, include selection and adaptation overhead within a prespecified accounting horizon.

## 6. Contribution hierarchy and hypotheses

Primary contribution: an auditable benchmark and evaluation framework for cross-family task-level outcome predictability.
Secondary contribution: empirical evidence about the conditions under which predictions improve system selection or fail to improve it.
Supporting contribution: reproducible measurements, grouped partitions, and failure analyses.
No algorithmic novelty is claimed merely for fitting a standard predictor or selector.

H1: task-conditioned predictions improve prespecified out-of-group prediction losses over simple training-only baselines. Test outcomes separately.
H2: prediction-informed selection reduces prespecified regret against the training-selected static baseline.
H3: contract-failure prediction supplies incremental decision information beyond quality and operational predictions. Test with a matched ablation only if failure variation permits informative evaluation.
These are testable propositions, not promised findings. Cross-family oracle variation and near-constant contract validity are reported as diagnostics, not used to cherry-pick tasks.

## 7. Baselines and evaluation safeguards

Required comparison classes: training-only constant or candidate-specific outcome predictors; a single candidate selected on training groups only; simple metadata-based selection rules; and outcome/feature ablations. Exact implementations remain undecided. The hindsight oracle is an upper-bound reference, not an executable competitor.

All related source variants stay together in outer partitions. All selector tuning, feature selection, preprocessing learned across tasks, and baseline tuning use inner training groups only. Candidate fitting and prompt construction respect within-task training/evaluation separation. Never choose the single-best baseline using outer-test outcomes.

Report paired group-level effects and uncertainty. Do not treat individual text examples, repeated seeds, or outer folds as additional independent tasks. Specify resampling, seed aggregation, interval methods, multiplicity handling, and missing-run policies before confirmatory evaluation.

Compare task-level and query-level approaches only in a separately specified extension with matched information, accounting, and objectives. Do not claim task-level superiority without that comparison.

## 8. Interpretation and claim boundaries

Positive evidence requires improvement against the prespecified baselines, uncertainty compatible with the stated conclusion, and operational violations accounted for. A numerical improvement alone does not establish practical importance.

A precise null or negative result is a valid boundary finding. Wide uncertainty is inconclusive, not proof that prediction cannot work. Near-zero validity variation limits the validity-prediction claim. A dominant static candidate limits evidence for selection value. Do not change the portfolio, task inclusion, or success definition after inspecting held-out outcomes to manufacture a positive result.

Bound conclusions to the measured portfolio, task groups, information boundary, and operational scenarios. Do not claim universal superiority, the first algorithm selector, the first text-dataset recommender, or proven universal novelty. The audit supports a bounded gap assessment, not proof of absent prior work. Treat shared-source concerns in prior studies as motivations for safeguards, not independently proven misconduct or leakage.

## 9. Deferred decisions and freeze gate

Still undecided: datasets, specific models, fingerprints, utility weights, hardware, provider, sample size, venue, exact quality metrics, prediction losses, practical-effect thresholds, confidence levels, and experimental implementation.

Before confirmatory runs, freeze a complete protocol resolving all those decisions plus task grouping, information permissions, baseline implementations, scenario objectives, infeasible/no-feasible cases, timeout and retry rules, accounting horizons, candidate adaptation budgets, and analysis methods. Separate exploratory feasibility work from confirmatory held-out evaluation and document access to any exploratory outcomes.

Sample size must follow group-level precision, feasibility, and resource analysis rather than a fixed arbitrary task count.

## 10. Change and review status

This document adds design guidance only. It does not authorize experiments, downloads, manuscript rewrites, merging to main, or modifying frozen pilot or novelty-audit files.

Drafted by the assistant with conceptual self-review. No independent scientific review or repository test execution is claimed. No datasets or model checkpoints were downloaded and no experiments were run in preparing this charter.
