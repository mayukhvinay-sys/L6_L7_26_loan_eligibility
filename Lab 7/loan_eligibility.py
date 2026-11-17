"""Loan eligibility helpers used in Lab 7 fuzz testing."""

import math

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}


def parse_income(income):
    """Parse a positive monthly income, allowing standard comma grouping."""
    if not isinstance(income, str):
        raise ValueError("income must be text")
    value = income.strip()
    if not value:
        raise ValueError("income cannot be empty")
    if "," in value:
        pieces = value.split(",")
        if not (1 <= len(pieces[0]) <= 3 and pieces[0].isdigit()
                and all(len(piece) == 3 and piece.isdigit() for piece in pieces[1:])):
            raise ValueError("income has invalid comma grouping")
        value = "".join(pieces)
    if not value.isdigit():
        raise ValueError("income must contain digits only")
    amount = int(value)
    if amount <= 0:
        raise ValueError("income must be greater than zero")
    return amount


def monthly_emi(details):
    """Return the monthly EMI for principal, annual rate (%) and term (years)."""
    if not isinstance(details, str):
        raise ValueError("details must be text")
    parts = [part.strip() for part in details.split(",")]
    if len(parts) != 3:
        raise ValueError("expected principal,rate,years")
    try:
        principal, annual_rate, years = (float(part) for part in parts)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("principal, rate and years must be numbers") from None
    if not all(map(math.isfinite, (principal, annual_rate, years))):
        raise ValueError("values must be finite")
    if principal <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("principal and years must be positive; rate cannot be negative")
    months = years * 12
    if not months.is_integer() or months > 1200:
        raise ValueError("term must be a whole number of months (maximum 100 years)")
    n = int(months)
    if annual_rate == 0:
        return round(principal / n, 2)
    monthly_rate = annual_rate / 1200
    # expm1/log1p stay accurate (and non-zero) for extremely small rates, where
    # the naive (1 + r) ** -n form rounds to 1 and divides by zero.
    denominator = -math.expm1(-n * math.log1p(monthly_rate))
    try:
        emi = principal * monthly_rate / denominator
    except ZeroDivisionError:
        emi = principal / n
    if not math.isfinite(emi):
        raise ValueError("EMI is too large to represent")
    return round(emi, 2)


def pan_category(pan):
    """Return the holder category for a structurally valid Indian PAN."""
    if not isinstance(pan, str):
        raise ValueError("PAN must be text")
    pan = pan.strip().upper()
    if len(pan) != 10 or not pan[:3].isalpha() or not pan[:3].isascii():
        raise ValueError("PAN must have 10 characters and start with 3 letters")
    if pan[3] not in CATEGORIES:
        raise ValueError("PAN holder category must be P, C, H or F")
    if not (pan[4].isalpha() and pan[4].isascii() and pan[5:9].isdigit()
            and pan[9].isalpha() and pan[9].isascii()):
        raise ValueError("PAN has an invalid character pattern")
    return CATEGORIES[pan[3]]


def main():
    print("==== Running parse_income ====")
    try:
        result = parse_income(input("Enter monthly income (e.g. 50,000): "))
        print("Income:", result)
        print("\n==== Running monthly_emi ====")
        result = monthly_emi(input("Enter principal,rate,years (e.g. 500000,10,5): "))
        print("Monthly EMI:", result)
        print("\n==== Running pan_category ====")
        result = pan_category(input("Enter a PAN number (e.g. ABCPE1234F): "))
        print("PAN Category:", result)
    except ValueError as exc:
        print("Invalid input:", exc)


if __name__ == "__main__":
    main()
