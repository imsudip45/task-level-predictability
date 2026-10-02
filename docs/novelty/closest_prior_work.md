# Closest Prior Work

Papers are organized by the dimension of closest overlap.

## A. Closest by task-level methodology

### 1. PsyMatrix: Characterizing Text Datasets with Psycholinguistic Features
**Monteiro, Karakkaparambil James, Kloft, Fellenz (2024). Findings of EMNLP 2024.**

1. **Question:** Can psycholinguistic features of text datasets enable a meta-learning system to recommend the best pretrained model for fine-tuning?
2. **Data:** 146 text-classification datasets derived from 11 base datasets; 24 pretrained language models.
3. **Candidate systems:** 24 pretrained language models (fine-tuned).
4. **Features:** Psycholinguistic features, topic distributions, complexity measures.
5. **Outcomes:** Model performance for recommendation.
6. **Generalization:** Meta-learning evaluation on held-out datasets.
7. **Selection:** Task-level.
8. **Regret evaluated:** Not verified.
9. **Validity modeled:** No.
10. **Overlap:** This is the closest NLP-specific task-level model recommendation work. It uses dataset features (psycholinguistic) to predict which pretrained model to fine-tune — directly analogous to the proposed task-fingerprint approach.
11. **Remaining contribution:** PsyMatrix only considers fine-tuned PLMs. It does not include classical classifiers, zero-shot or constrained generative LLMs, and does not model output validity, latency, or selection regret. The 146 datasets are derived from only 11 base datasets, raising dataset independence concerns.
12. **Novelty impact:** CRITICAL. A reviewer could argue that PsyMatrix already does task-level text-dataset characterization for model recommendation, making the proposed study incremental unless it substantially extends the portfolio, outcomes, and evaluation design.

### 2. ModelLens: Finding the Best for Your Task from Myriads of Models
**Cai, Mo, Wen, Ma, Zhu, Chen, Chen, Zhao (2026). arXiv:2605.07075.**

1. **Question:** Can a performance-aware latent space rank unseen models on unseen datasets without running candidates on the target data?
2. **Data:** 1.62M evaluation records spanning 47K models and 9.6K datasets.
3. **Candidate systems:** Open-source pretrained models at massive scale.
4. **Features:** Performance-aware latent space over model-dataset-metric tuples (learned from leaderboards).
5. **Outcomes:** Model performance ranking.
6. **Generalization:** Held-out tasks; generalizes to text and vision-language.
7. **Selection:** Task-level.
8. **Regret evaluated:** No.
9. **Validity modeled:** No.
10. **Overlap:** Task-level model recommendation without running candidates on the target; largest scale study found.
11. **Remaining contribution:** ModelLens does not predict operational behavior (latency, cost, validity). It does not include classical classifiers or constrained LLMs. Selection regret is not a metric.
12. **Novelty impact:** HIGH. ModelLens demonstrates that task-level model recommendation from dataset features is a maturing field, compressing the space for novel claims.

### 3. auto-sklearn: Efficient and Robust Automated Machine Learning
**Feurer et al. (2015). NeurIPS.**

1. **Question:** Can meta-learning over dataset features warmstart Bayesian optimization for model selection?
2. **Data:** 140 OpenML datasets.
3. **Candidate systems:** Classical classifiers (scikit-learn).
4. **Features:** Statistical, landmarking, PCA-based meta-features.
5. **Outcomes:** Accuracy.
6. **Generalization:** Cross-validation on held-out datasets.
7. **Selection:** Task-level.
8. **Regret evaluated:** No.
9. **Validity modeled:** No.
10. **Overlap:** Foundational task-level meta-learning for model selection with meta-features.
11. **Remaining contribution:** Tabular only; no text; no LLMs; no validity; no latency.
12. **Novelty impact:** Low (different domain, but establishes that the general approach is not novel).

## B. Closest by operational objectives

### 4. LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing
**Li et al. (2026). arXiv:2601.07206.**

1. **Question:** How do routing methods compare under unified evaluation for performance-cost trade-offs?
2. **Data:** 400K+ instances across 21 datasets, 33 models.
3. **Candidate systems:** 33 LLMs.
4. **Features:** Prompt embeddings.
5. **Outcomes:** Accuracy; enables latency-aware analysis.
6. **Generalization:** Held-out queries.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes (gap to oracle).
9. **Validity modeled:** No.
10. **Overlap:** Multi-objective routing (cost, performance, latency); oracle/regret evaluation; comprehensive benchmarking.
11. **Remaining contribution:** Query-level, not task-level; homogeneous LLM portfolio; no classical models; no output validity.
12. **Novelty impact:** HIGH. Demonstrates that multi-objective routing benchmarks are a crowded area. The proposed project must clearly separate task-level from query-level, and heterogeneous from homogeneous.

### 5. RouterBench: A Benchmark for Multi-LLM Routing System
**Hu et al. (2024). arXiv:2403.12031.**

1. **Question:** Can a theoretical framework and standardized dataset benchmark LLM routers?
2. **Data:** 405K+ inference outcomes.
3. **Candidate systems:** LLMs.
4. **Features:** Query characteristics.
5. **Outcomes:** Accuracy, cost.
6. **Generalization:** Held-out queries.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes.
9. **Validity modeled:** No.
10. **Overlap:** Routing benchmark design; regret evaluation framework.
11. **Remaining contribution:** No task-level selection; no classical models; no output validity.
12. **Novelty impact:** HIGH. Similar to LLMRouterBench.

### 6. FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance
**Chen, Zaharia, Zou (2023). arXiv:2305.05176.**

1. **Question:** Can LLM cascading reduce cost while maintaining quality?
2. **Data:** Multiple NLP tasks.
3. **Candidate systems:** LLM APIs (GPT-4, ChatGPT, etc.).
4. **Features:** Query text.
5. **Outcomes:** Accuracy, cost.
6. **Generalization:** Per-query evaluation.
7. **Selection:** Query-level (cascade).
8. **Regret evaluated:** Not verified.
9. **Validity modeled:** No.
10. **Overlap:** Cost-aware model selection; foundational LLM routing work.
11. **Remaining contribution:** Query-level cascade only; no classical models; no task-level prediction; no validity.
12. **Novelty impact:** Moderate. Foundational but focused narrowly on LLM cascading.

## C. Closest by output-validity treatment

### 7. Constrained Sequence-to-Tree Generation for Hierarchical Text Classification
**Yu et al. (2022). SIGIR.**

This paper enforces hierarchical label validity via constrained decoding. It is a single-model methodology, not a task-level selector. Relevant as background on output validity enforcement, but does not predict validity from dataset features.

### 8. Lost in Space: Optimizing Tokens for Grammar-Constrained Decoding
**Hamilton & Mimno (2025). arXiv:2502.14969.**

Addresses grammar-constrained decoding for structured outputs. Demonstrates the "quality tax" of constrained generation. Relevant for understanding why output validity is non-trivial, but not a selection problem.

**No paper in the verified corpus was found that predicts output-contract validity from task-level features before running the model.** This remains the strongest potential gap.

---

## Comparison Table

| Paper | Selection unit | Candidate portfolio | Predicted outcomes | Validity modeled? | Regret evaluated? | Main overlap | Remaining gap |
|---|---|---|---|---|---|---|---|
| PsyMatrix (Monteiro et al. 2024) | Task | 24 fine-tuned PLMs | Performance | No | Not verified | Text dataset features → model recommendation | No classical/LLMs; no validity/latency/regret |
| ModelLens (Cai et al. 2026) | Task | 47K models | Performance ranking | No | No | Task-level recommendation at scale | No operational behavior; no validity/regret |
| LLMRouterBench (Li et al. 2026) | Query | 33 LLMs | Accuracy, latency, cost | No | Yes | Multi-objective routing benchmark | Query-level; homogeneous; no validity |
| RouterBench (Hu et al. 2024) | Query | LLMs | Accuracy, cost | No | Yes | Routing benchmark design | Query-level; homogeneous; no validity |
| FrugalGPT (Chen et al. 2023) | Query | LLM APIs | Accuracy, cost | No | Not verified | Cost-aware model cascading | Query-level; LLM-only; no validity |
| auto-sklearn (Feurer et al. 2015) | Task | Classical classifiers | Accuracy | No | No | Task-level meta-learning | No text; no LLMs; no validity/latency |
| Yu et al. 2022 | Instance | 1 model | Labels | Yes (enforced) | No | Validity enforcement | Not selection; single model |
| Hamilton & Mimno 2025 | Instance | 1 model | Valid sequences | Yes (enforced) | No | Grammar constraint methodology | Not selection; single model |
