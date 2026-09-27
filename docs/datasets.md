# Datasets

Raw benchmark text is not in this repository. The files under `data/fingerprint/` and `results/raw/` store row identifiers, scores, and the task fingerprint. Label names that define a task may appear there. Example sentences do not.

Download each release yourself into a private `data/raw/` directory. That directory is gitignored. The notes below are the provenance of the frozen measurement.

The classifier cap **C100k** applies when the fingerprint training split has more than 100,000 rows. The draw is stratified. Its generator seed is the first 8 bytes, little-endian, of SHA-256 of `traincap-20260927-{task_id}`. Civil Comments, VitaminC, and ESCI use C100k. The other five tasks are **Cfull**: every fingerprint training row. C100k is a compute limit. It is not a scarcity experiment.

Evaluation rows are at most 1,000 per task, drawn under EP-1 before any fit. Index files store those row identifiers only.

## Banking77

- Source: Hugging Face `PolyAI/banking77` (Casanueva et al., 2020).
- Release: the dataset card's official train and test files. Train 10,003, test 3,080. No validation split.
- Split: official train for the fingerprint and for Cfull; official test as the evaluation pool.
- Transformation: none. The task is 77-way customer intent.
- License: CC BY 4.0.
- Redistribution: raw text is not included.
- Obtain: https://huggingface.co/datasets/PolyAI/banking77

## CLINC150 plus

- Source: Hugging Face `clinc_oos`, configuration `plus` (Larson et al., 2019).
- Release: plus split. Train 15,250, validation 3,100, test 5,500.
- Split: official plus train for the fingerprint and for Cfull. The evaluation pool is the official plus test split.
- Transformation: none. The task is 151-way intent, including the out-of-scope label.
- License: CC BY 3.0, as stated on the Hugging Face dataset card.
- Redistribution: raw text is not included.
- Obtain: https://huggingface.co/datasets/clinc_oos

## Civil Comments

- Source: Hugging Face `google-research-datasets/civil_comments`.
- Release: official train, validation, and test. Train 1,804,874, validation 97,320, test 97,320.
- Split: official train is the fingerprint training split. The classifier is C100k, not the full train split. Evaluation uses the official test split, then the EP-1 cap of 1,000 rows.
- Transformation: binarized at toxicity 0.5 before any primitive was scored. The input is comment text only. Identity fields are not inputs.
- License: CC0, as stated on the Hugging Face dataset card.
- Redistribution: raw text is not included.
- Obtain: https://huggingface.co/datasets/google-research-datasets/civil_comments

## SMS Spam Collection

- Source: UCI SMS Spam Collection.
- Release: the released collection of 5,574 messages. DOI 10.24432/C5CC84. There is no official train/test split.
- Split: one stratified split was drawn once, before any primitive was scored. Training indices are `data/fingerprint/sms_train_indices.json` (4,458 integers). Evaluation indices are the complement, in `results/raw/sms_spam_eval_indices.json`. The classifier is Cfull.
- Transformation: none beyond that stored split. Labels are the collection's spam and ham labels. The written rule is `configs/sms_rule.txt`.
- License: the UCI page displays CC BY 4.0.
- Redistribution: raw text is not included. The rule file is a regular expression, not the message collection.
- Obtain: https://archive.ics.uci.edu/dataset/228/sms+spam+collection

## ESCI English (US), Task 2

- Source: `amazon-science/esci-data`.
- Release: English (US), large version. Filter `product_locale=us`, `large_version=1`. Official examples: train 1,393,063, test 425,762.
- Split: those official example rows. ESCI is held out of every selector fit. The classifier training rows are a C100k subset of the filtered train split. Evaluation rows are an EP-1 draw from the filtered test split.
- Transformation: Task 2, four labels (Exact, Substitute, Complement, Irrelevant). Task 1 ranking is not used. The input joins the query with product title, description, and bullet points. Product text was read from a tasksource copy of those three fields, keyed by product id and locale, because the official products file was not fully downloaded. Row identity stays the official examples file. The tasksource train split was not substituted as the row set.
- License: Apache 2.0.
- Redistribution: raw text is not included.
- Obtain the examples from https://github.com/amazon-science/esci-data. A reader who needs the same product strings must use that tasksource join, keyed by product id and locale.

## LEDGAR (LexGLUE)

- Source: LexGLUE, Hugging Face `lex_glue`, configuration `ledgar` (Chalkidis et al., 2021).
- Release: official train 60,000, validation 10,000, test 10,000.
- Split: official train for the fingerprint and for Cfull. Evaluation uses the official test split, then the EP-1 cap.
- Transformation: none. The task is 100-way clause type.
- License: CC BY 4.0 on the LexGLUE dataset card.
- Redistribution: raw text is not included.
- Obtain: https://huggingface.co/datasets/lex_glue

## PubMedQA

- Source: Hugging Face `qiaojin/PubMedQA`, configuration `pqa_labeled` (Jin et al., 2019).
- Release: 1,000 expert-labeled examples. The artificial split is excluded. `pqa_artificial` is excluded.
- Split: training rows are fold 0 of the official seed-0 split, 450 rows, not the undivided 1,000-row pool. Those training PMIDs are `data/fingerprint/pubmedqa_fold0_train_pmids.json`. Evaluation uses the 500-row test half of `split_dataset.py` with `random.seed(0)`. The classifier is Cfull.
- Transformation: the input joins the question with the abstract context. A question-only run is a different task.
- License: MIT, as stated on the Hugging Face dataset card.
- Redistribution: raw text is not included. The PMID list is a set of row identifiers.
- Obtain: https://huggingface.co/datasets/qiaojin/PubMedQA

## VitaminC

- Source: VitaminC fact verification (Schuster et al., 2021).
- Release: train 370,653, dev 63,054, test 55,197 pairs, from the paper's Table 2.
- Split: official train for the fingerprint. The classifier is C100k. Evaluation rows are drawn from `vitaminc/test.jsonl` in the fact-verification release.
- Transformation: the input is the claim joined with the provided evidence. A claim-only run is a different task.
- License: data CC BY-SA 3.0. Accompanying code MIT.
- Redistribution: raw text is not included.
- Obtain: the release linked from the VitaminC paper, https://github.com/TalSchuster/VitaminC
