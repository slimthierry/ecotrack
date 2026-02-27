from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class ChallengeResponse(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    target_carbon_reduction: float
    duration_days: int
    start_date: date
    end_date: date
    is_active: bool
    participants_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ChallengeJoin(BaseModel):
    challenge_id: UUID


class ChallengeProgress(BaseModel):
    challenge_id: UUID
    challenge_title: str
    progress_percent: float
    carbon_saved: float
    completed: bool
    joined_at: date
    days_remaining: int


class LeaderboardEntry(BaseModel):
    username: str
    carbon_saved: float
    rank: int
