# Claim Boundary

## SAFE OR POTENTIALLY SAFE CLAIMS

- **Claim:** "We introduce a benchmark for task-level algorithm selection across fundamentally distinct architectural families (classical, encoder, LLM)."
  - *Supporting prior work:* Auto-WEKA uses classical; RouterBench uses LLMs. None combine them.
  - *Additional evidence required:* Must actually implement and benchmark this diverse portfolio.
  - *Confidence level:* High.

- **Claim:** "This framework evaluates the predictability of output contract validity from task characteristics."
  - *Supporting prior work:* Constrained decoding papers (Lazy-k) measure validity, but do not predict it at the task level from meta-features.
  - *Additional evidence required:* Must show empirical variance in validity across tasks.
  - *Confidence level:* High.

- **Claim:** "Our approach demonstrates whether task-level predictions can reduce downstream selection regret compared to standard static portfolio choices."
  - *Supporting prior work:* LLM routing papers measure regret, but at the query level.
  - *Additional evidence required:* Statistical significance in regret reduction on unseen test datasets.
  - *Confidence level:* Moderate (depends on actual empirical results).

## PROHIBITED OR UNSUPPORTED CLAIMS

- **"The first algorithm-selection framework"**
  - *Why it's unsafe:* Rice formalized this in 1976.
- **"The first use of task features for model selection"**
  - *Why it's unsafe:* Standard practice in AutoML literature for over a decade.
- **"The first NLP model recommender"**
  - *Why it's unsafe:* ModelLens and other NLP meta-learning frameworks already exist.
- **"The first LLM router"**
  - *Why it's unsafe:* Dozens of LLM routers exist (RouterBench, RouteJudge, FrugalGPT, etc.).
- **"The first constrained-output classification method"**
  - *Why it's unsafe:* Heavily researched area (e.g., constrained seq2tree generation, JSON-mode enforced APIs).
- **"The first heterogeneous AI benchmark"**
  - *Why it's unsafe:* Many benchmarks compare classical vs. deep learning models (e.g., TabPFN paper).
- **"Universal superiority of any primitive"**
  - *Why it's unsafe:* The core premise of algorithm selection is that no single model is universally superior.
- **"Generalization beyond bounded single-label decisions"**
  - *Why it's unsafe:* The study is explicitly restricted to bounded-decision systems; expanding to open-ended generation is unsupported by the proposed design.
