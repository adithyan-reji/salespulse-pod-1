"""
SalesPulse - Data Validation Module
Checks the sales CSV and reports every invalid row with its reason.

Install dependency:
    pip install pandas

Run from the project root:
    python validation.py
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "OrderID", "ProductName", "Region",
    "Quantity", "UnitPrice", "UnitCost"
]


def validate_sales(data):
    """Return (valid_data, invalid_data, summary) without silently deleting rows."""
    data = data.copy()

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column in ["Quantity", "UnitPrice", "UnitCost"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    reasons = [[] for _ in range(len(data))]

    def add_reason(mask, message):
        for position, is_invalid in enumerate(mask.fillna(True).tolist()):
            if is_invalid:
                reasons[position].append(message)

    add_reason(
        data["OrderID"].isna() | data["OrderID"].astype("string").str.strip().eq(""),
        "Missing Order ID"
    )
    add_reason(
        data["ProductName"].isna() | data["ProductName"].astype("string").str.strip().eq(""),
        "Missing Product Name"
    )
    add_reason(
        data["Region"].isna() | data["Region"].astype("string").str.strip().eq(""),
        "Missing Region"
    )

    add_reason(data["Quantity"].isna(), "Missing or non-numeric Quantity")
    add_reason(data["Quantity"].le(0), "Zero or negative Quantity")
    add_reason(data["UnitPrice"].isna(), "Missing or non-numeric UnitPrice")
    add_reason(data["UnitPrice"].le(0), "Zero or negative UnitPrice")
    add_reason(data["UnitCost"].isna(), "Missing or non-numeric UnitCost")
    add_reason(data["UnitCost"].lt(0), "Negative UnitCost")

    order_id = data["OrderID"].astype("string").str.strip()
    has_order_id = order_id.notna() & order_id.ne("")
    duplicate_ids = order_id[has_order_id].duplicated(keep=False)
    duplicate_mask = pd.Series(False, index=data.index)
    duplicate_mask.loc[order_id[has_order_id].index] = duplicate_ids
    add_reason(duplicate_mask, "Duplicate Order ID")

    data["ValidationReason"] = ["; ".join(row_reasons) for row_reasons in reasons]
    invalid_mask = data["ValidationReason"].ne("")
    valid_data = data.loc[~invalid_mask].copy()
    invalid_data = data.loc[invalid_mask].copy()

    reason_counts = {}
    for row_reasons in reasons:
        for reason in row_reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    summary = {
        "total_records": len(data),
        "valid_records": len(valid_data),
        "invalid_records": len(invalid_data),
        "reason_counts": reason_counts,
    }
    return valid_data, invalid_data, summary


if __name__ == "__main__":
    sales_data = pd.read_csv("data/sales.csv")
    valid_sales, invalid_sales, report = validate_sales(sales_data)

    print("\\n--- DATA QUALITY SUMMARY ---")
    print(f"Total records:   {report['total_records']}")
    print(f"Valid records:   {report['valid_records']}")
    print(f"Invalid records: {report['invalid_records']}")

    print("\\n--- INVALID RECORDS BY REASON ---")
    for reason, count in report["reason_counts"].items():
        print(f"{reason}: {count}")

    print("\\n--- INVALID ROW DETAILS ---")
    if invalid_sales.empty:
        print("No invalid records found.")
    else:
        print(invalid_sales[[
            "OrderID", "ProductName", "Region", "Quantity",
            "UnitPrice", "UnitCost", "ValidationReason"
        ]].to_string(index=False))

    valid_sales.to_csv("valid_sales.csv", index=False)
    invalid_sales.to_csv("invalid_sales.csv", index=False)
    print("\\nSaved valid_sales.csv and invalid_sales.csv")
