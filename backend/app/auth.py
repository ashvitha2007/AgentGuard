from datetime import datetime, timedelta
import jwt
from fastapi import Header, HTTPException
from .config import settings

DEMO_USER = {
    "id": 1,
    "email": "admin@agentguard.com",
    "name": "AgentGuard Admin",
    "password": "admin123",
    "role": "admin",
}

def create_token():
    payload = {
        "sub": str(DEMO_USER["id"]),
        "email": DEMO_USER["email"],
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def authenticate(email: str, password: str):
    if email.lower() == DEMO_USER["email"] and password == DEMO_USER["password"]:
        return {"id": DEMO_USER["id"], "email": DEMO_USER["email"], "name": DEMO_USER["name"], "role": DEMO_USER["role"]}
    return None

def get_current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return {"id": int(payload["sub"]), "email": payload["email"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
