from part4_agent.mock_agent_runner import run


CSV_PATH = "part2_engine/fixtures/monthly_category_revenue.csv"


def test_may_scenario():
    # Given
    csv_path = CSV_PATH

    # When
    result = run("May", csv_path, csv_path)

    # Then
    assert result["validation_status"] == "valid"

    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        77.1,
        -23.6,
        -23.48,
    ]

    assert set(result["suppressed_categories"]) == {
        "Beauty & Personal Care",
        "Home & Kitchen",
    }

    assert result["escalated_categories"] == []

    assert result["action_taken"] == "drafted_and_held_for_approval"
def test_june_scenario():
    # Given
    csv_path = CSV_PATH

    # When
    result = run("June", csv_path, csv_path)

    # Then
    assert result["validation_status"] == "valid"

    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        -58.74,
        42.59,
        23.9,
    ]

    assert result["suppressed_categories"] == [
        "Western Wear",
    ]

    # Beauty & Personal Care is not flagged and must appear nowhere.
    assert all(
        item["category"] != "Beauty & Personal Care"
        for item in result["flagged_categories"]
    )
    assert "Beauty & Personal Care" not in result["suppressed_categories"]

    assert result["escalated_categories"] == []

    assert result["action_taken"] == "drafted_and_held_for_approval"
def test_corrupted_feed_hard_stop():
    # Given
    corrupted_path = "part2_engine/fixtures/corrupted_feed.csv"
    monthly_path = CSV_PATH

    # When
    result = run(
        "July",
        monthly_path,
        corrupted_path,
    )

    # Then
    assert result["validation_status"] == "invalid"
    assert result["action_taken"] == "hard_stop"

    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == []
def test_exact_boundary(tmp_path):
    # Given
    previous_csv = tmp_path / "previous.csv"
    current_csv = tmp_path / "current.csv"

    previous_csv.write_text(
        "month,category,revenue,n_orders\n"
        "April,Test Category,100000,10\n"
    )

    current_csv.write_text(
        "month,category,revenue,n_orders\n"
        "May,Test Category,108000,10\n"
    )

    # When
    result = run(
        "May",
        str(previous_csv),
        str(current_csv),
    )

    # Then
    assert result["validation_status"] == "valid"
    assert result["escalated_categories"] == ["Test Category"]
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["action_taken"] == "drafted_and_held_for_approval"