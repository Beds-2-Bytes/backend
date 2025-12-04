import shutil
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Header, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.files_database import FileItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function
from security.create_token import create_access_token
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from config import UPLOAD_DIR
from pathlib import Path
from uuid import uuid4

router = APIRouter(
    prefix="/rooms",
    tags=["rooms-images"],
    dependencies=[Depends(verify_jwt_token)],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/root")
async def root():
    return {'message': "Files root path!, Working maybe!"}

@router.post("/{room_id}/images")
async def upload_image(
    room_id: str,
    request: Request,
    file: UploadFile = File(...),
):
    """
    Endpoint to upload image
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are allowed")
    
    room_dir = UPLOAD_DIR / room_id
    room_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix
    filename = f"{uuid4()}{ext}"
    file_path = room_dir / filename

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = request.url_for("images", path=f'{room_id}/{filename}')

    return { 'url': image_url }

@router.get("/{room_id}/images")
async def get_images(
    room_id: str,
    request: Request
):
    """
    Returns all images for a specific room
    """
    room_dir = UPLOAD_DIR / room_id

    if not room_dir.exists() or not room_dir.is_dir():
        return { "room_id": room_id, "images": []}
    
    image_urls = []
    for file_path in room_dir.iterdir():
        if file_path.is_file():
            url = request.url_for("images", path=f"{room_id}/{file_path.name}")
            image_urls.append(url)
    
    return {
        "room_id": room_id,
        "images": image_urls
    }

@router.delete("/{room_id}/images")
async def delete_images(
    room_id: str
):
    room_dir = UPLOAD_DIR / room_id

    if not room_dir.exists() or not room_dir.is_dir():
        return { "room_id": room_id, "deleted": False, "reason": "Room has no images"}
    
    for file_path in room_dir.iterdir():
        if file_path.is_file():
            file_path.unlink()

    room_dir.rmdir()

    return { "room_id": room_id, "deleted": True }