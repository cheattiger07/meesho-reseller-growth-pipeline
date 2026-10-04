import csv
import json
import re

from part2_engine.growth_engine import (
    mom_growth,
    is_flagged,
    validate_feed,
)

from part3_narrative.template_fill import fill_template


def read_month_revenue(csv_path: str, month: str) -> dict[str, float]:
    revenue_by_category = {}

    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["month"] == month:
                revenue_by_category[row["category"]] = float(row["revenue"])

    return revenue_by_category


def numbers_are_valid(
    message: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
) -> bool:
    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        message.replace(",", "")
    )

    allowed = {
        round(previous_revenue, 2),
        round(current_revenue, 2),
        round(mom_pct, 2),
    }

    return all(round(float(number), 2) in allowed for number in numbers)


PREVIOUS_MONTH = {
    "May": "April",
    "June": "May",
    "July": "June",
}


def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str
) -> dict:

    # 1. Validate current feed
    valid, errors = validate_feed(current_month_csv)

    # 2. Hard Stop if invalid
    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # 3. Find previous month
    previous_month = PREVIOUS_MONTH[month]

    # 4. Read revenue for both months
    previous_revenue = read_month_revenue(
        previous_month_csv,
        previous_month,
    )

    current_revenue = read_month_revenue(
        current_month_csv,
        month,
    )

    flagged = []
    escalated = []

    # 5. Calculate MoM and classification
    for category in current_revenue:

        if category not in previous_revenue:
            continue

        previous = previous_revenue[category]
        current = current_revenue[category]

        mom_pct = mom_growth(previous, current)
        result = is_flagged(mom_pct)

        if result == "flagged":
            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous,
                "current_revenue": current,
            })

        elif result == "escalate_exact_boundary":
            escalated.append(category)

    # 6. Sort flagged categories by absolute MoM descending
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True,
    )

    # 7. Draft only top 3
    MAX_DRAFTS = 3

    drafted = flagged[:MAX_DRAFTS]

    # 8. Suppress remaining flagged categories
    suppressed = [
        item["category"]
        for item in flagged[MAX_DRAFTS:]
    ]

    # 9. Generate and validate messages
    for item in drafted:

        message = fill_template(
            item["category"],
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
            month,
            previous_month,
        )

        # Output guardrail
        if not numbers_are_valid(
            message,
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
        ):
            raise ValueError(
                f"Output guardrail failed for {item['category']}"
            )

        item["drafted"] = True
        item["message"] = message

    # 10. Return exact required schema
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    result = run(
        "May",
        "part2_engine/fixtures/monthly_category_revenue.csv",
        "part2_engine/fixtures/monthly_category_revenue.csv",
    )

    print(json.dumps(result, indent=2))