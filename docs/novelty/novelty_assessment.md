# Novelty Assessment

## A. Established ideas
The following ideas are clearly not novel and are well-supported by prior work:
- **Algorithm selection from problem features:** Established since Rice (1976); comprehensively surveyed by Smith-Miles (2009) and Vanschoren (2018).
- **Dataset meta-features for model recommendation:** Standard in AutoML (Auto-WEKA, auto-sklearn); extended to text by PsyMatrix (Monteiro et al., 2024).
- **Model-performance prediction from dataset properties:** Addressed by ModelLens (Cai et al., 2026) at massive scale (47K models, 9.6K datasets).
- **Text-dataset model recommendation:** PsyMatrix uses psycholinguistic features across 146 text-classification datasets and 24 PLMs.
- **LLM routing:** Crowded area with multiple benchmarks (RouterBench, LLMRouterBench, RouterArena) and methods (FrugalGPT, RouteLLM, Hybrid LLM).
- **Cost-aware routing:** Addressed by nearly all recent LLM routing papers.
- **Constrained decoding for output validity:** Established method for enforcing structure (Lazy-k, Koa, grammar-constrained decoding).
- **Oracle and regret evaluation:** Standard in both algorithm selection (Kotthoff 2014) and LLM routing literature (LLMRouterBench, RouterBench).

## B. Potentially distinctive combination
The proposed combination may be defensible, but this assessment is bounded by the scope of the search conducted. Specifically:

- **Heterogeneous portfolio spanning fundamentally different system families:** In the literature verified by this review, no included study was found that jointly performs pre-deployment task-level prediction across classical classifiers, fine-tuned encoders, and generative language models while treating output-contract validity and selection regret as first-class outcomes. This is a bounded search finding, not proof of universal nonexistence. Confidence: Moderate.
- **Output contract failure as a first-class predicted outcome:** No paper in the verified corpus predicts output-contract validity from task-level features. Constrained decoding papers enforce validity at generation time but do not predict it from dataset properties. This appears to be a gap, but the expanded search may not have covered all relevant industrial or application-specific work. Confidence: Moderate.
- **Task-level prediction vs. query-level routing:** PsyMatrix and ModelLens perform task-level selection, but neither includes LLMs or classical models in the same portfolio, and neither predicts latency, cost, or validity. LLM routing benchmarks predict these operational outcomes but only at query level within homogeneous LLM pools.
- **Downstream selection regret as the practical endpoint across heterogeneous families:** Regret is evaluated in LLM routing (query-level, LLM-only). It has not been verified across truly heterogeneous model families at the task level.

### Comparison with PsyMatrix
PsyMatrix (Monteiro et al., 2024) is the most direct prior work for task-level text-dataset model recommendation. Key differences:

| Dimension | PsyMatrix | Proposed study |
|---|---|---|
| Portfolio | 24 fine-tuned PLMs | Classical, encoders, constrained/unconstrained LLMs |
| Task features | Psycholinguistic, topic, complexity | To be determined (may overlap) |
| Predicted outcomes | Model performance | Quality, validity, latency, cost |
| Output validity | Not modeled | First-class outcome |
| Selection regret | Not verified | Primary evaluation metric |
| Dataset independence | 146 from 11 base datasets | Must address independence explicitly |
| Classical models | No | Yes |
| Zero-shot/constrained LLMs | No | Yes |

### Comparison with ModelLens
ModelLens (Cai et al., 2026) operates at a much larger scale but with a narrower outcome set:

| Dimension | ModelLens | Proposed study |
|---|---|---|
| Scale | 47K models, 9.6K datasets | Smaller but more heterogeneous |
| Features | Learned latent space from leaderboards | Task-level meta-features |
| Portfolio | Pretrained models (open-source) | Classical + encoder + LLM |
| Predicted outcomes | Performance ranking | Quality, validity, latency, cost |
| Output validity | Not modeled | First-class outcome |
| Requires leaderboard data | Yes | No (task features only) |

## C. Strongest novelty threat
The strongest novelty threat is **PsyMatrix** (Monteiro et al., 2024), not the LLM routing literature. PsyMatrix already does task-level text-dataset characterization for pretrained model recommendation using meta-features, which is the core methodology of the proposed study. A reviewer could say:

*"PsyMatrix already characterizes text datasets and recommends models. Your work just adds more model types to the portfolio. That is an incremental extension, not a new contribution."*

Secondary threats come from **ModelLens** (task-level prediction at scale) and **LLMRouterBench** (multi-objective routing with regret).

To survive these threats, the project must demonstrate that:
1. Extending the portfolio to include classical models and constrained LLMs introduces fundamentally different prediction challenges (not just more categories).
2. Output-contract validity is a substantively new outcome that changes the selection landscape.
3. Task-level selection across heterogeneous families produces different insights from within-family recommendation.
4. The dataset independence concern in PsyMatrix (146 from 11 bases) is explicitly addressed in the proposed study design.

## D. Proposed contribution
This study develops and evaluates a reproducible task-level benchmark for predicting quality, output-contract validity, and operational behavior across heterogeneous bounded-decision implementations, and tests whether these predictions reduce system-selection regret on unseen tasks.

This contribution is conservative and contingent on the experimental results demonstrating that:
- the heterogeneous portfolio produces meaningful oracle variation;
- task features can predict cross-family outcomes;
- output validity is predictably variable across tasks and families.

## E. Novelty verdict
**PROCEED WITH REFRAMING**

*Justification:* PsyMatrix establishes that task-level text-dataset characterization for model recommendation is published work. The proposed study cannot claim task-level model recommendation as novel. However, no verified work combines (a) a portfolio spanning classical, encoder, and LLM families, (b) output-contract validity as a predicted outcome, and (c) selection regret across heterogeneous families. This combination is defensible if the study is explicitly positioned against PsyMatrix and ModelLens, and if the experimental design addresses dataset independence.

The verdict could shift to PROCEED if expanded searching confirms that no other work predicts validity from task features, or to MAJOR REDESIGN if such work is found.

## F. Publishability conditions
To make a meaningful journal contribution, the study must demonstrate:

- **Task count:** Determined through precision, feasibility, and effective-independence analysis. The PsyMatrix concern (146 from 11 bases) must be explicitly addressed; derived variants must be grouped and must not cross outer evaluation folds.
- **Diversity of primitive families:** Must rigorously include classical (e.g., SVM, logistic regression), fine-tuned encoders (e.g., BERT), and LLMs (unconstrained and constrained).
- **Meaningful oracle variation:** The "best" system family must change depending on the task. If LLMs or classifiers dominate uniformly, the selection problem is trivial.
- **Strong simple baselines:** Must include "always pick the best-on-average family" and simple heuristic rules (e.g., "use classical if dataset is large").
- **Leakage-free evaluation:** Strict train/test splits for tasks; tasks from the same base dataset must not cross outer folds.
- **Output-validity analysis:** Must empirically show that models fail output contracts, that failure rates vary across tasks, and that task features have predictive power for these failures.
- **Selection-regret analysis:** Report effect sizes and uncertainty intervals for regret reduction. The primary result will report effect sizes and uncertainty; negative or null findings remain scientifically valid.
- **Reproducibility:** All code, data splits, and evaluation protocols must be publicly available.
- **Value of negative results:** If task features cannot predict validity or regret across families, this must be thoroughly analyzed and presented as a boundary of meta-learning. Publishability depends on benchmark quality and analysis, not a predetermined positive result.

## Reviewer 2 challenge
*Reviewer 2:* "PsyMatrix already characterizes text datasets with psycholinguistic features and recommends pretrained models. ModelLens does the same at 47K-model scale. Auto-sklearn has done task-level meta-learning for decades. Adding a few more model types to the portfolio and calling it 'heterogeneous' is not a contribution. Furthermore, output validity is a solved engineering problem — just use constrained decoding. And task-level selection is too coarse to be useful when LLM routing already works at the query level."

## Required response
To answer this criticism, the project must:
1. **Show that heterogeneity is substantive, not cosmetic.** Classical classifiers and LLMs have fundamentally different failure modes (underfitting vs. hallucination), cost profiles (near-zero vs. API-priced), and latency distributions (milliseconds vs. seconds). The benchmark must expose these differences empirically.
2. **Show that output validity is NOT fully solved by constrained decoding.** Even with constrained decoding, generative models can produce valid-format but semantically incorrect labels. The question is whether this failure rate is predictable from task features before deployment.
3. **Show that task-level selection adds value beyond query-level routing.** For bounded-decision tasks with known label sets, the task-level decision (which family to deploy) precedes and is independent of query-level routing. The benchmark must compare task-level meta-selectors against query-level routing baselines adapted to the task level.
4. **Explicitly compare against PsyMatrix baselines.** If possible, use PsyMatrix features as one of several feature sets and report whether they are sufficient for cross-family selection.
5. **Address dataset independence.** Unlike PsyMatrix's 146 datasets from 11 bases, ensure effective independence of evaluation tasks.
