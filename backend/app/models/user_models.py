from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    eco_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_carbon_saved: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    activities = relationship("Activity", back_populates="user", lazy="selectin")
    user_challenges = relationship("UserChallenge", back_populates="user", lazy="selectin")
    user_achievements = relationship("UserAchievement", back_populates="user", lazy="selectin")
