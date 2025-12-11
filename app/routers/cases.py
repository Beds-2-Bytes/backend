from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.cases_database import CaseItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function
from security.create_token import create_access_token
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


router = APIRouter(
    prefix="/cases",
    tags=["cases"],
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
    return {'message': "Cases root path!, Working maybe!"}

# Get all cases
@router.get("/", status_code=status.HTTP_200_OK)
async def get_cases(
    db: Session = Depends(get_db)
):
    """
    Get all cases
    Returns:
        All cases.
    """
    cases = db.query(CaseItem).all()

    if not cases:
        raise HTTPException(status_code=404, detail="No cases found")

    return [
        {   
            case
        }
        for case in cases
    ]

@router.get("/{case_id}", status_code=status.HTTP_200_OK)
async def get_single_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """Get single case for id"""
    case = db.query(CaseItem).filter(CaseItem.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case found")
    
    return case

# Case model for POST method
class CaseCreate(BaseModel):
    case_name: str
    patient_name: str
    patient_id: str
    base_problem: str
    learning_goals: str
    start_point: str

# Create Case
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_case(
    data: CaseCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_jwt_token)
):
    """
    Create a case to use for a simulation.
    Params:
        Look at example body:
    Returns:
        The Created body is returned.
    """

    user_id = payload.get('sub')
    new_case = CaseItem(
        user_id = user_id,
        **data.model_dump()
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return {
        'message': "Case created successfully",
        'body': new_case
    }

class CaseUpdate(BaseModel):
    case_name: Optional[str] = None
    patient_name: Optional[str] = None
    patient_id: Optional[str] = None
    base_problem: Optional[str] = None
    learning_goals: Optional[str] = None
    start_point: Optional[str] = None

# Edit cases
@router.patch("/{case_id}", status_code=status.HTTP_200_OK)
async def update_case(
    case_id: int,
    updates: CaseUpdate,
    db: Session = Depends(get_db),
):  
    """
    Update a specific and existing case with the case ID.
    Params:
        Check example body.
    """
    case = db.query(CaseItem).filter(CaseItem.id == case_id).first()

    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    # Update only the fields sent, not all
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)

    return {
        "message": f"Case (ID: {case.id} Name: {case.case_name}) updated successfully",
        "fields_updated": updates.model_dump(exclude_unset=True, exclude_none=True),
        "case": case
    }

# DELETE case
@router.delete("/{case_id}", status_code=status.HTTP_200_OK)
async def delete_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a case.
    Params:
        case_id: an integer representing an existing case.
    Returns:
        Nothing
    """
    case = db.query(CaseItem).filter(CaseItem.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db.delete(case)
    db.commit()

    return {
        "message": f"Case (ID: {case.id} Name: {case.case_name}) removed successfully"
    }