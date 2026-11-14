from pathlib import Path

import pandas as pd

from validation import validate_sales
from revenue import analyse_revenue
from product_analysis import analyse_products
from region_analysis import analyse_regions

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sales.csv"
REPORT_FILE = BASE_DIR / "sales_report.txt"


def money(value):
    return "N/A" if value is None else f"{value:,.2f}"


def build_report(summary, revenue, products, regions, loss_rows):
    lines = []
    line = "=" * 60

    # ---------- Title ----------
    lines += [line, "SALESPULSE SALES REPORT".center(60), line, ""]

    # ---------- 1. Data quality ----------
    lines += ["1. DATA QUALITY SUMMARY", "-" * 60]
    lines.append(f"Total records     : {summary['total_records']}")
    lines.append(f"Valid records     : {summary['valid_records']}")
    lines.append(f"Invalid records   : {summary['invalid_records']}")
    lines.append("Reasons for exclusion (a record can be counted once per reason):")
    for reason, count in summary["reason_counts"].items():
        lines.append(f"  - {reason}: {count}")
    lines.append("Note: all rows sharing a duplicated Order ID are excluded.")
    lines.append(f"Loss-making valid orders (UnitCost > UnitPrice, kept): {len(loss_rows)}")
    lines.append("")

    # ---------- 2. Overall metrics ----------
    lines += ["2. OVERALL SALES METRICS", "-" * 60]
    lines.append(f"Total Revenue          : Rs. {money(revenue['total_revenue'])}")
    lines.append(f"Total Valid Orders     : {revenue['total_orders']}")
    lines.append(f"Average Order Value    : Rs. {money(revenue['average_order_value'])}")
    lines.append(f"Total Quantity Sold    : {revenue['total_quantity']}")
    lines.append(f"Est. Gross Profit      : Rs. {money(revenue['total_gross_profit'])}")
    if revenue["total_revenue"] > 0:
        margin = revenue["total_gross_profit"] / revenue["total_revenue"] * 100
        lines.append(f"Gross Profit Margin    : {margin:.2f}%")
    lines.append("")

    # ---------- 3. Top products ----------
    lines += ["3. TOP 5 PRODUCTS BY REVENUE", "-" * 60]
    if products["top_products"]:
        for rank, (name, amount) in enumerate(products["top_products"], 1):
            lines.append(f"{rank}. {name:<22} Rs. {money(amount)}")
    else:
        lines.append("No valid orders available.")
    hq = products["highest_quantity"]
    if hq:
        lines.append("")
        lines.append(
            f"Highest quantity sold: {', '.join(hq['products'])} ({hq['quantity']:g} units)"
        )
    lines.append("")

    # ---------- 4. Regions ----------
    lines += ["4. REGION-WISE PERFORMANCE", "-" * 60]
    by_region = regions["by_region"]
    ranked = sorted(by_region.items(), key=lambda kv: kv[1]["revenue"], reverse=True)
    lines.append(f"{'Region':<10}{'Revenue':>16}{'Gross Profit':>16}{'Orders':>9}")
    for name, d in ranked:
        lines.append(
            f"{name:<10}{money(d['revenue']):>16}{money(d['gross_profit']):>16}{d['orders']:>9}"
        )
    if regions["best_region"]:
        lines.append(f"\nBest region (by revenue): {regions['best_region']}")
    lines.append("")

    # ---------- 5. Insights (built from the actual results) ----------
    insights = []
    recommendations = []
    total_rev = revenue["total_revenue"]
    top = products["top_products"]

    if top and total_rev > 0:
        best_name, best_amt = top[0]
        share = best_amt / total_rev * 100
        insights.append(
            f"{best_name} is the top product with Rs. {money(best_amt)}, "
            f"{share:.1f}% of total revenue."
        )
        top5_share = sum(a for _, a in top) / total_rev * 100
        insights.append(
            f"The top {len(top)} products together make up {top5_share:.1f}% of revenue."
        )
        recommendations.append(
            f"Keep {best_name} well stocked, since it alone drives {share:.1f}% of revenue."
        )

    if hq:
        names = hq["products"]
        top_names = [n for n, _ in top]
        pos = [top_names.index(n) + 1 for n in names if n in top_names]
        if pos:
            insights.append(
                f"{', '.join(names)} sells the most units ({hq['quantity']:g}) "
                f"but ranks #{pos[0]} by revenue."
            )
        else:
            insights.append(
                f"{', '.join(names)} sells the most units ({hq['quantity']:g}) "
                f"but is outside the top {len(top)} by revenue."
            )

    if ranked and total_rev > 0:
        best_r, best_d = ranked[0]
        worst_r, worst_d = ranked[-1]
        insights.append(
            f"{best_r} leads regional revenue ({best_d['revenue'] / total_rev * 100:.1f}% "
            f"share); {worst_r} is lowest with Rs. {money(worst_d['revenue'])}."
        )
        most_orders = max(ranked, key=lambda kv: kv[1]["orders"])
        if most_orders[0] != best_r:
            insights.append(
                f"{most_orders[0]} has the most orders ({most_orders[1]['orders']}) "
                f"but is not the top region by revenue, so its order value is lower."
            )
        recommendations.append(
            f"Study what works in {best_r} (pricing, promotions) and apply it in {worst_r}, "
            f"the weakest region."
        )

    if total_rev > 0:
        margin = revenue["total_gross_profit"] / total_rev * 100
        insights.append(f"Overall gross profit margin is {margin:.2f}%.")

    if loss_rows:
        insights.append(
            f"{len(loss_rows)} order(s) sell below cost and should be reviewed."
        )
        recommendations.append("Review loss-making orders for pricing errors or discounts.")

    lines += ["5. BUSINESS INSIGHTS", "-" * 60]
    lines += [f"{i}. {t}" for i, t in enumerate(insights, 1)] or ["No insights available."]
    lines.append("")
    lines += ["6. RECOMMENDATIONS FOR THE STORE MANAGER", "-" * 60]
    lines += [f"{i}. {t}" for i, t in enumerate(recommendations, 1)] or ["None."]
    lines.append("")
    return "\n".join(lines)


def main():
    data = pd.read_csv(DATA_FILE)

    valid, invalid, summary = validate_sales(data)

    # Keep the excluded records for transparency
    valid.to_csv(BASE_DIR / "valid_sales.csv", index=False)
    invalid.to_csv(BASE_DIR / "invalid_sales.csv", index=False)

    rows = valid.to_dict("records")
    revenue = analyse_revenue(rows)
    products = analyse_products(rows)
    regions = analyse_regions(rows)

    # Loss-making orders are kept in the analysis but flagged
    loss_rows = [r for r in rows if r["UnitCost"] > r["UnitPrice"]]

    report = build_report(summary, revenue, products, regions, loss_rows)
    print(report)

    REPORT_FILE.write_text(report, encoding="utf-8")
    print("SalesPulse Analysis Completed!")
    print(f"Report saved as {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
