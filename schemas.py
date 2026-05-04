from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    normal = "normal"
    warning = "warning"
    fault = "fault"
    offline = "offline"


class ResultEnum(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


# ── Equipment ──────────────────────────────────────

class EquipmentCreate(BaseModel):
    name: str = Field(..., example="RGA-3001")
    brand: str = Field(..., example="DAIHEN")
    model: str = Field(..., example="RGA-3000 Series")
    category: str = Field("RF Generator", example="RF Generator")
    location: str = Field(..., example="Fab A - Chamber 2")
    status: StatusEnum = StatusEnum.normal
    power_output_kw: Optional[float] = Field(None, example=3.0)
    frequency_mhz: Optional[float] = Field(None, example=13.56)


class EquipmentOut(EquipmentCreate):
    id: int
    installed_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Status Update ──────────────────────────────────

class StatusUpdate(BaseModel):
    status: StatusEnum = Field(..., example="warning")


# ── Maintenance Log ────────────────────────────────

class LogCreate(BaseModel):
    action: str = Field(..., example="更換輸出電容")
    description: Optional[str] = Field(None, example="C102電容漏液，更換同規格元件後輸出恢復正常")
    engineer: str = Field(..., example="陳劭泓")
    result: ResultEnum = ResultEnum.success


class LogOut(LogCreate):
    id: int
    equipment_id: int
    logged_at: datetime

    class Config:
        from_attributes = True
