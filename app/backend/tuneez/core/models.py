from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class BuildProfile(BaseModel):
    craft_type: str = "freestyle"
    frame_size: Optional[str] = None
    frame_model: Optional[str] = None
    prop_size: Optional[str] = None
    prop_pitch: Optional[str] = None
    motor_size: Optional[str] = None
    motor_kv: Optional[int] = None
    esc_firmware: Optional[str] = None
    gyro: Optional[str] = None
    battery_cells: Optional[int] = None
    flight_style: str = "freestyle"
    symptoms: List[str] = Field(default_factory=list)

class Finding(BaseModel):
    title: str
    severity: str
    confidence: float
    evidence: Dict[str, Any] = Field(default_factory=dict)
    why: str
    recommendation: str
    risk: str = "low"

class TuneReport(BaseModel):
    scores: Dict[str, float]
    findings: List[Finding]
    cli: str
    summary: str
