import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ActionRequest, RiskAssessment, Approval
from ..schemas import ActionRequestCreate, ActionResponse
from ..auth import get_current_user
from ..services.risk_engine import calculate_risk
from ..services.policy_engine import evaluate_policy
from ..services.audit_service import create_audit_log

router = APIRouter(prefix="/api/actions", tags=["Runtime Governor"])

@router.post("/evaluate", response_model=ActionResponse)
def evaluate_action(
    request: ActionRequestCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    action = ActionRequest(
        user_id=user["id"],
        action_type=request.action_type,
        description=request.description,
        target=request.target,
        data_classification=request.data_classification,
        data_source=request.data_source,
        file_id=request.file_id,
        status="evaluating",
    )
    db.add(action)
    db.commit()
    db.refresh(action)

    risk = calculate_risk(
        request.action_type,
        request.description,
        request.target,
        request.data_classification,
        request.data_source,
    )

    db.add(RiskAssessment(
        action_request_id=action.id,
        risk_score=risk["score"],
        risk_level=risk["level"],
        injection_detected=risk["injection_detected"],
        reasons=json.dumps(risk["reasons"]),
    ))

    policy = evaluate_policy(
        risk["score"], risk["level"], risk["injection_detected"], request.action_type
    )

    decision = policy["decision"]
    if decision == "ALLOW":
        action.status = "allowed"
    elif decision == "DENY":
        action.status = "denied"
    else:
        action.status = "approval_required"
        db.add(Approval(
            action_request_id=action.id,
            status="pending",
            reason=policy["reason"],
        ))

    db.commit()

    create_audit_log(
        db, action.id, "POLICY_EVALUATION",
        {
            "risk_score": risk["score"],
            "risk_level": risk["level"],
            "decision": decision,
            "action_type": request.action_type,
        },
    )

    return ActionResponse(
        action_id=action.id,
        risk_score=risk["score"],
        risk_level=risk["level"],
        decision=decision,
        reasons=risk["reasons"],
        injection_detected=risk["injection_detected"],
        requires_approval=policy["requires_approval"],
    )
