from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    eco_score: int
    total_carbon_saved: float
    streak_days: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfile(UserResponse):
    total_activities: int = 0
    active_challenges: int = 0
    achievements_unlocked: int = 0
    carbon_saved_this_week: float = 0.0
    carbon_saved_this_month: float = 0.0

    model_config = {"from_attributes": True}
