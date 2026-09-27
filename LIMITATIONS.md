# Limitations

This is an eight-task measurement pilot.

- Each task family is a singleton: one intent pair is the only within-family contrast, and the other families appear once.
- One written rule is scored, and only on SMS Spam.
- One Laya checkpoint is scored: `convaiinnovations/laya`, English router. It does not represent the Laya family.
- One Qwen checkpoint is scored: `Qwen/Qwen2.5-0.5B-Instruct`. It does not represent the Qwen family.
- Latency is device-specific. The rule, the classifier, and Laya ran on CPU. Qwen ran in float16 on a GTX 1650 Ti. Those latencies are not hardware-normalized.
- API dollars are zero because no API was called. That is an accounting fact, not a cost comparison against hosted models.
- Civil Comments, VitaminC, and ESCI use the C100k classifier cap. Those scores are not full-data classifier scores.
- The literature search is incomplete. Scopus was not queried. A Semantic Scholar pass returned HTTP 429.
- ESCI is one held-out e-commerce task. A closer error on that task did not change the selected primitive.
