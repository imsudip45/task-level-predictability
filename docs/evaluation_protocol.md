# Evaluation protocol

Freeze id: **EP-1**. Date: 2026-09-26.

The numerical fingerprint manifest is frozen and is not edited by this protocol. FPS-1 and FPS-2 are not edited. Novelty stays **MODIFY**. Scopus was not searched. Semantic Scholar was not searched.

This protocol defines how a primitive is scored. It does not train a selector. A selector is not licensed until a performance vector exists for every eligible pair that this protocol marks as executable.

## What is measured

For each eligible task and primitive,

\[
Y_{t,p} = (Q_{t,p}, C_{t,p}, L_{t,p})
\]

- \(Q\): macro-F1 on the frozen evaluation rows. Accuracy is stored beside it and is not the primary quality number.
- \(C\): local training seconds, local inference seconds, and API dollars. API dollars are 0 when nothing is called. No dollar figure is invented for a model that was not called.
- \(L\): per-example prediction latency on the evaluation rows, p50 and p95, in milliseconds. Model load time is stored separately and is not inside \(L\).

Every primitive on a task sees the same evaluation rows and the same input string defined in the schema manifest.

## Eligible pairs

| Primitive | Tasks |
| --- | --- |
| R, rule | SMS Spam only |
| C, conventional classifier | All eight candidates, including ESCI |
| D, typed decision model | All eight, when a pinned local checkpoint is actually loaded |
| G, generative model | All eight, when a pinned local or API model is actually called |

ESCI is scored. Its rows do not enter selector training. This protocol does not fit a selector.

This execution pass runs R and C. D and G are specified and not executed. Their cells are missing, not zero. No endpoint and no decision-model checkpoint were loaded before scores were produced.

## Frozen rows

Evaluation rows are drawn before any fit, with an independent generator per task:

`numpy.random.default_rng` seeded by the first 8 bytes of SHA-256 of `eval-20260926-{task_id}`, little-endian.

If the official test side has at most 1,000 rows, all of them are used. If it has more, 1,000 rows are drawn without replacement.

| Task | Test side |
| --- | --- |
| Banking77 | Official test CSV, 3,080 rows |
| CLINC150 plus | Official plus test split |
| Civil Comments | Official test split, label `toxicity >= 0.5`, input `text` only |
| SMS Spam | Rows whose indices are absent from `sms_train_indices.json` |
| ESCI | Official examples with `product_locale=us`, `large_version=1`, `split=test` |
| LEDGAR | Official test split |
| PubMedQA | The 500-row test half of `split_dataset.py` with `random.seed(0)` |
| VitaminC | `vitaminc/test.jsonl` in the fact-verification zip |

Training rows for C are the fingerprint training rows. When that count is above 100,000, C is fit on a stratified 100,000-row subset. The generator seed is the first 8 bytes of SHA-256 of `traincap-20260927-{task_id}`. Within each class the draw is without replacement, and class counts are the largest integers proportional to the class that sum to 100,000. This cap is named **C100k**. It is a compute limit. It is not the scarcity intervention, and it is not the full-data classifier. Banking77, CLINC150 plus, SMS Spam, LEDGAR, and PubMedQA fold 0 are at or below 100,000 and are fit on every fingerprint training row. Those runs are named **Cfull**.

## Classifier

Same object on every task:

- `TfidfVectorizer`, word unigrams and bigrams, `min_df=2`, `max_features=30000`, `sublinear_tf=True`
- `LogisticRegression`, `solver=saga`, `C=1.0`, `max_iter=200`

No task-specific retuning after a score is seen.

## SMS rule

The rule file is `research/configs/sms_rule.txt`. SHA-256 of its bytes, including the trailing newline:

`264e288b89a430005de7b72fdfeb77862e46b23b7415c76df285e4e5e1a7f992`

The compiled expression is those bytes decoded as UTF-8 with one trailing newline removed. A message is spam if the expression matches, and ham otherwise. The file is not edited after this hash. The rule is not fit on labels.

## What this pass does not claim

Seven selector-training tasks, with rules on one of them, cannot support a generalization claim. The output of this pass is a partial performance table for R and C.
