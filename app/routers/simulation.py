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

@router.get("/root")
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

# Get individual Case
@router.get("/{sim_id}", status_code=status.HTTP_200_OK)
async def get_single_sim(
    sim_id: int,
    db: Session = Depends(get_db)
):
    """Get single simulation for id"""
    simulation = db.query(SimulationItem).filter(SimulationItem.id == sim_id).first()

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return simulation

# Get all active simulations
@router.get("/", status_code=status.HTTP_200_OK)
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
            "case": sim.case
        }
        for sim in active_sims
    ]

# Get all simulations for a user
@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user_simulations(
    db: Session = Depends(get_db), 
    payload: dict = Depends(verify_jwt_token)
):
    """Get all of the users made simulations"""
    user_id = int(payload.get('sub'))
    user_sims = db.query(SimulationItem).filter(SimulationItem.user_id == user_id).all()

    if not user_sims:
        raise HTTPException(status_code=404, detail="No simulations found for user")
    
    return [
        {
            "id": sim.id,
            "case_id": sim.case_id,
            "name": sim.name,
            "patient_notes": sim.patient_notes,
            "passphrase": sim.passphrase,
            "state": sim.state
        }
        for sim in user_sims
    ]

class SimUpdate(BaseModel):
    name: Optional[str] = None
    patient_notes: Optional[str] = None
    passphrase: Optional[str] = None
    state: Optional[bool] = None

# Update sims
@router.patch("/{sim_id}", status_code=status.HTTP_200_OK)
async def update_sim(
    sim_id: int,
    updates: SimUpdate,
    db: Session = Depends(get_db),
):
    """Update the sim, mostly meant for deactivating it"""
    sim = db.query(SimulationItem).filter(SimulationItem.id == sim_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    # Update only the fields sent, not all again
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(sim, key, value)
    
    db.commit()
    db.refresh(sim)

    return {
        "message": f"Simulation {sim.name} updated successfully!",
        "simulation": {
            "id": sim.id,
            "case_id": sim.case_id,
            "name": sim.name,
            "patient_notes": sim.patient_notes,
            "passphrase": sim.passphrase,
            "state": sim.state
        }
    }

# Delete sim
@router.delete("/{sim_id}", status_code=status.HTTP_200_OK)
async def delete_sim(
    sim_id: int,
    db: Session = Depends(get_db),
    #payload: dict = Depends(get_db)
):
    """Delete a simulation"""
    #user_id = int(payload.get('sub'))
    sim = db.query(SimulationItem).filter(SimulationItem.id == sim_id).first()

    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    db.delete(sim)
    db.commit()

    return {"message": f"Simulation {sim.name} removed"}
