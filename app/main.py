from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#from app.database import SessionLocal, CartItem
from app.auth import verify_jwt_token
from app.routers import simulation, users

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
app.include_router(users.router)
app.include_router(simulation.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Beds2Bytes root!!!"}
