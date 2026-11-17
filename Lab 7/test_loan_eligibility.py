"""Property based and boundary tests for the Lab 7 loan helpers."""
import math
import pytest
from hypothesis import given, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category


@given(st.integers(min_value=1, max_value=10**12))
def test_parse_income_accepts_digits(amount):
    assert parse_income(str(amount)) == amount


@given(st.integers(min_value=1, max_value=10**12))
def test_parse_income_accepts_grouped_amount(amount):
    grouped = f"{amount:,}"
    assert parse_income(grouped) == amount


@given(st.one_of(st.none(), st.integers(), st.text().filter(lambda s: not s.strip().isdigit())))
def test_parse_income_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        parse_income(value)


@given(
    principal=st.floats(min_value=1, max_value=10**9, allow_nan=False, allow_infinity=False),
    rate=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    months=st.integers(min_value=1, max_value=1200),
)
def test_monthly_emi_returns_finite_positive_value(principal, rate, months):
    result = monthly_emi(f"{principal},{rate},{months / 12}")
    assert math.isfinite(result)
    # Interest can only raise the EMI above the zero-interest value
    # (allow 0.01 for rounding to 2 decimals).
    assert result >= round(principal / months, 2) - 0.01


@given(st.one_of(st.none(), st.integers(), st.text().filter(lambda s: s.count(',') != 2)))
def test_monthly_emi_rejects_malformed_details(value):
    with pytest.raises(ValueError):
        monthly_emi(value)


def test_monthly_emi_zero_rate():
    assert monthly_emi("120000,0,1") == 10000.00


@given(category=st.sampled_from(list("PCHF")), letters=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=4, max_size=4), digits=st.text(alphabet="0123456789", min_size=4, max_size=4))
def test_pan_category_returns_expected_category(category, letters, digits):
    pan = "ABC" + category + letters[0] + digits + letters[1]
    assert pan_category(pan) == {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}[category]


@given(st.one_of(st.none(), st.integers(), st.text().filter(lambda s: len(s.strip()) != 10)))
def test_pan_category_rejects_wrong_type_or_length(value):
    with pytest.raises(ValueError):
        pan_category(value)


@given(category=st.sampled_from(list("ABDEG...")))
def test_pan_category_rejects_unknown_holder_code(category):
    with pytest.raises(ValueError):
        pan_category("ABC" + category + "E1234F")


# --- Handout-style "must not crash" fuzz tests: only ValueError is acceptable ---
@given(st.text() | st.none())
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except ValueError:
        pass


@given(st.text() | st.none())
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except ValueError:
        pass
