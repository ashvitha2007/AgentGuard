from .injection_detector import detect_prompt_injection

ACTION_RISK = {
    "read_file": 10,
    "write_file": 25,
    "delete_file": 70,
    "execute_code": 60,
    "api_call": 30,
    "database_read": 30,
    "database_write": 55,
    "external_upload": 70,
    "send_email": 40,
}
DATA_RISK = {
    "public": 0,
    "internal": 15,
    "confidential": 30,
    "sensitive": 45,
    "secret": 60,
}

def calculate_risk(action_type, description, target, data_classification, data_source):
    score = ACTION_RISK.get(action_type, 30)
    reasons = [f"Action risk: +{score}"]

    data_score = DATA_RISK.get(data_classification or "public", 20)
    score += data_score
    if data_score:
        reasons.append(f"Data classification risk: +{data_score}")

    target_lower = (target or "").lower()
    if any(x in target_lower for x in ["http://", "https://", "external", "public-api"]):
        score += 20
        reasons.append("External destination: +20")

    injection = detect_prompt_injection(description)
    if injection["detected"]:
        score += 50
        reasons.append("Prompt injection detected: +50")

    if data_classification in ["sensitive", "secret"] and target_lower and (
        "http" in target_lower or "external" in target_lower
    ):
        score += 30
        reasons.append("Sensitive data sent externally: +30")

    score = min(score, 100)
    level = "LOW" if score < 40 else "MEDIUM" if score < 70 else "HIGH"

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "injection_detected": injection["detected"],
    }
