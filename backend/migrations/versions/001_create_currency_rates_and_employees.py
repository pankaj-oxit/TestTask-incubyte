"""create_currency_rates_and_employees

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-07

Creates:
- currency_rates table
- employees table with all indexes
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- currency_rates ---
    op.create_table(
        "currency_rates",
        sa.Column("currency", sa.String(3), primary_key=True),
        sa.Column("rate_to_usd", sa.Float(), nullable=False),
    )

    # --- employees ---
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("employee_code", sa.String(20), unique=True, nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("job_title", sa.String(100), nullable=False),
        sa.Column("department", sa.String(100), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        # Annual salary in local currency; stored as integer to avoid float rounding bugs
        sa.Column("annual_salary", sa.Integer(), nullable=False),
        sa.Column("hire_date", sa.Date(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

    # Individual column indexes (id PK index created automatically by Postgres — skip)
    op.create_index("ix_employees_country_code", "employees", ["country_code"])
    op.create_index("ix_employees_job_title", "employees", ["job_title"])
    op.create_index("ix_employees_department", "employees", ["department"])
    op.create_index("ix_employees_last_name", "employees", ["last_name"])

    # Composite index for the most common insights query pattern
    op.create_index(
        "ix_employees_country_job", "employees", ["country_code", "job_title"]
    )


def downgrade() -> None:
    op.drop_index("ix_employees_country_job", table_name="employees")
    op.drop_index("ix_employees_last_name", table_name="employees")
    op.drop_index("ix_employees_department", table_name="employees")
    op.drop_index("ix_employees_job_title", table_name="employees")
    op.drop_index("ix_employees_country_code", table_name="employees")
    op.drop_table("employees")
    op.drop_table("currency_rates")
