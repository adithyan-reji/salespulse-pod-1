# SalesPulse - Test Results

## Scenario tests

| Test | Expected | Actual | Status |
|---|---|---|---|
| TC-01 Normal order | valid=1, revenue=100000, profit=20000 | valid=1, revenue=100000.0, profit=20000.0, AOV=100000.0 | Pass |
| TC-02 Zero quantity | valid=1, revenue=100000, profit=20000 | valid=1, revenue=100000.0, profit=20000.0, AOV=100000.0 | Pass |
| TC-03 Negative price | valid=1, revenue=100000, profit=20000 | valid=1, revenue=100000.0, profit=20000.0, AOV=100000.0 | Pass |
| TC-04 Missing product | valid=1, revenue=100000, profit=20000 | valid=1, revenue=100000.0, profit=20000.0, AOV=100000.0 | Pass |
| TC-05 Duplicate ID | valid=1, revenue=100000, profit=20000 | valid=1, revenue=100000.0, profit=20000.0, AOV=100000.0 | Pass |
| TC-06 Cost > price | valid=1, revenue=12000, profit=-2000 | valid=1, revenue=12000.0, profit=-2000.0, AOV=12000.0 | Pass |
| TC-07 No valid orders | valid=0, revenue=0, profit=0 | valid=0, revenue=0.0, profit=0.0, AOV=0.0 | Pass |

## Full dataset (data/sales.csv)

| Check | Expected | Actual | Status |
|---|---|---|---|
| Total records | 120 | 120 | Pass |
| Valid records | 108 | 108 | Pass |
| Invalid records | 12 | 12 | Pass |
| Duplicate rows | 4 | 4 | Pass |
| Total revenue | 2,347,050 | 2,347,050.0 | Pass |
| Valid orders | 108 | 108 | Pass |
| AOV | 21,731.94 | 21,731.94 | Pass |
| Total quantity | 401 | 401 | Pass |
| Gross profit | 534,850 | 534,850.0 | Pass |
