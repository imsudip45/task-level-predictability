# Performance matrix

Date: 2026-09-26. Generated from performance_p0_p1.json and performance_dg.json.

Each cell is one task-primitive pair. A blank pair was not eligible. Nothing here was filled with zero to mean unmeasured.

Q is macro-F1. C is local train seconds, local inference seconds, and API dollars. API dollars are 0 because no API was called. L is per-example p50 and p95 in milliseconds and does not include model load.

R, C, and D ran on CPU. G ran on the GTX 1650 Ti in float16. Latencies are not a single-hardware comparison.

C100k is the pre-registered 100,000-row fit. It is not the full-training classifier.

| Task | Primitive | Q | Train s | Infer s | API USD | p50 ms | p95 ms | Invalid | Eval n | Device |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| sms_spam | R | 0.8576 | 0.000 | 0.028 | 0.0 | 0.020 | 0.062 | 0 | 1000 | cpu |
| sms_spam | Cfull | 0.9393 | 0.295 | 0.351 | 0.0 | 0.188 | 0.719 | 0 | 1000 | cpu |
| sms_spam | D | 0.7822 | 0.000 | 724.349 | 0.0 | 698.724 | 941.798 | 0 | 1000 | cpu |
| sms_spam | G | 0.2067 | 0.000 | 308.276 | 0.0 | 323.515 | 417.066 | 25 | 1000 | cuda |
| pubmedqa_fold0 | Cfull | 0.2691 | 0.635 | 0.194 | 0.0 | 0.261 | 0.623 | 0 | 500 | cpu |
| pubmedqa_fold0 | D | 0.3128 | 0.000 | 1019.183 | 0.0 | 1978.849 | 2842.361 | 0 | 500 | cpu |
| pubmedqa_fold0 | G | 0.2327 | 0.000 | 474.746 | 0.0 | 932.252 | 1239.578 | 174 | 500 | cuda |
| banking77 | Cfull | 0.8508 | 2.412 | 0.267 | 0.0 | 0.184 | 0.456 | 0 | 1000 | cpu |
| banking77 | D | 0.3888 | 0.000 | 5260.039 | 0.0 | 5212.193 | 5888.881 | 0 | 1000 | cpu |
| banking77 | G | 0.1316 | 0.000 | 1360.532 | 0.0 | 1274.864 | 1668.698 | 514 | 1000 | cuda |
| clinc_oos_plus | Cfull | 0.8299 | 5.033 | 0.237 | 0.0 | 0.177 | 0.337 | 0 | 1000 | cpu |
| clinc_oos_plus | D | 0.4280 | 0.000 | 4614.129 | 0.0 | 4584.007 | 4905.017 | 0 | 1000 | cpu |
| clinc_oos_plus | G | 0.2465 | 0.000 | 1455.811 | 0.0 | 1336.641 | 1980.492 | 745 | 1000 | cuda |
| ledgar | Cfull | 0.7418 | 139.867 | 0.298 | 0.0 | 0.215 | 0.481 | 0 | 1000 | cpu |
| ledgar | D | 0.2088 | 0.000 | 4724.659 | 0.0 | 4528.972 | 6190.025 | 0 | 1000 | cpu |
| ledgar | G | 0.0281 | 0.000 | 1346.729 | 0.0 | 1236.580 | 1887.759 | 86 | 1000 | cuda |
| civil_comments_binary | C100k | 0.6298 | 19.757 | 0.316 | 0.0 | 0.196 | 0.628 | 0 | 1000 | cpu |
| civil_comments_binary | D | 0.7367 | 0.000 | 807.656 | 0.0 | 726.485 | 1376.470 | 0 | 1000 | cpu |
| civil_comments_binary | G | 0.0000 | 0.000 | 544.926 | 0.0 | 489.657 | 808.857 | 1000 | 1000 | cuda |
| vitaminc | C100k | 0.3826 | 15.300 | 0.251 | 0.0 | 0.176 | 0.416 | 0 | 1000 | cpu |
| vitaminc | D | 0.2165 | 0.000 | 797.699 | 0.0 | 766.750 | 1045.356 | 0 | 1000 | cpu |
| vitaminc | G | 0.2209 | 0.000 | 603.543 | 0.0 | 578.279 | 779.076 | 23 | 1000 | cuda |
| esci_en_us_task2 | C100k | 0.2189 | 77.896 | 0.253 | 0.0 | 0.181 | 0.394 | 0 | 1000 | cpu |
| esci_en_us_task2 | D | 0.1527 | 0.000 | 1909.519 | 0.0 | 1444.679 | 4742.117 | 0 | 1000 | cpu |
| esci_en_us_task2 | G | 0.0358 | 0.000 | 1024.658 | 0.0 | 922.247 | 2060.757 | 32 | 1000 | cuda |

ESCI rows are measurements. They are not selector-training rows. No selector was fit. Novelty remains MODIFY.

