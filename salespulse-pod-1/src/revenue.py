def analyse_revenue(valid_rows):

    total_revenue = 0.0
    total_orders = 0
    total_quantity = 0
    total_gross_profit = 0.0

    for r in valid_rows:

        quantity = r["Quantity"]
        unit_price = r["UnitPrice"]
        unit_cost = r["UnitCost"]

        total_revenue += quantity * unit_price

        total_orders += 1

        total_quantity += quantity

        total_gross_profit += quantity * (unit_price - unit_cost)

    if total_orders > 0:
        average_order_value = total_revenue / total_orders
    else:
        average_order_value = 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "average_order_value": round(average_order_value, 2),
        "total_quantity": total_quantity,
        "total_gross_profit": round(total_gross_profit, 2)
    }
