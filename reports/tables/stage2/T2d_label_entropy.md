# Table 2d - Intra-pand EPC label consistency audit (experimental dataset)

Experimental dataset: **10086** buildings. Buildings linked back to at least one raw residential certificate: **10086**.

Labels normalised A+..A++++ -> A. modal share = fraction of a pand's
certificates carrying its most common label. Oracle ceiling = accuracy of
predicting each pand's modal label scored against a random unit's label.

## All certificates (any year)

- pands with >=1 certificate: **10086**
- pands with >=2 certificates: **5892** (58.4%)
- certificates per pand (all): median 2, mean 3.2, max 235
- among multi-cert pands, >=2 distinct labels: **4541** (77.1% of multi)

| quantity | all pands | multi-cert pands only |
|---|---:|---:|
| mean modal share (oracle acc ceiling) | **0.7915** | 0.6431 |
| median modal share | 1.0000 | 0.5000 |
| p25 modal share | 0.5000 | 0.5000 |
| mean entropy (bits) | 0.5243 | 0.8976 |
| P(latest == modal) | 0.8801 | 0.7948 |
| median intra-pand PF std (kWh/m2.yr) | not applicable | 35.8 |

### by building type

| type | pands | % multi-cert | median n_certs | mean modal share | mean entropy |
|---|---:|---:|---:|---:|---:|
| AB | 8916 | 65.1% | 2 | 0.7668 | 0.5861 |
| TH | 992 | 4.8% | 1 | 0.9877 | 0.0300 |
| SFH | 132 | 0.0% | 1 | 1.0000 | 0.0000 |
| MFH | 46 | 95.7% | 6 | 0.7535 | 0.7112 |

## NTA 8800 era only (reg >= 2021; sensitivity set)

- pands with >=1 certificate: **10086**
- pands with >=2 certificates: **5890** (58.4%)
- certificates per pand (all): median 2, mean 3.2, max 235
- among multi-cert pands, >=2 distinct labels: **4539** (77.1% of multi)

| quantity | all pands | multi-cert pands only |
|---|---:|---:|
| mean modal share (oracle acc ceiling) | **0.7916** | 0.6431 |
| median modal share | 1.0000 | 0.5000 |
| p25 modal share | 0.5000 | 0.5000 |
| mean entropy (bits) | 0.5241 | 0.8975 |
| P(latest == modal) | 0.8801 | 0.7947 |
| median intra-pand PF std (kWh/m2.yr) | not applicable | 35.8 |

### by building type

| type | pands | % multi-cert | median n_certs | mean modal share | mean entropy |
|---|---:|---:|---:|---:|---:|
| AB | 8916 | 65.0% | 2 | 0.7669 | 0.5859 |
| TH | 992 | 4.8% | 1 | 0.9877 | 0.0300 |
| SFH | 132 | 0.0% | 1 | 1.0000 | 0.0000 |
| MFH | 46 | 95.7% | 6 | 0.7535 | 0.7112 |

