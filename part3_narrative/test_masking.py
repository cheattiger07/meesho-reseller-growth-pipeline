import csv
import os

from part3_narrative.masking import (
    alias_for,
    assert_no_raw_names_leak,
)


def test_alias_for():
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"


def test_no_raw_names_leak():
    # Given
    project_root = os.path.dirname(os.path.dirname(__file__))

    narrative_path = os.path.join(
        project_root,
        "part3_narrative",
        "narrative_report.md",
    )

    reseller_path = os.path.join(
        project_root,
        "data",
        "resellers.csv",
    )

    # When
    with open(narrative_path, encoding="utf-8") as file:
        report = file.read()

    start = report.index("# Top Reseller")
    end = report.find("\n#", start + len("# Top Reseller"))

    if end == -1:
        top_reseller_text = report[start:]
    else:
        top_reseller_text = report[start:end]

    reseller_names = []

    with open(
        reseller_path,
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            reseller_names.append(row["reseller_name"])

    # Then
    assert assert_no_raw_names_leak(
        top_reseller_text,
        reseller_names,
    ) is True

    leaked_text = top_reseller_text + " Mumbai Reseller 1"

    assert assert_no_raw_names_leak(
        leaked_text,
        reseller_names,
    ) is False