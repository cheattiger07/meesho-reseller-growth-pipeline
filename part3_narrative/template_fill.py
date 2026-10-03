def fill_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:

    if mom_pct > 0:
        implication = (
            "Implication — Hypothesis: The increase may be linked to "
            "higher demand or promotional activity. The regional manager "
            "should check the promotions and sales activity during the month."
        )
    elif mom_pct < 0:
        implication = (
            "Implication — Hypothesis: The decline may be linked to "
            "lower demand, changes in promotions, or stock availability. "
            "The regional manager should check these areas between the two months."
        )
    else:
        implication = (
            "Implication — Fact: Revenue remained unchanged between "
            "the two months. The regional manager can continue monitoring "
            "the category for further movement."
        )

    return (
        f"Context: Monthly revenue for {category} is compared "
        f"between {prev_month} and {month}, with revenue measured in INR.\n\n"
        f"Insight — Fact: Revenue changed from ₹{previous_revenue:,.2f} "
        f"to ₹{current_revenue:,.2f}, with a MoM change of {mom_pct}%.\n\n"
        f"{implication}"
    )