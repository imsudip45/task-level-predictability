# Closest Prior Work

This review organizes nearest prior work into three distinct dimensions:
- **A. Closest by task-level methodology** (dataset characterization & cross-task model recommendation)
- **B. Closest by operational objectives** (cost, latency, and selection regret in model routing)
- **C. Closest by output-validity treatment** (constrained decoding and contract adherence)

---

## A. Closest by Task-Level Methodology

### 1. PsyMatrix: Characterizing Text Datasets with Psycholinguistic Features
**Marcio Monteiro, Charu Karakkaparambil James, Marius Kloft, Sophie Fellenz (2024)**
*Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 14977–14990.
DOI: `10.18653/v1/2024.findings-emnlp.880`. Canonical URL: https://aclanthology.org/2024.findings-emnlp.880/

1. **Question studied:** Can multidimensional psycholinguistic and discourse features of text datasets enable a meta-learning system to recommend optimal or near-optimal pretrained language models (PLMs) for downstream fine-tuning without exhaustive per-dataset trial and error?
2. **Data used:** 146 text-classification datasets derived from 11 base datasets.
3. **Candidate systems compared:** 24 pretrained language models fine-tuned on task data.
4. **Features used:** Psycholinguistic features, topic distributions, and text complexity measures synthesized into low-dimensional dataset embeddings.
5. **Outcomes predicted:** Model performance (classification accuracy / F1) on target datasets.
6. **Generalization evaluation:** Meta-learning evaluated on held-out datasets.
7. **Selection unit:** Task-level (per-dataset model recommendation).
8. **Selection regret evaluated:** Not explicitly evaluated as downstream dollar/latency regret.
9. **Output validity modeled:** No (focuses entirely on fine-tuned transformer classification heads).
10. **Exact overlap with proposed study:** PsyMatrix represents the most direct prior work in task-level text dataset characterization for model recommendation. It computes dataset-level meta-features to predict model suitability before full-scale fine-tuning.
11. **Remaining defensible contribution:**
    - **Candidate portfolio heterogeneity:** PsyMatrix is restricted to 24 fine-tuned PLMs (homogeneous encoder family). It does not include sparse classical models (e.g., TF-IDF + Logistic Regression/SVM), rule-based primitives, zero-shot generative LLMs, or grammar-constrained LLMs.
    - **Operational outcomes:** PsyMatrix does not predict latency, monetary inference cost, or memory overhead.
    - **Output contract validity:** PsyMatrix does not model schema or format failures.
    - **Downstream selection regret:** PsyMatrix does not evaluate decision regret on multi-objective frontiers.
    - **Dataset independence:** PsyMatrix's 146 datasets stem from only 11 base corpora, introducing potential cross-variant contamination that the proposed study must explicitly avoid.
12. **Novelty threat level:** **CRITICAL**. Reviewers could argue that task-level text dataset meta-features for model recommendation are already established. The proposed project cannot claim novelty for the concept of task-level text characterization; it must emphasize cross-family heterogeneity, operational trade-offs, output validity, and leakage-free dataset independence.

### 2. ModelLens: Finding the Best for Your Task from Myriads of Models
**Rui Cai, Weijie Jacky Mo, Xiaofei Wen, Qiyao Ma, Wenhui Zhu, Xiwen Chen, Muhao Chen, Zhe Zhao (2026)**
*arXiv preprint*, arXiv:2605.07075. DOI: `10.48550/arXiv.2605.07075`. Canonical URL: https://arxiv.org/abs/2605.07075

1. **Question studied:** Can an implicit performance-aware latent space learned from historical public leaderboard interactions rank unseen models on unseen datasets without requiring candidate forward passes or fine-tuning on the target dataset?
2. **Data used:** 1.62M evaluation records spanning 47,000 models and 9,600 datasets.
3. **Candidate systems compared:** Pretrained models across open-source ecosystems (NLP, vision-language).
4. **Features used:** Performance-aware latent space over `(model, dataset, metric)` tuples learned via collaborative/graph filtering.
5. **Outcomes predicted:** Relative performance ranking of models on unseen datasets.
6. **Generalization evaluation:** Zero-shot evaluation on held-out task leaderboards.
7. **Selection unit:** Task-level.
8. **Selection regret evaluated:** No.
9. **Output validity modeled:** No.
10. **Exact overlap with proposed study:** Zero-shot task-level performance prediction on unseen datasets without running candidate systems on the target data.
11. **Remaining defensible contribution:**
    - ModelLens relies on dense historical leaderboard interaction graphs; it cannot operate on completely novel private tasks lacking leaderboard metadata.
    - ModelLens does not predict latency, inference compute cost, or memory footprints.
    - ModelLens does not include classical non-neural classifiers or output-contract constrained decoders.
    - ModelLens does not treat output-contract failure as a predicted outcome.
12. **Novelty threat level:** **HIGH**. Demonstrates that large-scale zero-shot task-level model recommendation is active and maturing.

### 3. OOD-Chameleon: Is Algorithm Selection for OOD Generalization Learnable?
**Liangze Jiang, Damien Teney (2024/2025)**
*Proceedings of the 42nd International Conference on Machine Learning (ICML 2025)*; *arXiv preprint*, arXiv:2410.02735.
DOI: `10.48550/arXiv.2410.02735`. Canonical URL: https://arxiv.org/abs/2410.02735

1. **Question studied:** Can dataset descriptors predict which out-of-distribution (OOD) generalization algorithm will perform best on a given dataset without training all candidate models?
2. **Data used:** Multi-dataset benchmark across synthetic, vision, and language distribution shifts.
3. **Candidate systems compared:** OOD generalization training algorithms (ERM, IRM, GroupDRO, CORAL, etc.).
4. **Features used:** Dataset descriptors measuring statistical properties, distribution shift indicators, and sample complexity.
5. **Outcomes predicted:** Generalization ranking across OOD algorithms.
6. **Generalization evaluation:** Multi-label classification evaluated on held-out datasets.
7. **Selection unit:** Task-level (per-dataset algorithm selection).
8. **Selection regret evaluated:** Evaluates top-k selection accuracy, but not operational cost regret.
9. **Output validity modeled:** No.
10. **Exact overlap with proposed study:** Formulates algorithm selection at the dataset level using pre-training dataset features to avoid trial-and-error training.
11. **Remaining defensible contribution:** OOD-Chameleon selects training algorithms for deep networks, whereas the proposed study selects across radically distinct inference architectures (rules, classical ML, encoders, generative LLMs) under operational and validity constraints.
12. **Novelty threat level:** **MODERATE**. Establishes modern precedent for learning decision rules from dataset descriptors.

---

## B. Closest by Operational Objectives (Cost, Latency, and Regret)

### 4. LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing
**Hao Li, Yiqun Zhang, Zhaoyan Guo, Chenxu Wang, Shengji Tang, Qiaosheng Zhang, Yang Chen, Biqing Qi, Peng Ye, Lei Bai, Zhen Wang, Shuyue Hu (2026)**
*Findings of the Association for Computational Linguistics: ACL 2026*, pages 37733–37754.
DOI: `10.18653/v1/2026.findings-acl.1881`. Canonical URL: https://aclanthology.org/2026.findings-acl.1881/ (arXiv:2601.07206)

1. **Question studied:** How do existing LLM routing strategies compare under a standardized, unified evaluation framework for performance-oriented and performance-cost trade-off routing?
2. **Data used:** >400,000 instances across 21 NLP datasets.
3. **Candidate systems compared:** 33 LLMs (proprietary and open-weight).
4. **Features used:** Query prompt embeddings and task type indicators.
5. **Outcomes predicted:** Response quality, latency-aware metrics, and serving cost.
6. **Generalization evaluation:** Evaluated on held-out test queries across 10 routing baselines.
7. **Selection unit:** **Query-level** (per-instance routing).
8. **Selection regret evaluated:** **Yes** (extensively analyzes the gap to the theoretical Oracle and model-recall failures).
9. **Output validity modeled:** No (does not track output contract or formatting compliance).
10. **Exact overlap with proposed study:** Joint evaluation of quality, cost, and latency; evaluation against an Oracle baseline; selection regret as the key figure of merit.
11. **Remaining defensible contribution:**
    - LLMRouterBench is strictly **query-level**, whereas the proposed study is **task-level** (pre-deployment system commitment).
    - LLMRouterBench operates exclusively on homogeneous LLMs; it completely omits deterministic rules, sparse classical classifiers, and fine-tuned encoders.
    - LLMRouterBench does not treat output validity as a predicted variable or operational failure mode.
12. **Novelty threat level:** **HIGH**. Shows that multi-objective routing benchmarks with oracle regret are thoroughly established in the query-level LLM space.

### 5. RouterBench: A Benchmark for Multi-LLM Routing System
**Qitian Jason Hu, Jacob Bieker, Xiuyu Li, Nan Jiang, Benjamin Keigwin, Gaurav Ranganath, Kurt Keutzer, Shriyash Kaustubh Upadhyay (2024)**
*arXiv preprint*, arXiv:2403.12031. DOI: `10.48550/arXiv.2403.12031`. Canonical URL: https://arxiv.org/abs/2403.12031

1. **Question studied:** How can multi-LLM routing systems be systematically assessed through a formal theoretical framework and standardized inference dataset?
2. **Data used:** Over 405,000 inference outcomes across representative LLMs.
3. **Candidate systems compared:** Multiple commercial and open-source LLMs.
4. **Features used:** Query difficulty, domain classification, and embedding features.
5. **Outcomes predicted:** Accuracy and monetary inference cost.
6. **Generalization evaluation:** Held-out query partitions.
7. **Selection unit:** **Query-level**.
8. **Selection regret evaluated:** **Yes** (regret against optimal routing policy).
9. **Output validity modeled:** No.
10. **Exact overlap with proposed study:** Theoretical formalization of router regret and cost-accuracy trade-offs.
11. **Remaining defensible contribution:** Query-level rather than task-level; homogeneous LLM portfolio; no classical models; no output contract modeling.
12. **Novelty threat level:** **HIGH**.

### 6. RouteJudge: An Open Platform for Reproducible and Preference-Aware LLM Routing
**Guannan Lai, Haoran Hu, Han-Jia Ye (2026)**
*arXiv preprint*, arXiv:2606.18774. Accepted at Pluralistic Alignment Workshop at ICML 2026 (non-archival).
DOI: `10.48550/arXiv.2606.18774`. Canonical URL: https://arxiv.org/abs/2606.18774

1. **Question studied:** How can routing systems be evaluated online using pairwise user preferences while tracking cost, latency, and task metadata?
2. **Data used:** Online human pairwise preference feedback and benchmark query sets.
3. **Candidate systems compared:** LLMs evaluated via the ORBIT toolbox.
4. **Features used:** Query text, task metadata, and router decision traces.
5. **Outcomes predicted:** Preference alignment, cost, and latency.
6. **Generalization evaluation:** Online platform deployment.
7. **Selection unit:** **Query-level**.
8. **Selection regret evaluated:** Yes, via preference regret.
9. **Output validity modeled:** No.
10. **Exact overlap with proposed study:** Explicit multi-objective tracking of cost, latency, and task metadata.
11. **Remaining defensible contribution:** Online query-level preference evaluation for LLMs, differing from pre-deployment task-level algorithm selection across architectural families.
12. **Novelty threat level:** **MODERATE**.

---

## C. Closest by Output-Contract Validity

### 7. Koa-action: Fast and Consistent Structured Decision Making with Generative LLMs
**Shenghong Dai, Shiva Kumar Pentyala, Yingchi Liu, Shubham Mehrotra, Suman Banerjee, James Zhu, Bin Bi, Sitaram Asur, Phil Mui (2026)**
*arXiv preprint*, arXiv:2609.36115. DOI: `10.48550/arXiv.2609.36115`. Canonical URL: https://arxiv.org/abs/2609.36115

1. **Question studied:** Can bounded decision-making (classification, intent routing, Boolean checks) be formulated as single-step constrained generation with atomic label tokens to achieve low latency and format adherence?
2. **Data used:** Production intent-routing benchmarks and standard classification sets.
3. **Candidate systems compared:** Generative LLMs with atomic single-token decoding vs. multi-token prompting and specialized classifiers.
4. **Features used:** Text inputs and atomic control tokens.
5. **Outcomes predicted:** Deterministic label emission, sub-second latency, and classification accuracy.
6. **Generalization evaluation:** Benchmark evaluation on intent routing.
7. **Selection unit:** Instance-level generation mechanism.
8. **Selection regret evaluated:** No.
9. **Output validity modeled:** **Yes** (guaranteed via atomic special-token vocabulary restriction).
10. **Exact overlap with proposed study:** Direct analysis of the speed, validity, and quality trade-offs of constrained generative classification.
11. **Remaining defensible contribution:** Koa-action is a model-level decoding technique, not a cross-system task-level recommender. It proves that constrained decoders exist as viable candidates in our proposed portfolio.
12. **Novelty threat level:** **LOW** (supports portfolio candidate feasibility rather than competing as a selector).

---

## Summary Comparison Matrix

| Paper | Selection Unit | Candidate Portfolio | Predicted Outcomes | Validity Modeled? | Regret Evaluated? | Main Overlap | Remaining Gap |
|---|---|---|---|---|---|---|---|
| **PsyMatrix** (Monteiro et al. 2024) | Task | 24 fine-tuned PLMs | Performance (F1/Acc) | No | Not verified | Task features → NLP model recommendation | Homogeneous PLMs; no classical or LLMs; no latency/cost/validity; dataset independence concern |
| **ModelLens** (Cai et al. 2026) | Task | 47K pretrained models | Performance ranking | No | No | Zero-shot task-level performance prediction | No operational behavior (latency/cost); no classical models; no validity or regret |
| **OOD-Chameleon** (Jiang & Teney 2025) | Task | OOD training algorithms | Generalization rank | No | Top-k only | Learning decision rules from dataset descriptors | Focuses on training algorithms; no inference cost/latency; no validity; no LLMs |
| **LLMRouterBench** (Li et al. 2026) | Query | 33 LLMs | Quality, latency, cost | No | Yes (Oracle gap) | Multi-objective routing benchmark & regret | Query-level; LLMs only; no classical models; no output contract modeling |
| **RouterBench** (Hu et al. 2024) | Query | LLMs | Quality, cost | No | Yes | Theoretical routing regret & benchmarking | Query-level; LLMs only; no classical models; no output validity |
| **RouteJudge** (Lai et al. 2026) | Query | LLMs | Preference, cost, latency | No | Yes | Multi-objective tracking & task metadata | Query-level; online preference focus; LLMs only; no validity |
| **Koa-action** (Dai et al. 2026) | Instance | Generative LLMs | Latency, label accuracy | Yes (enforced) | No | Single-token constrained classification | Method-level decoding; not a task-level selector across families |
