import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


def test_credit_bands():
    assert credit_band(800) == "excellent"
    assert credit_band(700) == "good"
    assert credit_band(600) == "fair"
    assert credit_band(500) == "poor"


def test_invalid_credit_score():
    with pytest.raises(ValueError):
        credit_band(1000)


def test_eligible_applicant():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_ineligible_low_income():
    assert is_eligible(30, 20000, "salaried", 800) is False


def test_ineligible_poor_credit():
    assert is_eligible(30, 50000, "salaried", 500) is False


def test_interest_rates():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(600, "salaried", False) == 13
    assert interest_rate(600, "self_employed", False) == 14
    assert interest_rate(600, "salaried", True) == 11
