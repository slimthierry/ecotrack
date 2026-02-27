import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ActivityCategory(str, enum.Enum):
    TRANSPORT = "transport"
    FOOD = "food"
    ENERGY = "energy"
    PURCHASE = "purchase"


class Activity(Base):
    __tablename__ = "activities"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[ActivityCategory] = mapped_column(
        Enum(ActivityCategory), nullable=False, index=True
    )
    sub_category: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    carbon_kg: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="activities")


class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sub_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    factor_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
