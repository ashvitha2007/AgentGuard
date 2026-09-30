def evaluate_policy(risk_score, risk_level, injection_detected, action_type):
    if injection_detected:
        return {"decision": "DENY", "requires_approval": False, "reason": "Prompt injection detected"}

    if risk_score >= 70:
        return {"decision": "DENY", "requires_approval": False, "reason": "Risk exceeds maximum allowed threshold"}

    if risk_score >= 40:
        return {"decision": "REQUIRE_APPROVAL", "requires_approval": True, "reason": "Human approval required"}

    return {"decision": "ALLOW", "requires_approval": False, "reason": "Action satisfies current runtime policy"}
