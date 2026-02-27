from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    category: str = Field(..., description="One of: transport, food, energy, purchase")
    sub_category: str = Field(..., description="Sub-category within the main category")
    quantity: float = Field(..., gt=0, description="Amount of activity")
    unit: str = Field(..., description="Unit of measurement (km, kg, kWh, etc.)")
    date: date = Field(..., description="Date of the activity")
    notes: str | None = Field(None, max_length=500, description="Optional notes")


class ActivityResponse(BaseModel):
    id: UUID
    user_id: UUID
    category: str
    sub_category: str
    quantity: float
    unit: str
    carbon_kg: float
    date: date
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ActivitySummary(BaseModel):
    total_carbon: float
    activity_count: int
    date_range_start: date
    date_range_end: date


class CarbonBreakdown(BaseModel):
    transport_percent: float = 0.0
    food_percent: float = 0.0
    energy_percent: float = 0.0
    purchase_percent: float = 0.0
    transport_kg: float = 0.0
    food_kg: float = 0.0
    energy_kg: float = 0.0
    purchase_kg: float = 0.0
    total_kg: float = 0.0
