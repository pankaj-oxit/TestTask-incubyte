import pytest

from app.core.reference_data import COUNTRY_CURRENCY_MAP, CURRENCY_RATES
from app.services import currency_service


def test_get_currency_for_country_known():
    assert currency_service.get_currency_for_country("US") == "USD"
    assert currency_service.get_currency_for_country("DE") == "EUR"


def test_get_currency_for_country_unknown_raises():
    with pytest.raises(ValueError, match="Unknown country"):
        currency_service.get_currency_for_country("XX")


def test_validate_currency_for_country_mismatch_raises():
    with pytest.raises(ValueError, match="does not match"):
        currency_service.validate_currency_for_country("US", "EUR")


def test_to_usd_converts_with_fixed_rate():
    # 100_000 USD → 100_000 USD
    assert currency_service.to_usd(100_000, "USD") == 100_000.0
    # 100_000 INR × 0.012 = 1200 USD
    assert currency_service.to_usd(100_000, "INR") == 1200.0


def test_to_usd_unknown_currency_raises():
    with pytest.raises(ValueError, match="No exchange rate"):
        currency_service.to_usd(1, "ZZZ")


def test_service_rates_match_reference_data():
    """DRY: service must not drift from reference_data / migration seed."""
    for country, currency in COUNTRY_CURRENCY_MAP.items():
        assert currency_service.get_currency_for_country(country) == currency
    for currency, rate in CURRENCY_RATES.items():
        assert currency_service.to_usd(1, currency) == round(rate, 2)
