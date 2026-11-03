import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


def test_credit_band_boundaries_and_invalid_scores():
    assert credit_band(300) == "poor"
    assert credit_band(549) == "poor"
    assert credit_band(550) == "fair"
    assert credit_band(649) == "fair"
    assert credit_band(650) == "good"
    assert credit_band(749) == "good"
    assert credit_band(750) == "excellent"
    assert credit_band(900) == "excellent"
    with pytest.raises(ValueError):
        credit_band(299)
    with pytest.raises(ValueError):
        credit_band(901)


def test_unknown_employment():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)


def test_age_boundaries():
    assert is_eligible(20, 50000, "salaried", 800) is False
    assert is_eligible(21, 50000, "salaried", 800) is True
    assert is_eligible(60, 50000, "salaried", 800) is True
    assert is_eligible(61, 50000, "salaried", 800) is False


def test_income_branches():
    assert is_eligible(30, 24999, "salaried", 800) is False
    assert is_eligible(30, 25000, "salaried", 800) is True
    assert is_eligible(30, 39999, "self_employed", 800) is False
    assert is_eligible(30, 40000, "self_employed", 800) is True


def test_poor_credit_branch():
    assert is_eligible(30, 50000, "salaried", 500) is False
    assert is_eligible(30, 50000, "salaried", 550) is True


def test_interest_rate_all_branches():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(600, "salaried", False) == 13
    assert interest_rate(600, "self_employed", False) == 14
    assert interest_rate(600, "salaried", True) == 11
    assert interest_rate(600, "self_employed", True) == 12
