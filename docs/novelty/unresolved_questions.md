# Unresolved Questions

These questions must be answered before freezing the research charter.

## Task-level methodology

- **Is task-level selection sufficiently different from existing per-dataset model recommendation?**
  PsyMatrix (Monteiro et al., 2024) already performs task-level text-dataset characterization for pretrained model recommendation using psycholinguistic features. ModelLens (Cai et al., 2026) does task-level recommendation at 47K-model scale using latent spaces. The proposed study must articulate what task-level prediction across heterogeneous families adds beyond extending PsyMatrix's portfolio.

- **Has prior work already compared classical classifiers, encoders, and LLMs in one task-level selector with cost/latency objectives?**
  Current search suggests no, but deep survey of internal industry benchmarks and application-specific papers (e.g., in healthcare or finance NLP) is needed. This is a bounded search finding.

- **What is the correct comparison against PsyMatrix?**
  Should PsyMatrix features be used as one of several feature sets in the proposed study? Should PsyMatrix's evaluation design be replicated and extended? The proposed study must explicitly engage with PsyMatrix's methodology and limitations.

## Output validity

- **Has output validity already been predicted from dataset features, or just enforced via constrained decoding?**
  Within the verified corpus, validity is enforced at generation time (constrained decoding) but not predicted from task-level features before deployment. However, this gap may be covered by industrial work, application-specific papers, or very recent preprints not found in this search.

- **Is output validity a meaningful predicted variable, or is it effectively solved by constrained decoding?**
  Constrained decoding ensures format validity (e.g., valid JSON, valid label from a set). But semantic validity (e.g., the label is from the right set but incorrect) is not guaranteed. The study must clarify which type of validity it measures and whether task features predict either type.

## Dataset independence

- **How should derived datasets be handled?**
  PsyMatrix reports 146 datasets from 11 base datasets. This raises the concern that nominal dataset count does not equal the number of independent task families. The proposed study must:
  - Group derived variants from the same base dataset.
  - Ensure variants from the same base do not cross outer evaluation folds.
  - Report both nominal and effective (grouped) task counts.
  - Use effective task independence as the primary measure of benchmark breadth, not raw task count.

- **What is the minimum meaningful candidate portfolio?**
  Must determine how many distinct system families are needed to prove heterogeneity without overwhelming the evaluation compute budget. A portfolio of 3 families (classical, encoder, LLM) may be the minimum; 5-6 may be needed for robustness.

## Selection regret

- **Has selection regret been evaluated across heterogeneous system families, or only within LLM routing?**
  Regret is standard in LLM routing (LLMRouterBench, RouterBench) but these operate within homogeneous LLM pools. Algorithm selection literature (Kotthoff 2014, Hutter et al. 2014) uses runtime prediction but in SAT/CSP domains, not NLP. Task-level regret across classical + encoder + LLM families appears unverified.

## Contribution framing

- **Is the main contribution a method (the meta-model), a benchmark (the dataset of tasks and model behaviors), an empirical finding, or an evaluation framework?**
  This decision affects the target venue and the evaluation criteria. A benchmark contribution requires comprehensive coverage and reproducibility. A method contribution requires novel algorithms. An empirical contribution requires surprising or boundary-setting findings.

- **Would a negative result remain publishable?**
  If task features cannot reliably predict which family is best due to noise or lack of discriminative power, this is a scientifically valid finding. It would set a boundary on meta-learning for heterogeneous system selection. Venues like NeurIPS Datasets and Benchmarks track, JMLR, or Transactions on Machine Learning Research may be receptive.

- **Which journal communities are the best match?**
  - JMLR or Machine Learning: for methods/AutoML/meta-learning emphasis.
  - ACL (Findings or main): for NLP task focus and text-dataset characterization.
  - NeurIPS Datasets and Benchmarks: for benchmark contribution.
  - TMLR: for systematic empirical studies.
  - The decision should wait until the contribution framing is resolved.

## Comparison methodology

- **What is the correct comparison against LLM-routing literature?**
  Should a query-level router (e.g., RouteLLM) be adapted to the task level as a baseline? Should the study evaluate both task-level and query-level selection on the same tasks to measure the granularity trade-off?
