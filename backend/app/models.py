from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)
    size = Column(Integer, default=0)
    classification = Column(String(50), default="public")
    uploaded_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ActionRequest(Base):
    __tablename__ = "action_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    target = Column(String(500), nullable=True)
    data_classification = Column(String(100), default="public")
    data_source = Column(String(255), default="user")
    file_id = Column(Integer, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(Integer, primary_key=True)
    action_request_id = Column(Integer, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False)
    injection_detected = Column(Boolean, default=False)
    reasons = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True)
    action_request_id = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")
    reason = Column(Text, nullable=True)
    resolved_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    action_request_id = Column(Integer, nullable=True)
    event = Column(String(255), nullable=False)
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
