from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from database.users_database import SessionLocal, UserItem
from security.verify import verify_jwt_token  # Import the verify_jwt_token function
from security.create_token import create_access_token
from passlib.context import CryptContext
from constants import RoleEnum

# Split the endpoints into public and private, eg you have to be able to login and register without authorization
public_router = APIRouter(
    prefix="/users",
    tags=["users-public"],
    responses={404: {"description": "Not found"}},
)

# Add a token verification to verify that user is allowed to a thing
protected_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_jwt_token)],
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

# For being able to send params in the body, not as URL params
class UserCreate(BaseModel):
    username: str = Field(..., example="your_name")
    email: EmailStr = Field(..., example="your_email")
    password: str = Field(..., example="something_clever")
    role: RoleEnum = Field(..., example="student")

# Users root endpoint
@public_router.get("/")
async def root():
    return {'message': "Users root path!, Working maybe!"}

# Register new users endpoint
@public_router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a user within the service. 
    """
    # Check if email already exists
    existing_user = db.query(UserItem).filter(UserItem.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = db.query(UserItem).filter(UserItem.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Hash password before saving
    hashed_pw = pwd_context.hash(user.password)

    new_user = UserItem(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Login user
@public_router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login user, returns a jwttoken"""
    user = db.query(UserItem).filter(UserItem.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "username": user.username,
            "email":user.email,
            "role": user.role
            }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 7200,
        "user": {"name": user.username, "email": user.email, "role": user.role }
    }

# Delete user
@protected_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user based on the users id.
    Params: 
        user_id
    Returns: 
        A message confirming the deletion.
    """
    user = db.query(UserItem).filter(UserItem.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist"
        )
    
    db.delete(user)
    db.commit()

    return {'message': f'User: {user_id} removed'}

# Get all users
@protected_router.get("/all", status_code=status.HTTP_200_OK)
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
