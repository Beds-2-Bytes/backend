from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.files_database import FileItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function
from security.create_token import create_access_token
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


router = APIRouter(
    prefix="/files",
    tags=["files"],
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
