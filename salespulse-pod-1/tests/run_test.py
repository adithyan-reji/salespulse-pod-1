import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from validation import validate_sales
from revenue import analyse_revenue

COLS = ["OrderID", "OrderDate", "ProductName", "Category", "Region",
        "Quantity", "UnitPrice", "UnitCost"]
r = lambda oid, p, q, price, cost: [oid, "2026-11-01", p, "X", "West", q, price, cost]
GOOD = r("O1", "Laptop", 2, 50000, 40000)

def run(df):
    valid, _, s = validate_sales(df)
    return s, analyse_revenue(valid.to_dict("records"))

# name, rows, expected valid, expected revenue, expected profit
TESTS = [
    ("TC-01 Normal order", [GOOD], 1, 100000, 20000),
    ("TC-02 Zero quantity", [GOOD, r("O2", "Monitor", 0, 12000, 9000)], 1, 100000, 20000),
    ("TC-03 Negative price", [GOOD, r("O3", "Chair", 3, -5000, 3000)], 1, 100000, 20000),
    ("TC-04 Missing product", [GOOD, r("O4", "", 1, 8000, 6000)], 1, 100000, 20000),
    ("TC-05 Duplicate ID", [GOOD, r("O5", "SSD", 2, 9000, 7000), r("O5", "SSD", 3, 9000, 7000)],
     1, 100000, 20000),
    ("TC-06 Cost > price", [r("O6", "Keyboard", 4, 3000, 3500)], 1, 12000, -2000),
    ("TC-07 No valid orders", [r("O7", "Monitor", 0, 12000, 9000)], 0, 0, 0),
]

out = ["# SalesPulse - Test Results", "", "## Scenario tests", "",
       "| Test | Expected | Actual | Status |", "|---|---|---|---|"]
for name, rows, ev, er, eg in TESTS:
    exp = f"valid={ev}, revenue={er}, profit={eg}"
    try:
        s, m = run(pd.DataFrame(rows, columns=COLS))
        ok = (s["valid_records"], m["total_revenue"], m["total_gross_profit"]) == (ev, er, eg)
        act = (f"valid={s['valid_records']}, revenue={m['total_revenue']}, "
               f"profit={m['total_gross_profit']}, AOV={m['average_order_value']}")
    except Exception as e:
        ok, act = False, f"CRASH {type(e).__name__}: {e}"
    print("PASS" if ok else "FAIL", "|", name, "|", exp, "|", act)
    out.append(f"| {name} | {exp} | {act} | {'Pass' if ok else 'Fail'} |")

out += ["", "## Full dataset (data/sales.csv)", "", "| Check | Expected | Actual | Status |", "|---|---|---|---|"]
s, m = run(pd.read_csv(ROOT / "data" / "sales.csv"))
checks = [("Total records", 120, s["total_records"]), ("Valid records", 108, s["valid_records"]),
          ("Invalid records", 12, s["invalid_records"]),
          ("Duplicate rows", 4, s["reason_counts"].get("Duplicate Order ID")),
          ("Total revenue", 2347050, m["total_revenue"]), ("Valid orders", 108, m["total_orders"]),
          ("AOV", 21731.94, m["average_order_value"]), ("Total quantity", 401, m["total_quantity"]),
          ("Gross profit", 534850, m["total_gross_profit"])]
for name, exp, act in checks:
    ok = act is not None and abs(act - exp) < 0.01
    print("PASS" if ok else "FAIL", "|", name, "|", exp, "|", act)
    out.append(f"| {name} | {exp:,} | {act:,} | {'Pass' if ok else 'Fail'} |")

(ROOT / "tests" / "test-results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("Saved tests/test-results.md")