import re

PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous instructions",
    r"disregard previous instructions",
    r"bypass security",
    r"disable security",
    r"override policy",
    r"reveal system prompt",
    r"show system prompt",
    r"send confidential data",
    r"send sensitive data",
    r"upload secrets",
    r"exfiltrate",
]

def detect_prompt_injection(text: str):
    text = (text or "").lower()
    matches = [p for p in PATTERNS if re.search(p, text)]
    return {"detected": bool(matches), "patterns": matches}
