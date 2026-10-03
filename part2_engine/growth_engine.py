import csv
def mom_growth(previous: float, current: float)->float:
    return round(((current - previous) / previous) * 100, 2)
def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    value = abs(mom_pct)
    if value > threshold:
        return "flagged"
    elif value < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"
def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []
    with open(csv_path,newline="") as file:
        reader = csv.DictReader(file)
        for line,row in enumerate(reader, start=2):
            category = row["category"].strip()
            if not category:
                errors.append(f"line {line}: missing category (month={row['month']})")
            revenue = row["revenue"].strip()
            if not revenue:
                errors.append(f"line {line}: missing revenue (category={category})")
            else:
                try:
                    value = float(revenue)
                    if value < 0:
                        errors.append(f"line {line}: negative revenue ({value}) for category={category}")
                except ValueError:
                    errors.append(f"line {line}: revenue not numeric: {revenue!r}")
                
    return len(errors) == 0, errors
