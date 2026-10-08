"""
Fixed reference data for countries and exchange rates (as of 2024-01-01).
Used by Alembic seed migration and currency_service — single source of truth.
"""

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

CURRENCY_RATE_ROWS: list[dict[str, str | float]] = [
    {"currency": "USD", "rate_to_usd": 1.0},
    {"currency": "INR", "rate_to_usd": 0.012},
    {"currency": "GBP", "rate_to_usd": 1.27},
    {"currency": "EUR", "rate_to_usd": 1.09},
    {"currency": "CAD", "rate_to_usd": 0.74},
    {"currency": "AUD", "rate_to_usd": 0.65},
    {"currency": "SGD", "rate_to_usd": 0.74},
    {"currency": "JPY", "rate_to_usd": 0.0067},
    {"currency": "BRL", "rate_to_usd": 0.20},
]

CURRENCY_RATES: dict[str, float] = {
    str(row["currency"]): float(row["rate_to_usd"]) for row in CURRENCY_RATE_ROWS
}
