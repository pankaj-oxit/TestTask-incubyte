from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    # ISO 4217 currency code — primary key
    currency: Mapped[str] = mapped_column(String(3), primary_key=True)
    # How many USD one unit of this currency equals (fixed rates, as of 2024-01-01)
    rate_to_usd: Mapped[float] = mapped_column(Float, nullable=False)
