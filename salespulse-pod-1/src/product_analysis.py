def analyse_products(valid_rows, top_n=5):
    stats = {}
    for r in valid_rows:
        s = stats.setdefault(r["ProductName"], {"revenue": 0.0, "quantity": 0.0})
        s["revenue"] += r["Quantity"] * r["UnitPrice"]
        s["quantity"] += r["Quantity"]

    ranked = sorted(stats.items(), key=lambda kv: (-kv[1]["revenue"], kv[0]))
    top = [(name, s["revenue"]) for name, s in ranked[:top_n]]

    top_qty = None
    if stats:
        best = max(s["quantity"] for s in stats.values())
        top_qty = {"products": sorted(n for n, s in stats.items() if s["quantity"] == best),
                   "quantity": best}
    return {"revenue_by_product": dict(ranked), "top_products": top,
            "highest_quantity": top_qty}
