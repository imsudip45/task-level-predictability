# Claim Boundary

## SAFE OR POTENTIALLY SAFE CLAIMS

All safe claims must remain conditional on experimental verification and bounded by the literature corpus reviewed:

- **Claim 1 (Cross-Family Task-Level Portfolio):**
  *Wording:* “In the literature verified by this review, no included study was found that jointly performs pre-deployment task-level prediction across classical classifiers, fine-tuned encoders, and generative language models while evaluating system-selection regret across quality, latency, and monetary cost.”
  *Supporting prior work:* PsyMatrix (Monteiro et al., 2024) evaluates only fine-tuned PLMs. ModelLens (Cai et al., 2026) evaluates open-source foundation models without operational cost/latency. LLMRouterBench (Li et al., 2026) operates at the query level on LLMs only. auto-sklearn (Feurer et al., 2015) operates on tabular data.
  *Evidence required:* Empirical demonstration of a unified benchmark spanning all three system families.
  *Confidence level:* **Moderate**. Bounded search finding; industrial or domain-specific benchmarks may exist.

- **Claim 2 (Output-Contract Validity as a Predicted Variable):**
  *Wording:* “This benchmark investigates whether output-contract validity rates across generative and typed decision systems can be predicted from task-level characteristics prior to deployment.”
  *Supporting prior work:* Constrained decoding methods (Yu et al. 2022, Hemmer et al. 2023, Dai et al. 2026) enforce validity at generation time, but do not predict contract failure as an outcome from dataset meta-features.
  *Evidence required:* Statistical evidence that task meta-features correlate with and predict contract failure rates on unseen tasks.
  *Confidence level:* **Moderate**.

- **Claim 3 (Pre-Deployment Regret Reduction):**
  *Wording:* “Our experiments assess whether pre-deployment task-level meta-features reduce downstream selection regret compared to standard static portfolio choices (such as Single Best on Average or size-based heuristics).”
  *Supporting prior work:* Regret evaluation is standard in query-level LLM routing (Hu et al. 2024, Li et al. 2026), but has not been established for pre-deployment task-level cross-family selection.
  *Evidence required:* Effect sizes and confidence intervals demonstrating regret reduction on held-out tasks.
  *Confidence level:* **Low-to-Moderate** (depends entirely on experimental outcomes; null results must be treated as valid findings).

- **Claim 4 (Methodological Independence over PsyMatrix):**
  *Wording:* “The benchmark design explicitly enforces effective task independence by grouping derived dataset variants to prevent cross-variant leakage, addressing an evaluation limitation present in prior text-dataset characterization studies.”
  *Supporting prior work:* PsyMatrix utilized 146 datasets derived from 11 base datasets without explicit cross-fold grouping.
  *Evidence required:* Partitioning protocol documentation demonstrating zero base-dataset overlap across outer folds.
  *Confidence level:* **High** (structural design property).

---

## PROHIBITED OR UNSUPPORTED CLAIMS

The following claims are demonstrably false or scientifically unsupportable based on the verified literature and must be strictly avoided:

1. **“The first algorithm-selection framework”**
   *Why prohibited:* Rice established the Algorithm Selection Problem in 1976. The field has 50 years of literature.
2. **“The first use of dataset meta-features for model recommendation”**
   *Why prohibited:* Standard in AutoML for decades (Brazdil et al. 1994, Pfahringer et al. 2000, Thornton et al. 2013, Feurer et al. 2015).
3. **“The first NLP dataset characterization or model recommender”**
   *Why prohibited:* Directly refuted by **PsyMatrix** (Monteiro et al., Findings of EMNLP 2024) and **ModelLens** (Cai et al., 2026).
4. **“The first LLM router or routing benchmark”**
   *Why prohibited:* Refuted by RouterBench (2024), LLMRouterBench (ACL 2026 Findings), RouteJudge (2026), FrugalGPT (2023), and RouteLLM (ICLR 2025).
5. **“The first constrained-output classification method”**
   *Why prohibited:* Constrained decoding for classification is thoroughly explored in prior literature (Yu et al. 2022, Hemmer et al. 2023, Behzad et al. 2024, Dai et al. 2026).
6. **“The first heterogeneous AI benchmark”**
   *Why prohibited:* Broadly claims priority over numerous benchmarks comparing classical ML against neural nets or transformers.
7. **“Universal superiority of any candidate primitive family”**
   *Why prohibited:* Violates the No Free Lunch theorem and empirical algorithm selection reality; primitives exhibit distinct trade-offs across data scale, label cardinality, latency, and cost.
8. **“Generalization beyond bounded single-label decisions”**
   *Why prohibited:* The study is strictly bounded to single-label categorical decisions. Extending claims to open-ended dialogue, summarization, or free-form reasoning is unsupported.
9. **“PsyMatrix features are fundamentally defective or uninformative”**
   *Why prohibited:* Cannot be claimed without empirical ablation comparing psycholinguistic features directly against alternative feature sets.
10. **“Novelty is proven by the absence of identical papers in our search”**
    *Why prohibited:* A literature search establishes absence within an auditable sample, not proof of universal nonexistence.
