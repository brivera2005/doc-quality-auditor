from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class AuditRequest(BaseModel):
    encounter_note: str = Field(..., min_length=20)
    encounter_type: Literal["office", "inpatient", "ed"] = "office"


class MeasureGap(BaseModel):
    measure_id: str
    measure_name: str
    category: str
    status: Literal["pass", "gap"]
    finding: str
    suggested_addendum: Optional[str] = None


class AuditSummary(BaseModel):
    total_measures: int
    passed: int
    gaps: int
    compliance_pct: float


class AuditResponse(BaseModel):
    summary: AuditSummary
    gaps: list[MeasureGap]
    passed: list[MeasureGap]
