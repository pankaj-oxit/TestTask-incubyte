"""seed_currency_rates

Revision ID: 002_seed_currency_rates
Revises: 001_create_currency_rates_and_employees
Create Date: 2026-10-07

Inserts fixed exchange rates as of 2024-01-01.
"""

from alembic import op
import sqlalchemy as sa

revision = "002_seed_currency_rates"
down_revision = "001_create_currency_rates_and_employees"
branch_labels = None
depends_on = None

RATES = [
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


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "currency_rates",
            sa.column("currency", sa.String),
            sa.column("rate_to_usd", sa.Float),
        ),
        RATES,
    )


def downgrade() -> None:
    # ANY(:c) is Postgres syntax — this downgrade only runs in migration context, not tests
    currencies = [r["currency"] for r in RATES]
    op.execute(
        sa.text("DELETE FROM currency_rates WHERE currency = ANY(:c)").bindparams(c=currencies)
    )
