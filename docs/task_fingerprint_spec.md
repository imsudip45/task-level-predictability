# Task fingerprint specification

Freeze id: **FPS-1** for measurement rules. Date: 2026-09-26.

**FPS-2**, same day, changes only the candidate list: BFCL-simple is removed. No feature, formula, seed, weight, or primitive mask was added. The scarcity grid is stated as an intervention, which FPS-1 already required and which FPS-2 states as a separate analysis object.

This document defines how a task may be described before any primitive is chosen. It does not report length, imbalance, or label-similarity values, and it does not authorize sampling or training.

The datasets below are a **candidate pilot**, not the final pilot. Eight remain after FPS-2. Scopus has still not been queried. A public ACM Digital Library search on this date did not find the four-way held-out selector; that does not clear the novelty gate. Novelty remains **MODIFY**. A later paper with that selector kills the project.

Schema checks for Banking77, VitaminC, and BFCL are in `schema_validation.md`. Computed fingerprint cells stay empty. No primitive is shown an example until a later gate computes the permitted fingerprint and freezes a manifest.

## Why the candidate list is not balanced

Most of the remaining candidates are ordinary closed-set text classification. The gates already removed multilabel tasks, retrieval stacks, and agent episodes. FPS-2 also removes the only schema-choice task. Under those decisions, several proposed features do not vary:

- External knowledge is not required for any candidate, because tasks that needed a corpus or a source article outside the input were rejected or rewritten so the evidence is inside the input.
- None of the remaining candidates uses a per-example function schema. The relation code `schema_choice` has no task. It stays in the codebook so the protocol is unchanged, and it is unused.
- None is multilabel.

That is a property of the candidate list. It is not a reason to invent ratings so that a feature varies. The candidate pilot is a measurement drill: which pre-registered features can be computed without discretionary choices, and which of them actually differ across these tasks. A feature that is constant is reported as constant. A feature that cannot be computed under this specification is reported as unmeasurable. Neither outcome is repaired by editing the feature after primitive scores exist.

Adding a dataset to fill a missing kind of variation is allowed only as a dated amendment to this freeze, and only before any primitive result exists.

## Information rule

A selector feature has to be fixed from the task contract and the training split alone.

Forbidden in the selector, with no exception for a "diagnostic" model:

- test-set labels, test-set scores, or test-set examples
- any primitive's quality, cost, latency, or error rate
- the benchmark name or dataset id
- a hand rating of difficulty
- a guess about which primitive will win

Train/test divergence uses test inputs. It may be published later as a dataset diagnostic. It is not a selector feature.

Operational cost and latency weights are not properties of Banking77 or LEDGAR. The source papers do not state a latency budget. Those weights are scenarios applied after a performance vector is predicted. They are specified in FPS-1 so they are not chosen to match a winner.

## Feature registry

Instruments, named now:

- Token length uses `bert-base-uncased` WordPiece, without the special tokens added by the tokenizer. The revision hash is written into the research log at the first download, before any primitive run.
- Label-name similarity uses `sentence-transformers/all-MiniLM-L6-v2`. Same revision rule.
- Label strings are lowercased, and underscores and hyphens become spaces. No example text enters the embedding.

| Feature | What is recorded | Where it comes from | Selector |
| --- | --- | --- | --- |
| Output size `K` | Number of legal labels | Task contract | Yes |
| Output size, varying | For BFCL only: median and IQR of the per-example candidate-set size on the training rows | Training split, after the formulation check | Yes, if BFCL remains |
| Class imbalance | Training-split max/min count, and entropy divided by log(K) | Training labels only | Yes |
| Training size | Training rows, and minimum and median rows per class | Training split | Yes |
| Input length | Median and P95 WordPiece tokens on the training input defined below | Training inputs only | Yes |
| Input structure | One of `free_text`, `text_plus_evidence`, `text_plus_schema` | Task contract | Yes |
| Evidence required | Yes or no | Task contract | Yes |
| External knowledge required | Yes only if the label is undefined from the declared input | Annotation instructions | Yes |
| Relation code | `utterance`, `paired_text`, or `schema_choice` | Task contract. This is the reasoning proxy. | Yes |
| Label-name similarity | Mean and minimum pairwise cosine among label names | Label strings only | Yes |
| Documented shift | `none_documented`, `query_grouped`, `temporal`, `domain`, or `unspecified` | Split documentation, not a test statistic | Yes, once the documentation is read |
| Operational scenario | Not a task value. Three weight vectors below | This freeze | Applied after prediction |
| Primitive mask | Which of R, C, D, G are defined for the task | This freeze | Mask, not a score |

Human codes of context dependence as low, medium, or high are not in the selector. Nine tasks cannot support that rating. The relation code is the measurable stand-in: an utterance label, a relation between two texts that are both in the input, or a choice among a schema that is in the input.

### Training input, field by field

The string that is tokenized is fixed here. If a file uses different column names, computation stops and the research log records the amendment before any number is saved.

| Candidate | Training input |
| --- | --- |
| Banking77 | The `text` column of the official training CSV. The loader also has `label`. There is no validation split |
| CLINC150 `plus` | The official training utterance only |
| Civil Comments | Comment text only, after the toxicity score is binarized at 0.5 |
| SMS Spam | The `sms` column on the training side of the split defined below. The label column is `label` and is not part of the input |
| ESCI English (US), Task 2 | Query, then product title, then description, then bullet points, joined by a blank line. English (US) rows only |
| LEDGAR | The official training clause only |
| PubMedQA `pqa_labeled` | `question`, then the context sentences joined by a blank line. Not the Hugging Face pool of 1,000. Fold 0 train file from the official seed-0 script, which has not been generated. Exclude `long_answer`, `final_decision`, mesh terms, and reasoning-prediction fields |
| VitaminC | Fact-verification `claim`, then `evidence`, joined by a blank line. The label field is not part of the input |

Length and imbalance for Civil Comments and ESCI may be estimated from a simple random sample of 20,000 training rows, seed `20260926`, because those training splits are large. That sample is a measurement sample. It is not the evaluation set. Entropy on that draw is stratified only if the implementation samples within classes; the seed and the size stay 20,000 and `20260926`. Label counts for imbalance on those two tasks use the full training split, which is a count, not a model.

No fingerprint statistic is computed on the concatenation of train and test.

### Two different objects

**Static fingerprint.** Describes the task before a primitive is chosen. It contains the features in the registry above, including the official training size and the examples-per-class figures. It is computed once, on the full training split (or the pre-registered 20,000-row measurement sample where that rule already applies). It does not change when an experiment withholds training rows.

**Scarcity intervention.** Asks what happens to each primitive when the training set is artificially reduced. The rates are 1%, 5%, 10%, 25%, and 100% of the training split, stratified by label, seed `20260926`. A rate is infeasible for a task, by arithmetic and before any fit, when the expected count in any class is below 1. Infeasible rates are recorded and skipped. The draw is not repeated until every class appears.

The 100% cell of the intervention is the same training split as the static fingerprint. The 1–25% cells are experiments on that task. They are not additional coordinates of the fingerprint, and they are not chosen after seeing which primitive wins. In the eventual analysis these two objects are reported in separate tables. A model that predicts the primitive may use the static training size. It may not treat "we subsampled to 5%" as if that rate had been a property of the published task.

SMS Spam has no official split. When a split is drawn, it is one stratified 80/20 cut of the 5,574 messages, seed `20260926`. The static fingerprint uses the 80% side. The cut is not drawn in FPS-1. The scarcity intervention, if run, applies only to that 80% side.

### Operational scenarios

These multiply a predicted performance vector. They are not filled in from the datasets.

- Quality only: cost weight 0, latency weight 0.
- Equal weights after min-max normalization within a task.
- Cost and latency each weighted equally with quality.

Normalization constants come from the primitives' measured cost and latency on the training tasks. They are not known yet, and they are not guessed.

### Primitive mask

| Candidate | R | C | D | G |
| --- | --- | --- | --- | --- |
| SMS Spam | Defined. The rule text is written and hashed before any score | Defined | Defined | Defined |
| All other candidates | Not run | Defined | Defined | Defined |

A rule is not added later to a 77-, 100-, or 151-way task because the classifier was weak. Civil Comments does not get a keyword list under this freeze. One rule task is enough to see whether the rule primitive is measurable.

## Definitional cells

These cells come from the task contract and the screening record. Blank cells are not zeros. They are not computed yet.

| Candidate | K | Structure | Evidence in the input | Relation code | External knowledge | Training size | Length, imbalance, label similarity, documented shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Banking77 | 77 | free text | no | utterance | no | 10,003 official training rows. 3,080 test rows. No validation split | Length, imbalance, and label similarity pending. Documented shift: `none_documented` |
| CLINC150 plus | 151 | free text | no | utterance | no | 15,250 training rows on the card | Pending |
| Civil Comments | 2 | free text | no | utterance | no | 1,804,874 training rows before the pilot cap | Pending |
| SMS Spam | 2 | free text | no | utterance | no | Pending the 80/20 cut | Pending |
| ESCI English Task 2 | 4 | text plus evidence | yes, the product text | paired text | no | 1,393,063 English (US) training judgments on the ESCI table | Pending. Held out of selector training |
| LEDGAR | 100 | free text | no | utterance | no | 60,000 training clauses | Pending |
| PubMedQA labeled | 3 | text plus evidence | yes, the context sentences | paired text | no | Fold 0 train file from the official seed-0 script. Not generated. The 1,000-row Hugging Face pool is not the training split | Pending |
| VitaminC fact verification | 3 | text plus evidence | yes | paired text | no | Paper Table 2 train row sums to 370,653 pairs. Dev 63,054. Test 55,197 | Length, imbalance, and label similarity pending. Article-wise split is documented and is not in the shift codebook, so that cell stays blank |

ESCI's fingerprint may be computed. It is not a training row for the selector.

## What the candidate pilot is allowed to conclude

With eight candidate tasks, a fitted selector is a sketch. This protocol does not treat a leave-one-task-out accuracy on these tasks as evidence that the fingerprint generalizes. The allowed conclusions of the measurement drill are:

- the feature was computed under this specification, or it was not
- the feature varies across the candidates, or it does not
- the feature required a judgment that this specification does not allow

Primitive runs, if they happen later, are a separate gate. They do not rewrite the table above.

## Amendment rule

A change to a formula, a field, a seed, a weight, the primitive mask, or the candidate list is a new freeze id. The research log states the change and the reason. A primitive result is not a permitted reason. Discovery that a file uses a different column name is a permitted reason, and it has to be logged before the number is kept.

## Stop condition

If a search finds a study that already selects among a rule, a conventional classifier, a typed decision model, and a generative language model from pre-deployment task features on held-out tasks, this specification is archived and the experiment stops.
