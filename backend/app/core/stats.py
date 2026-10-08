"""Pure stats helpers (median, USD salary distribution buckets)."""

from __future__ import annotations

BUCKET_WIDTH_USD = 10_000
NUM_BUCKETS = 10

BUCKET_LABELS = [
    "0–10k",
    "10–20k",
    "20–30k",
    "30–40k",
    "40–50k",
    "50–60k",
    "60–70k",
    "70–80k",
    "80–90k",
    "90–100k",
]


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("median requires at least one value")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def distribution_buckets_usd(amounts_usd: list[float]) -> list[dict[str, int | str]]:
    counts = [0] * NUM_BUCKETS
    for amount in amounts_usd:
        index = int(amount // BUCKET_WIDTH_USD)
        if index >= NUM_BUCKETS:
            index = NUM_BUCKETS - 1
        counts[index] += 1
    return [{"range": BUCKET_LABELS[i], "count": counts[i]} for i in range(NUM_BUCKETS)]
