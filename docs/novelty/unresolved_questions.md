# Unresolved Questions

- Is task-level selection sufficiently different from existing per-dataset model recommendation (e.g., ModelLens)?
- Has prior work already compared classical classifiers, encoders, and LLMs in one task-level selector with cost/latency objectives? (Current search suggests no, but deep survey of internal industry benchmarks is needed).
- Has output validity already been predicted from dataset features, or just enforced via constrained decoding?
- Has selection regret been evaluated across heterogeneous system families, or only within LLM routing?
- What is the minimum meaningful candidate portfolio to prove heterogeneity without overwhelming the evaluation compute budget?
- What is the correct comparison against LLM-routing literature? Should we adapt a query-level router to the task level as a baseline?
- Is the main contribution a method (the meta-model), a benchmark (the dataset of tasks and model behaviors), an empirical finding, or an evaluation framework?
- Would a negative result (i.e., task features cannot reliably predict which family is best due to noise) remain publishable, and in which venue?
- Which journal communities are the best match? (JMLR for methods/AutoML, ACL for NLP task focus, or specialized benchmark tracks like NeurIPS Datasets and Benchmarks).
