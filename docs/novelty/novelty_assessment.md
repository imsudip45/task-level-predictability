# Novelty Assessment

## A. Established ideas
The following ideas are clearly not novel and are well-supported by prior work:
- **Algorithm selection from problem features:** Established since Rice (1976).
- **Dataset meta-features:** Heavily used in AutoML (e.g., Auto-WEKA, Auto-sklearn).
- **Model-performance prediction:** Widely studied (e.g., ModelLens, algorithm runtime prediction).
- **Text-dataset model recommendation:** Explored in NLP dataset characterization (e.g., ModelLens).
- **LLM routing:** Crowded area with multiple benchmarks (RouterBench, LLMRouterBench, RouterArena).
- **Cost-aware routing:** Addressed by almost all recent LLM routing papers.
- **Constrained decoding:** Established method for enforcing structure (e.g., Lazy-k, Koa).
- **Oracle and regret evaluation:** Standard practice in the LLM routing literature.

## B. Potentially distinctive combination
The proposed combination is defensible. While many papers do task-level selection (AutoML) or predict operational outcomes (LLM routing), there is a gap at their intersection. Specifically:
- **Heterogeneous portfolio:** Comparing sparse classical models, encoders, and unconstrained/constrained LLMs in a single selection framework is distinct. LLM routers only route among LLMs; AutoML only selects among classical/pipeline models.
- **Output contract failure as a first-class outcome:** Predicting *whether* a model family will generate valid structure based on task features (e.g., before spending budget on an LLM) is missing from current literature.
- **Task-level vs Query-level:** Recent focus has shifted heavily to query-level LLM routing. Demonstrating that task-level features can reliably predict latency and validity across radically different architectures to reduce regret on untouched tasks is a defensible benchmark contribution.

## C. Strongest novelty threat
The strongest novelty threat is the line of work surrounding **LLMRouterBench (Wu et al., 2026)** and **Latency-Aware LLM Query Routing**. A reviewer might say: *"This has already been done. LLM routing benchmarks already predict quality, cost, and latency, and evaluate selection regret using oracle baselines."*

To survive this threat, the project must differ substantively by proving that incorporating heterogeneous architectures (e.g., TF-IDF + Logistic Regression vs. Llama 3) and output validity constraints at the *task level* introduces fundamental challenges and insights not present in query-level LLM routing. The study must explicitly benchmark simple models against LLMs to justify the portfolio design.

## D. Proposed contribution
This study develops and evaluates a reproducible task-level benchmark for predicting quality, output-contract validity, and operational behavior across heterogeneous bounded-decision implementations, and tests whether these predictions reduce system-selection regret on unseen tasks.

## E. Novelty verdict
**PROCEED WITH REFRAMING**

*Justification:* The core idea of predicting operational behavior to reduce regret is heavily commoditized in the LLM routing space. To proceed, the project must explicitly frame itself *against* query-level homogeneous LLM routing, highlighting the necessity and complexity of cross-family (classical vs. neural vs. LLM) task-level selection and output contract validity. If it remains just another routing benchmark without architectural diversity, it will be rejected as incremental.

## F. Publishability conditions
To make a meaningful journal contribution, the study must demonstrate:
- **Breadth of tasks:** At least 50+ diverse datasets to support robust task-level generalization.
- **Diversity of primitive families:** Must rigorously include classical (e.g., SVM/XGBoost), fine-tuned encoders (e.g., BERT), and LLMs.
- **Output-validity analysis:** Must empirically show that models fail contracts, and that these failures are predictable from task features.
- **Meaningful oracle variation:** The "best" system family must change depending on the task (i.e., LLMs don't just win everything).
- **Strong simple baselines:** Comparisons against simple metadata rules (e.g., dataset size -> model class).
- **Selection-regret improvement:** Demonstrable reduction in cost/latency without sacrificing quality compared to picking the single best-on-average model.
- **Leakage-free evaluation:** Strict train/test splits for tasks, untouched by the meta-model.
- **Value of negative results:** If task features cannot predict validity or latency across families, this must be thoroughly analyzed and presented as a boundary of meta-learning.

## Reviewer 2 challenge
*Reviewer 2:* "The proposed benchmark is unnecessary. We already have Auto-sklearn for classical models and RouterBench/LLMRouterBench for LLMs. Any practitioner simply uses a classical model if they have enough data and tight latency budgets, or an LLM if they have zero-shot needs. Formalizing this into a 'heterogeneous selection framework' is over-engineering a trivial heuristic. Furthermore, task-level features (like dataset size or text length) are too crude to beat simple query-level routing."

## Required response
To answer this criticism, the project must design the benchmark to show that trivial heuristics (e.g., "always use classical if N > 1000" or "always use LLMs for complex tasks") incur massive regret compared to a learned task-level predictor. We must evaluate these exact heuristics as baselines. Furthermore, the output validity constraint must be leveraged to show that LLMs, despite their zero-shot power, predictably fail on certain task distributions, making the meta-selector's decision non-trivial.
