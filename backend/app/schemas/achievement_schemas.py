from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AchievementResponse(BaseModel):
    id: UUID
    name: str
    description: str
    icon: str
    criteria_type: str
    criteria_value: float
    created_at: datetime

    model_config = {"from_attributes": True}


class UserAchievementResponse(BaseModel):
    id: UUID
    achievement: AchievementResponse
    unlocked_at: datetime

    model_config = {"from_attributes": True}
