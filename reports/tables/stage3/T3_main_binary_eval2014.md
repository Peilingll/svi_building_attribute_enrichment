# Table 3 — Stage 3 pipeline comparison (binary A-C | D-G, hold-out, n=2014)

| Route | macro-F1 | 95% CI | κ | acc | bal.acc | MCC | ROC-AUC | M3−M1 mF1 | M3−M1 κ |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| M0 | 0.4123 | [0.406, 0.419] | 0.0000 | 0.7016 | 0.5000 | 0.0000 | 0.5000 |  |  |
| M1 | 0.4918 | [0.470, 0.513] | 0.0753 | 0.7026 | 0.5289 | 0.1136 | 0.6463 |  |  |
| M3-DINOv2 | 0.4903 | [0.469, 0.512] | 0.0565 | 0.6892 | 0.5222 | 0.0763 | 0.5816 | -0.0015 | -0.0188 |
| M3-ResNet50 | 0.4878 | [0.466, 0.508] | 0.0465 | 0.6832 | 0.5185 | 0.0609 | 0.5700 | -0.0040 | -0.0288 |
| M3-VLMv3 | 0.5274 | [0.505, 0.549] | 0.0554 | 0.5963 | 0.5282 | 0.0554 | 0.5342 | +0.0356 | -0.0199 |

The pool is 29.8% D-G, so M0 (constant A-C) already scores acc 0.7016. Read accuracy only against M0; macro-F1, balanced accuracy and ROC-AUC are the informative columns.
