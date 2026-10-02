# Claim Boundary

## SAFE OR POTENTIALLY SAFE CLAIMS

All claims below are conditional on experimental results and bounded by the scope of the literature search conducted.

- **Claim:** "In the literature verified by this review, no included study was found that jointly performs pre-deployment task-level prediction across classical classifiers, fine-tuned encoders, and generative language models while treating output-contract validity and selection regret as first-class outcomes."
  - *Supporting prior-work comparison:* PsyMatrix uses only fine-tuned PLMs. ModelLens uses open-source pretrained models without operational outcomes. LLM routing benchmarks (LLMRouterBench, RouterBench) operate at query level with homogeneous LLM portfolios. auto-sklearn uses classical models without text or LLMs.
  - *Additional evidence required:* Must build and evaluate such a benchmark. Must confirm through deeper search that no industrial or unpublished work addresses this combination.
  - *Confidence level:* Moderate. This is a bounded search finding, not proof of universal nonexistence.

- **Claim:** "This benchmark evaluates the predictability of output contract validity from task characteristics, an outcome not modeled as a predicted variable in the verified prior work."
  - *Supporting prior-work comparison:* Constrained decoding papers (Lazy-k, Koa, grammar-constrained) enforce validity but do not predict it from dataset-level features. PsyMatrix and ModelLens do not model validity. LLM routing benchmarks do not model validity.
  - *Additional evidence required:* Must empirically show that validity failure rates vary across tasks and are predictable from task features.
  - *Confidence level:* Moderate. The gap exists within the verified corpus; it is possible that industrial/application work addresses this.

- **Claim:** "Our approach demonstrates whether task-level predictions can reduce downstream selection regret compared to static portfolio choices across heterogeneous system families."
  - *Supporting prior-work comparison:* LLM routing papers measure query-level regret within LLM pools. No verified paper evaluates task-level regret across families including classical models.
  - *Additional evidence required:* Effect sizes and uncertainty intervals for regret reduction. Negative findings (task features cannot reduce regret) must be reported as a boundary result.
  - *Confidence level:* Low-Moderate (depends entirely on empirical results).

- **Claim:** "The proposed benchmark design explicitly addresses dataset independence concerns identified in PsyMatrix (Monteiro et al., 2024), where 146 datasets were derived from 11 base datasets."
  - *Supporting prior-work comparison:* PsyMatrix reports 146 datasets but these are derived from 11 bases, raising independence concerns for outer-fold evaluation.
  - *Additional evidence required:* Must demonstrate that the proposed study's task selection and evaluation design ensures effective independence (grouping derived variants, preventing cross-fold leakage).
  - *Confidence level:* High (this is a design choice, not an empirical finding).

## PROHIBITED OR UNSUPPORTED CLAIMS

- **"The first algorithm-selection framework"**
  - *Why it's unsafe:* Rice formalized this in 1976. The idea is nearly 50 years old.

- **"The first use of task features for model selection"**
  - *Why it's unsafe:* Standard practice in AutoML for over a decade (auto-sklearn 2015, Auto-WEKA 2013, Brazdil et al. 1994).

- **"The first NLP model recommender"**
  - *Why it's unsafe:* PsyMatrix (Monteiro et al., 2024) explicitly does text-dataset characterization for pretrained model recommendation. ModelLens (Cai et al., 2026) handles text tasks at scale.

- **"The first LLM router"**
  - *Why it's unsafe:* FrugalGPT (2023), RouteLLM (2024), Hybrid LLM (2024), RouterBench (2024), LLMRouterBench (2026), and many others exist.

- **"The first constrained-output classification method"**
  - *Why it's unsafe:* Constrained decoding for classification is well-established (Yu et al. 2022, Lazy-k 2023, Koa 2024, grammar-constrained decoding 2025).

- **"The first heterogeneous AI benchmark"**
  - *Why it's unsafe:* Many benchmarks compare classical vs. deep learning models. The claim must be narrowed to the specific combination of classical + encoder + LLM with validity and regret evaluation, and even then stated as a gap finding within the verified corpus.

- **"Universal superiority of any primitive"**
  - *Why it's unsafe:* The core premise of algorithm selection (Rice 1976) is that no single algorithm dominates.

- **"Generalization beyond bounded single-label decisions"**
  - *Why it's unsafe:* The study is explicitly restricted to bounded-decision systems. Claims about open-ended generation are unsupported by design.

- **"PsyMatrix features are insufficient for model selection"**
  - *Why it's unsafe:* Cannot be claimed without empirical comparison using PsyMatrix features as a baseline.

- **"Novelty has been proven by this literature review"**
  - *Why it's unsafe:* A literature review identifies gaps within the searched corpus. It does not prove that no one has ever done the work.
