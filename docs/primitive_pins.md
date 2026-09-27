# Execution pin for D and G

Date: 2026-09-26. Written before any decision-model or generative score.

EP-1 is not changed. These are the pins EP-1 requires before D or G is called. The evaluation rows remain the indices already stored under `research/results/raw/`.

## D

Checkpoint: `convaiinnovations/laya`, router model name `english`.

One choice question. The criteria keys are the task's training-set label strings, sorted. Each description is the same string as its key. The instruction is `Which label applies?` The state is the same input string the classifier scored.

Context settings, identical for every task: `max_len=2048`, `head_max_len=1024`. They are not changed after a score.

Load time is stored separately from per-example latency.

## G

Model: `Qwen/Qwen2.5-0.5B-Instruct`. `do_sample` is false. `max_new_tokens` is 32. No API call. API dollars are 0.

The prompt is exactly:

```
Return exactly one valid class label.
Do not explain.

Labels:
{labels, one per line, sorted}

Text:
{input}
```

A prediction is valid only if, after stripping whitespace and one matching pair of surrounding quotes, it equals a legal label. Anything else is invalid and is not a legal class. Invalid rows count in the invalid-output rate and are wrong for macro-F1.

## Not in this pin

No selector. ESCI stays out of selector training. Novelty stays MODIFY.
