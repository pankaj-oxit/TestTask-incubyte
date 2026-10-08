import pytest

from app.core.stats import distribution_buckets_usd, median


def test_median_odd_count():
    assert median([3.0, 1.0, 2.0]) == 2.0


def test_median_even_count():
    assert median([4.0, 1.0, 2.0, 3.0]) == 2.5


def test_median_single_value():
    assert median([42.0]) == 42.0


def test_median_empty_raises():
    with pytest.raises(ValueError):
        median([])


def test_distribution_buckets_ten_fixed_ranges():
    amounts = [5_000.0, 15_000.0, 95_000.0, 150_000.0]
    buckets = distribution_buckets_usd(amounts)
    assert len(buckets) == 10
    assert buckets[0] == {"range": "0–10k", "count": 1}
    assert buckets[1] == {"range": "10–20k", "count": 1}
    assert buckets[9] == {"range": "90–100k", "count": 2}
    assert sum(b["count"] for b in buckets) == len(amounts)
