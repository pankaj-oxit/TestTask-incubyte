"""
Currency service — country/currency mapping and USD conversion.
Rates are fixed as of 2024-01-01 and stored in the currency_rates table.
"""

# Maps ISO country code → ISO currency code
# Used to validate that an employee's currency matches their country
COUNTRY_CURRENCY_MAP: dict[str, str] = {
    "US": "USD",
    "IN": "INR",
    "GB": "GBP",
    "DE": "EUR",
    "FR": "EUR",
    "CA": "CAD",
    "AU": "AUD",
    "SG": "SGD",
    "JP": "JPY",
    "BR": "BRL",
}

# Fixed exchange rates as of 2024-01-01: 1 unit of currency = X USD
CURRENCY_RATES: dict[str, float] = {
    "USD": 1.0,
    "INR": 0.012,
    "GBP": 1.27,
    "EUR": 1.09,
    "CAD": 0.74,
    "AUD": 0.65,
    "SGD": 0.74,
    "JPY": 0.0067,
    "BRL": 0.20,
}


def get_currency_for_country(country_code: str) -> str:
    """Return the ISO currency code for a given country. Raises ValueError if unknown."""
    if country_code not in COUNTRY_CURRENCY_MAP:
        raise ValueError(f"Unknown country code: {country_code}")
    return COUNTRY_CURRENCY_MAP[country_code]


def validate_currency_for_country(country_code: str, currency: str) -> None:
    """Raise ValueError if the currency doesn't match the country."""
    expected = get_currency_for_country(country_code)
    if currency != expected:
        raise ValueError(
            f"Currency '{currency}' does not match country '{country_code}' "
            f"(expected '{expected}')"
        )


def to_usd(amount: int, currency: str) -> float:
    """Convert a local currency amount (integer) to USD using fixed rates."""
    if currency not in CURRENCY_RATES:
        raise ValueError(f"No exchange rate for currency: {currency}")
    return round(amount * CURRENCY_RATES[currency], 2)
