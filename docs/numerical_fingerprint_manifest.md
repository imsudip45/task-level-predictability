# Numerical fingerprint manifest

Date: 2026-09-26. Generated from `research/data/fingerprint/fingerprint.json`.

FPS-1 and FPS-2 are unchanged. The schema manifest is unchanged. This file is the measurement record.

No primitive was run. Test files were not read, except that the official PubMedQA script's test half was counted and not tokenized.

Tokenizer: `bert-base-uncased` revision `86b5e0934494bd15c9632b12f734a8a67f723594`.
Label encoder: `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
Normalized entropy is Shannon entropy in nats divided by ln(K). even n: mean of the two central ranks; numpy percentile linear for the reported median and p95.

Scopus was not searched. Semantic Scholar was not searched. Novelty remains **MODIFY**.

ESCI is measured and held out of selector training. The scarcity grid is not in this table.

| Candidate | Train rows | K | Norm. entropy | Max/min | Median tokens | P95 tokens | Mean label cosine | Min label cosine | Relation | Selector training |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| banking77 | 10003 | 77 | 0.9920 | 5.343 | 11.0 | 35.0 | 0.2011 | -0.1309 | utterance | yes |
| clinc_oos_plus | 15250 | 151 | 0.9990 | 2.500 | 9.0 | 15.0 | 0.1342 | -0.1968 | utterance | yes |
| civil_comments_binary | 1804874 | 2 | 0.4021 | 11.505 | 46.0 | 201.0 | 0.5701 | 0.5701 | utterance | yes |
| sms_spam | 4458 | 2 | 0.5681 | 6.467 | 18.0 | 53.0 | 0.2830 | 0.2830 | utterance | yes |
| esci_en_us_task2 | 1393063 | 4 | 0.6228 | 33.310 | 213.0 | 805.0 | 0.2643 | 0.1075 | paired_text | no |
| ledgar | 60000 | 100 | 0.9348 | 137.696 | 104.0 | 379.0 | 0.2194 | -0.1086 | utterance | yes |
| pubmedqa_fold0 | 450 | 3 | 0.8516 | 5.082 | 319.5 | 490.1 | 0.5272 | 0.4000 | paired_text | yes |
| vitaminc | 370653 | 3 | 0.9030 | 3.505 | 45.0 | 89.0 | 0.2113 | 0.1966 | paired_text | yes |

## Notes fixed before these numbers were used

- Banking77's official CSV header is `text`, `category`. The loader calls the second field `label`. The category strings are the labels that were embedded.
- Civil Comments length uses 20,000 training rows drawn with `numpy` `default_rng(20260926)`. Imbalance uses all 1,804,874 training rows. Declared names for the thresholded classes are `nontoxic` and `toxic`.
- ESCI row identity and labels come from the official examples file: English (US), `large_version` 1, `split` train, 1,393,063 rows. Length uses 20,000 of those rows. Product title, description, and bullets for that sample were read from the tasksource copy of those three fields, keyed by product id and locale. The tasksource train split itself was not the row set.
- SMS training size is the 80 percent side. Indices are in `sms_train_indices.json`.
- PubMedQA fold 0 from `split_dataset.py` with `random.seed(0)` is 450 train, 50 dev, 500 test. PMIDs are in `pubmedqa_fold0_train_pmids.json`.
- VitaminC training rows are 370,653, matching Table 2. The article-grouped shift code stays blank.
- `schema_choice` has no candidate.

## Structural codes

| Candidate | Structure | Evidence | External knowledge | Documented shift | Rules |
| --- | --- | --- | --- | --- | --- |
| banking77 | free_text | False | False | none_documented | False |
| clinc_oos_plus | free_text | False | False | unspecified | False |
| civil_comments_binary | free_text | False | False | unspecified | False |
| sms_spam | free_text | False | False | none_documented | True |
| esci_en_us_task2 | text_plus_evidence | True | False | query_grouped | False |
| ledgar | free_text | False | False | unspecified | False |
| pubmedqa_fold0 | text_plus_evidence | True | False | unspecified | False |
| vitaminc | text_plus_evidence | True | False | blank | False |

