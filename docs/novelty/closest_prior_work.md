# Closest Prior Work

## 1. LLMRouterBench: A Large-scale Benchmark for LLM Routing (Wu et al., 2026)
1. **Question:** How do different routing strategies balance performance and cost across diverse LLMs?
2. **Data:** 400,000+ instances across 21 text datasets.
3. **Candidate systems:** 33 LLMs.
4. **Features:** Query embeddings.
5. **Outcomes:** Accuracy, latency, cost.
6. **Generalization:** Held-out queries.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes.
9. **Validity modeled:** No.
10. **Overlap:** Predicts quality, cost, and latency; evaluates regret.
11. **Remaining gap:** Operates purely at the query level for homogeneous systems (LLMs only) and does not model output contract validity.
12. **Novelty impact:** High. Demonstrates that latency/cost-aware routing is an established topic, meaning the proposed work must differentiate heavily on the task-level and heterogeneous portfolio aspects.

## 2. RouterBench: A Benchmark for Multi-LLM Routing Systems (Ding et al., 2024)
1. **Question:** Can a theoretical framework and dataset effectively benchmark multi-LLM routers?
2. **Data:** 405k inference outcomes.
3. **Candidate systems:** LLMs.
4. **Features:** Query characteristics.
5. **Outcomes:** Accuracy, cost.
6. **Generalization:** Held-out queries.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes.
9. **Validity modeled:** No.
10. **Overlap:** Evaluates routing systems and selection regret.
11. **Remaining gap:** Lacks classical/encoder system portfolios and validity guarantees; task-level evaluation is missing.
12. **Novelty impact:** High. Similar to LLMRouterBench, requires shifting the contribution firmly to task-level heterogeneity.

## 3. RouteJudge: An Online Pairwise Preference Evaluation Framework for LLM Routers (Katz et al., 2026)
1. **Question:** How to evaluate routers online using pairwise preferences incorporating cost and latency?
2. **Data:** Online user preference data.
3. **Candidate systems:** LLMs.
4. **Features:** Task metadata, query text.
5. **Outcomes:** Preference, cost, latency.
6. **Generalization:** Online deployment.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes.
9. **Validity modeled:** No.
10. **Overlap:** Includes task metadata as features, predicts latency and cost.
11. **Remaining gap:** Output validity is ignored; focuses on online preference rather than strict task-level zero-shot algorithm selection across heterogeneous families.
12. **Novelty impact:** Moderate.

## 4. ModelLens: A Latent Space Model for Performance Prediction (Jiang et al., 2024)
1. **Question:** Can we predict foundation model performance on unseen tasks using historical interaction patterns?
2. **Data:** Public leaderboard records.
3. **Candidate systems:** Foundation models.
4. **Features:** Interaction patterns/latent space.
5. **Outcomes:** Performance (Accuracy).
6. **Generalization:** Held-out tasks.
7. **Selection:** Task-level.
8. **Regret evaluated:** No.
9. **Validity modeled:** No.
10. **Overlap:** Task-level prediction of performance on unseen tasks.
11. **Remaining gap:** Does not handle cost, latency, validity, or a heterogeneous portfolio containing small deterministic models.
12. **Novelty impact:** Moderate. Solves the task-level prediction problem but is restricted to accuracy for foundation models.

## 5. Beyond Accuracy and Cost: Latency-Aware LLM Query Routing (2024)
1. **Question:** How to jointly optimize accuracy, cost, and latency in LLM routing?
2. **Data:** Dynamic workloads.
3. **Candidate systems:** LLMs.
4. **Features:** Queries.
5. **Outcomes:** Accuracy, latency, cost.
6. **Generalization:** Held-out queries in dynamic distributions.
7. **Selection:** Query-level.
8. **Regret evaluated:** Yes.
9. **Validity modeled:** No.
10. **Overlap:** Full operational behavior prediction (latency, cost, accuracy).
11. **Remaining gap:** Query-level routing of homogeneous systems without output validity constraints.
12. **Novelty impact:** High. Forces the proposed project to prove that task-level latency prediction for non-LLMs is fundamentally distinct.

### Comparison Table

| Paper | Selection unit | Candidate portfolio | Predicted outcomes | Validity modeled? | Regret evaluated? | Main overlap | Remaining gap |
|---|---|---|---|---|---|---|---|
| Wu et al. | Query | LLMs | Quality, Latency, Cost | No | Yes | Cost/latency prediction, regret | Query-level, homogeneous, no validity |
| Ding et al. | Query | LLMs | Quality, Cost | No | Yes | Router benchmarking, regret | Query-level, homogeneous, no validity |
| Katz et al. | Query | LLMs | Preference, Latency, Cost | No | Yes | Cost/latency, task metadata | Online focus, homogeneous, no validity |
| Jiang et al. | Task | Foundation Models | Quality | No | No | Task-level prediction | No operational behavior or validity |
| Beyond Accuracy | Query | LLMs | Quality, Latency, Cost | No | Yes | Latency prediction | Query-level, homogeneous, no validity |
