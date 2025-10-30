from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.users_database import SessionLocal, UserItem
from auth import verify_jwt_token  # Import the verify_jwt_token function
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def root():
    return {'message': "Users root path!, Working maybe!"}

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def register_user(username: str, email:str, password:str, role: str, db: Session = Depends(get_db)):
    
    # Check if email already exists
    existing_user = db.query(UserItem).filter(UserItem.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = db.query(UserItem).filter(UserItem.username == username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Hash password before saving
    hashed_pw = pwd_context.hash(password)

    new_user = UserItem(
        username=username,
        email=email,
        password=hashed_pw,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}

@router.get("/all")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserItem).all()

    if not users:
        return {'message': 'No users'}
    
    user_response = []

    for user in users:
        user_response.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
    
    return user_response
