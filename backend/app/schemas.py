from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class LoginResponse(BaseModel):
    access_token: str
    user: dict

class ActionRequestCreate(BaseModel):
    action_type: str
    description: str
    target: Optional[str] = None
    data_classification: str = "public"
    data_source: str = "user"
    file_id: Optional[int] = None

class ActionResponse(BaseModel):
    action_id: int
    risk_score: float
    risk_level: str
    decision: str
    reasons: list[str]
    injection_detected: bool
    requires_approval: bool

class ApprovalRequest(BaseModel):
    approved: bool
    reason: Optional[str] = None
