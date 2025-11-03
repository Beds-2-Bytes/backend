from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#from app.database import SessionLocal, CartItem
from security.verify import verify_jwt_token
from routers import simulation, users
from database.database import Base, engine
from database.users_database import UserItem
from database.simulation_database import SimulationItem

# Create DB tables and such for sqlalchemy
Base.metadata.create_all(bind=engine)

# Main App instance
app = FastAPI()

# CORS, Allow all requests, types and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Include routes
app.include_router(users.public_router) # /users public
app.include_router(users.protected_router) # /users protected
app.include_router(simulation.router) # /simulations


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Beds2Bytes root!!!"}
