from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AuditLog, ActionRequest, RiskAssessment

router = APIRouter(prefix="/api/audit", tags=["Audit"])

@router.get("")
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(ActionRequest).count()
    allowed = db.query(ActionRequest).filter(ActionRequest.status == "allowed").count()
    denied = db.query(ActionRequest).filter(ActionRequest.status == "denied").count()
    pending = db.query(ActionRequest).filter(ActionRequest.status == "approval_required").count()
    high = db.query(RiskAssessment).filter(RiskAssessment.risk_level == "HIGH").count()
    medium = db.query(RiskAssessment).filter(RiskAssessment.risk_level == "MEDIUM").count()
    low = db.query(RiskAssessment).filter(RiskAssessment.risk_level == "LOW").count()
    return {
        "total": total,
        "allowed": allowed,
        "denied": denied,
        "pending": pending,
        "low": low,
        "medium": medium,
        "high": high,
    }
