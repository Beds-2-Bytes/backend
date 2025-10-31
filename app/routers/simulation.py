from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.simulation_database import SessionLocal, SimulationItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function

router = APIRouter(
    prefix="/simulations",
    tags=["simulations"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {'message': "Simulations root path!, Working maybe!"}