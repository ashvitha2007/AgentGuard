from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Approval, ActionRequest
from ..schemas import ApprovalRequest
from ..auth import get_current_user
from ..services.audit_service import create_audit_log

router = APIRouter(prefix="/api/approvals", tags=["Human Approval"])

@router.get("")
def get_pending_approvals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Approval).filter(Approval.status == "pending").order_by(Approval.created_at.desc()).all()

@router.post("/{approval_id}")
def resolve_approval(
    approval_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    action = db.query(ActionRequest).filter(ActionRequest.id == approval.action_request_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    approval.status = "approved" if request.approved else "rejected"
    approval.resolved_by = user["id"]
    approval.reason = request.reason
    approval.resolved_at = datetime.utcnow()
    action.status = "allowed" if request.approved else "denied"

    db.commit()

    create_audit_log(
        db,
        action.id,
        "HUMAN_APPROVED" if request.approved else "HUMAN_REJECTED",
        request.reason or "No reason supplied",
    )

    return {"success": True, "approval_id": approval.id, "action_status": action.status}
