from fastapi import APIRouter, HTTPException
from ..schemas import LoginRequest, LoginResponse
from ..auth import authenticate, create_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = authenticate(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_token(), "user": user}
