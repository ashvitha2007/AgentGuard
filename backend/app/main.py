from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .config import settings
from .api import auth, files, actions, approvals, audit

Base.metadata.create_all(bind=engine)
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AgentGuard Runtime Policy Engine",
    version="1.0.0",
    description="Hackathon prototype for runtime governance of AI agent actions.",
)

origins = [x.strip() for x in settings.CORS_ORIGINS.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(actions.router)
app.include_router(approvals.router)
app.include_router(audit.router)

@app.get("/")
def root():
    return {"name": "AgentGuard", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
