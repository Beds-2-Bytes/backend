from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.users_database import SessionLocal, UserItem
from app.auth import verify_jwt_token  # Import the verify_jwt_token function

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {'message': "Users root path!, Working maybe!"}

