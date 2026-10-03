import os
from part2_engine.growth_engine import(
    mom_growth,
    is_flagged,
    validate_feed,
)


def test_april_to_may_ethnic_wear():
    # Given
    previous = 104520.77
    current = 185107.61

    # When
    growth = mom_growth(previous, current)

    # Then
    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


def test_may_to_june_beauty():
    # Given
    previous = 35542.11
    current = 37559.07

    # When
    growth = mom_growth(previous, current)

    # Then
    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


def test_exact_boundary():
    # Given
    previous = 100.0
    current = 108.0

    # When
    growth = mom_growth(previous, current)

    # Then
    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"


def test_validate_feed():
    #Given
    fixture_path = os.path.join(os.path.dirname(__file__),
                            "fixtures","corrupted_feed.csv"
    )
    # When
    valid,errors= validate_feed(fixture_path)
    #Then
    assert valid is False
    assert len(errors) == 3
    assert errors == [
    "line 3: negative revenue (-4200.0) for category=Western Wear",
    "line 4: missing category (month=July)",
    "line 6: missing revenue (category=Home & Kitchen)",
    ]
def test_valid_feed():
    # Given
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "monthly_category_revenue.csv",
    )

    # When
    valid, errors = validate_feed(fixture_path)

    # Then
    assert valid is True
    assert errors == []
