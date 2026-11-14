
import pandas as pd

def calculate_sales_metrics(valid_df):

    valid_df = valid_df.copy()

    valid_df["Revenue"] = (
        valid_df["Quantity"] * valid_df["UnitPrice"]
    )

    valid_df["GrossProfit"] = (
        valid_df["Quantity"] *
        (valid_df["UnitPrice"] - valid_df["UnitCost"])
    )

    total_revenue = valid_df["Revenue"].sum()
    total_orders = len(valid_df)
    total_quantity = valid_df["Quantity"].sum()
    total_profit = valid_df["GrossProfit"].sum()

    if total_orders > 0:
        average_order_value = total_revenue / total_orders
    else:
        average_order_value = 0

    print("\n--- OVERALL SALES METRICS ---")
    print(f"Total Revenue: Rs. {total_revenue:,.2f}")
    print(f"Total Valid Orders: {total_orders}")
    print(f"Average Order Value: Rs. {average_order_value:,.2f}")
    print(f"Total Quantity Sold: {total_quantity}")
    print(f"Estimated Gross Profit: Rs. {total_profit:,.2f}")

    return valid_df
