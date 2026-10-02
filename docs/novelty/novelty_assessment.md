# Novelty Assessment

## A. Established Ideas

The following concepts are clearly established in the literature and cannot be claimed as novel contributions:

1. **Algorithm selection from problem characteristics:** Formalized by Rice (1976), with 50 years of foundational literature across combinatorial search, optimization, and machine learning (Smith-Miles 2009, Kotthoff 2014, Vanschoren 2018).
2. **Dataset meta-features for algorithm recommendation:** Standardized in AutoML frameworks including Auto-WEKA (Thornton et al., 2013) and auto-sklearn (Feurer et al., 2015), utilizing statistical, landmarking, and complexity measures (Brazdil et al. 1994, Pfahringer et al. 2000, Ho & Basu 2002).
3. **Text-dataset characterization for model recommendation:** Directly established by **PsyMatrix** (Monteiro et al., Findings of EMNLP 2024), which extracts psycholinguistic and discourse features across 146 text datasets to recommend fine-tuned pretrained language models.
4. **Large-scale zero-shot task-level performance prediction:** Demonstrated by **ModelLens** (Cai et al., 2026) across 47,000 models and 9,600 datasets using latent performance spaces learned from public leaderboards.
5. **Multi-objective LLM routing (quality, cost, latency):** Addressed by extensive query-level benchmarks including **LLMRouterBench** (Li et al., Findings of ACL 2026), **RouterBench** (Hu et al., 2024), **RouteJudge** (Lai et al., 2026), and methods such as **FrugalGPT** (Chen et al., 2023), **RouteLLM** (Ong et al., ICLR 2025), and **Hybrid LLM** (Ding et al., ICLR 2024).
6. **Evaluation via Oracle performance and selection regret:** Universally practiced across classical algorithm selection benchmarks (Kotthoff 2014) and contemporary LLM router benchmarks (Hu et al. 2024, Li et al. 2026).
7. **Constrained decoding for structured output validity:** Thoroughly established via methods such as sequence-to-tree generation (Yu et al., 2022), Lazy-k decoding (Hemmer et al., 2023), grammar-constrained token optimization (Hamilton & Mimno, 2025), and single-token atomic generation (Koa-action; Dai et al., 2026).

---

## B. Potentially Distinctive Combination

The proposed study investigates whether pre-deployment characteristics of a bounded-decision task can predict the quality, output validity, and operational latency/cost of heterogeneous decision systems to reduce selection regret on unseen tasks.

This combination is potentially distinctive along four specific axes:

1. **Architectural heterogeneity across system families:**
   Existing task-level selectors operate within a single architectural family (e.g., auto-sklearn on classical ML pipelines, PsyMatrix on fine-tuned transformer encoders, ModelLens on leaderboard-evaluated foundation models). Existing routers operate within LLM ensembles (LLMRouterBench, RouteLLM). In the literature verified by this review, no included study was found that jointly performs pre-deployment task-level prediction across deterministic rules, sparse classical classifiers, fine-tuned encoders, and generative language models.
2. **Output-contract validity as a first-class predicted outcome:**
   Prior work enforces output structure during decoding (e.g., regex/grammar masks, Koa-action) or measures post-hoc failure rates. No verified prior study models *whether* a given candidate system family will violate an output contract as a predictable function of task meta-features before deployment.
3. **Task-level commitment vs. Query-level routing:**
   Contemporary LLM routing focuses almost entirely on query-level dispatching. In enterprise and production settings, system engineers frequently must commit to an infrastructure archetype (e.g., deploying an edge logistic regression model vs. hosting an encoder container vs. calling an external LLM API) *before* query-level traffic arrives. Evaluating selection regret at this pre-deployment task boundary addresses a distinct operational decision level.
4. **Downstream selection regret across radically different cost/latency regimes:**
   Because candidate primitives span orders of magnitude in inference latency (microseconds for sparse classifiers vs. seconds for generative LLMs) and cost ($0 for local rules vs. token charges for APIs), the regret landscape is fundamentally steeper and more discontinuous than within-LLM routing.

---

## C. Strongest Novelty Threat

The single strongest novelty threat to this project is **PsyMatrix** (Monteiro, Karakkaparambil James, Kloft, Fellenz, Findings of EMNLP 2024), followed by **ModelLens** (Cai et al., 2026) and **LLMRouterBench** (Li et al., Findings of ACL 2026).

A skeptical reviewer will argue:
> *"PsyMatrix already proved that you can characterize text datasets using psycholinguistic features and predict which pretrained model works best. LLMRouterBench already benchmarked cost, latency, and oracle regret. Your project merely takes PsyMatrix's dataset-characterization idea and applies it to a broader list of models. Adding a few scikit-learn models and an LLM API does not constitute a new scientific paradigm."*

### How the Proposed Study Must Substantively Differ
To answer this threat, the proposed project must:
1. **Demonstrate non-trivial cross-family trade-offs:** Show that simple rules (e.g., "always use LLMs" or "use classical if N is large") incur severe regret, and that meta-features predict when a sparse classical model beats a fine-tuned encoder or when an unconstrained LLM suffers catastrophic contract invalidity.
2. **Address dataset independence rigorously:** PsyMatrix derived 146 evaluation sets from only 11 base corpora. The proposed benchmark must ensure effective task independence by grouping derived variants and enforcing strict zero-leakage outer cross-validation folds.
3. **Establish output-contract validity as a key operational dimension:** Demonstrate that contract violation is not merely an engineering nuisance, but a task-predictable failure mode that alters the optimal system choice.

---

## D. Proposed Defensible Contribution Statement

> *“This study develops and evaluates a reproducible task-level benchmark for predicting quality, output-contract validity, and operational behavior across heterogeneous bounded-decision implementations, and tests whether these predictions reduce system-selection regret on unseen tasks.”*

This statement is conservative, precise, and avoids unsupported novelty claims.

---

## E. Novelty Verdict

### **PROCEED WITH REFRAMING**

**Justification:**
The original conceptualization assumed that task-level model recommendation from text dataset properties was entirely unaddressed. The verified presence of **PsyMatrix** (EMNLP 2024 Findings) and **ModelLens** (2026) invalidates any claim to being "the first text-dataset model recommender." Furthermore, **LLMRouterBench** (ACL 2026 Findings) establishes that multi-objective evaluation with selection regret is well-developed in query-level LLM routing.

However, the intersection—**pre-deployment task-level prediction across radically heterogeneous architectural families with output-contract validity and operational regret as first-class endpoints**—remains defensible as a benchmark and empirical study. The project can proceed, provided its contribution is strictly reframed around cross-family boundaries, validity predictability, and auditable dataset independence.

---

## F. Publishability Conditions

To achieve publication in a top-tier machine learning or NLP venue (e.g., JMLR, TMLR, or NeurIPS Datasets and Benchmarks), the study must satisfy:

1. **Effective task independence:** Nominal task counts are meaningless if datasets share base sources. All dataset variants derived from the same base corpus must be grouped and held out together across outer folds.
2. **Rigorous family representation:** The candidate portfolio must include at least:
   - Deterministic rule heuristics;
   - Sparse classical models (e.g., TF-IDF + Logistic Regression/SVM);
   - Dense fine-tuned encoders (e.g., RoBERTa/DeBERTa);
   - Unconstrained generative LLMs (zero-shot/few-shot);
   - Constrained generative LLMs (schema-enforced).
3. **Meaningful Oracle variation:** The empirical oracle must not be monopolized by a single system family. If fine-tuned encoders or LLMs win on 95% of tasks regardless of constraints, the algorithm selection problem collapses.
4. **Strong baseline comparisons:** The learned selector must be evaluated against:
   - Single Best on Average (SBoA);
   - Simple heuristic baselines (e.g., size-based or vocabulary-based decision trees);
   - Adapted query-level routing heuristics.
5. **Leakage-free meta-feature extraction:** All task-level features must be computed exclusively on the designated training/prompt splits of the unseen tasks without target label leakage.
6. **Explicit output-validity evaluation:** Measure syntactic format compliance and semantic label set adherence, documenting failure distributions across families.
7. **Value of negative or bounded findings:** If pre-deployment task features fail to reliably beat simple baselines on unseen task families, the result remains scientifically valuable as an empirical boundary on the limits of meta-learning for heterogeneous system selection.
