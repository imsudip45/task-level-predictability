# Limitations

These limits are part of the frozen pilot. They are also stated in the manuscript.

## Task coverage

Eight tasks. Each family is a singleton: one intent pair is the only within-family contrast, and the other families appear once.

## Primitive coverage

One written rule, scored only on SMS Spam. One Laya checkpoint: `convaiinnovations/laya`, English router. One Qwen checkpoint: `Qwen/Qwen2.5-0.5B-Instruct`. Neither checkpoint represents its model family.

## Hardware

The rule, the classifier, and Laya ran on CPU. Qwen ran in float16 on a GTX 1650 Ti. Latency is deployment-specific. It is not a hardware-normalized comparison.

## Cost

API cost is zero because no API was called. That is an accounting fact, not a comparison against hosted models.

## Classifier

C100k is a capped fit for Civil Comments, VitaminC, and ESCI. Those scores are not full-data classifier scores. The other five tasks are Cfull.

## Statistical scope

The independent unit is the task, not the examples inside a task.

## Domain holdout

ESCI is one e-commerce task, not an e-commerce domain sample. A closer prediction on that holdout did not change the selected primitive.

## Literature

The literature search is incomplete. Scopus was not queried. A Semantic Scholar pass returned HTTP 429.
