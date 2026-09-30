import json
from ..models import AuditLog

def create_audit_log(db, action_request_id, event, details):
    log = AuditLog(
        action_request_id=action_request_id,
        event=event,
        details=details if isinstance(details, str) else json.dumps(details),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
