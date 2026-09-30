from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import settings
from ..models import UploadedFile
from ..auth import get_current_user

router = APIRouter(prefix="/api/files", tags=["Files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    classification: str = "public",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    allowed = {".txt", ".csv", ".json", ".pdf", ".docx", ".xlsx", ".png", ".jpg", ".jpeg"}
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(status_code=400, detail="File type is not supported by the prototype")

    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="File is too large")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file.filename or "upload.bin").name
    stored = upload_dir / f"{user['id']}_{safe_name}"
    stored.write_bytes(content)

    record = UploadedFile(
        filename=safe_name,
        stored_path=str(stored),
        size=len(content),
        classification=classification,
        uploaded_by=user["id"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "filename": record.filename,
        "size": record.size,
        "classification": record.classification,
    }

@router.get("")
def list_files(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(UploadedFile).order_by(UploadedFile.created_at.desc()).limit(50).all()
