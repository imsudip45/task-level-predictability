# Unresolved Questions

These substantive questions must be resolved before freezing the research charter:

## 1. Task-Level Methodology vs. Existing Literature
- **How does task-level selection substantially advance beyond PsyMatrix (Monteiro et al., 2024)?**
  PsyMatrix proved that text dataset characteristics (psycholinguistic, topic, complexity) can recommend pretrained transformers. Does expanding the portfolio to include classical models (TF-IDF + Logistic Regression/SVM) and generative LLMs introduce a fundamentally new meta-learning problem, or does it merely extend the candidate set?
- **How does the study contrast with ModelLens (Cai et al., 2026)?**
  ModelLens operates at massive scale (47K models, 9.6K datasets) using leaderboard latent spaces. Since ModelLens handles zero-shot dataset recommendation, how does our feature-based task fingerprint justify itself when historical interaction data is absent?

## 2. Portfolio and Heterogeneity Boundaries
- **What is the minimum candidate portfolio required to demonstrate meaningful heterogeneity?**
  Does a portfolio consisting of:
  1. Deterministic majority / rule heuristic;
  2. Sparse linear classifier (TF-IDF + Logistic Regression);
  3. Pretrained encoder fine-tuned on task data (e.g., DeBERTa-v3);
  4. Unconstrained generative LLM (few-shot prompting);
  5. Constrained generative LLM (grammar/atomic token constrained);
  provide sufficient architectural divergence without exceeding computational evaluation budgets?
- **Does the Oracle exhibit meaningful variation across these families?**
  If fine-tuned encoders dominate on 90%+ of datasets where training data exists, does the selection problem collapse to a trivial choice between zero-shot LLMs (when $N=0$) and encoders (when $N>0$)?

## 3. Output-Contract Validity
- **Is output-contract validity predictable from pre-deployment task features?**
  While format constraints can be strictly enforced by grammar-constrained decoders (e.g., Koa-action, Outlines), does semantic validity (assigning an allowed label that is contextually meaningful vs. degenerate collapse) vary predictably with task properties like label set cardinality, semantic overlap, and input text length?
- **Is output validity a primary decision factor or a secondary filter?**
  Should validity be modeled as a continuous probability of contract compliance, or as a hard threshold constraint in a constrained optimization problem?

## 4. Benchmark Design and Dataset Independence
- **How should dataset independence be strictly operationalized?**
  Learning from the limitation in PsyMatrix (146 datasets derived from 11 base datasets), how will the benchmark group task variants? If multiple tasks share the same underlying text corpus (e.g., binary vs. fine-grained emotion classification on the same text), they must never cross outer evaluation folds.
- **What is the effective sample size for task-level meta-learning?**
  If the benchmark contains $M$ tasks, but they cluster into $K$ independent task families, what is the statistical power to detect meaningful regret reductions?

## 5. Comparison against Query-Level Routing
- **What is the precise baseline comparison against query-level LLM routers?**
  Query-level routers (LLMRouterBench, RouteLLM, FrugalGPT) decide on a per-query basis. How should a task-level selector be compared against an ensemble that runs an adapted query-level router across the task? Does task-level commitment offer latency, caching, or cold-start advantages that compensate for the lack of instance-level flexibility?

## 6. Publication Strategy and Null Results
- **Is the primary contribution a benchmark, an empirical finding, or a selection algorithm?**
  If the study designs a rigorous, leakage-free benchmark spanning heterogeneous families with standardized evaluation protocols, it may be best targeted at a Datasets and Benchmarks track (e.g., NeurIPS) or an empirical venue (e.g., TMLR, JMLR).
- **Would a negative result remain fully publishable?**
  If task-level meta-features fail to reliably beat a simple heuristic baseline (such as "always pick fine-tuned encoder if $N > 500$, else pick constrained LLM"), does the empirical negative finding provide sufficient scientific value by demonstrating the boundaries of meta-learning in heterogeneous NLP systems?
