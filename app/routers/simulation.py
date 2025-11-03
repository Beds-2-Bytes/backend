from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.simulation_database import SimulationItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function
from security.create_token import create_access_token
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


router = APIRouter(
    prefix="/simulations",
    tags=["simulations"],
    dependencies=[Depends(verify_jwt_token)],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def root():
    return {'message': "Simulations root path!, Working maybe!"}

class SimulationCreate(BaseModel):
    case_id: int
    name: str
    patient_notes: Optional[str] = None
    passphrase: str = "beds2bytes"
    state: bool = True

# Create simulation
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_simulation(
    data: SimulationCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_jwt_token)
):
    """Create a simulation"""
    user_id = payload.get('sub')
    new_sim = SimulationItem(
        user_id = user_id,
        **data.model_dump()
    )

    db.add(new_sim)
    db.commit()
    db.refresh(new_sim)

    return new_sim

# Get all active simulations
@router.get("/root", status_code=status.HTTP_200_OK)
async def get_all_active_sims(
    db: Session = Depends(get_db)
):
    """Get all active Simulations."""
    active_sims = db.query(SimulationItem).filter(SimulationItem.state == True).all()

    if not active_sims:
        return { "message": "No active simulations found" }
    
    return [
        {
            "id": sim.id,
            "user_id": sim.user_id,
            "case_id": sim.case_id,
            "name": sim.name,
            "patient_notes": sim.patient_notes,
            "state": sim.state,
        }
        for sim in active_sims
    ]


# Get all simulations for a user
@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_simulations(
    db: Session = Depends(get_db), 
    payload: dict = Depends(verify_jwt_token)
):
    """Get all of the users made simulations"""