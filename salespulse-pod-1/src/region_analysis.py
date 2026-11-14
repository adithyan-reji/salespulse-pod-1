def analyse_regions(valid_rows):
    stats = {}

    for r in valid_rows:
        s = stats.setdefault(
            r["Region"],
            {"revenue": 0.0, "gross_profit": 0.0, "orders": 0}
        )

        s["revenue"] += r["Quantity"] * r["UnitPrice"]
        s["gross_profit"] += r["Quantity"] * (
            r["UnitPrice"] - r["UnitCost"]
        )
        s["orders"] += 1

    ranked = sorted(
        stats.items(),
        key=lambda kv: (-kv[1]["revenue"], kv[0])
    )

    best = ranked[0][0] if ranked else None

    return {
        "by_region": dict(ranked),
        "best_region": best
    }
