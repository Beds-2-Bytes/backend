from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#from app.database import SessionLocal, CartItem
from security.verify import verify_jwt_token
from routers import simulation, users, cases, files
from routers.files import router as file_router
from database.database import Base, engine
from database.users_database import UserItem
from database.simulation_database import SimulationItem
from database.cases_database import CaseItem
from database.files_database import FileItem
from websocket.websocket import router as websocket_router
from pathlib import Path
from config import UPLOAD_DIR

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

# File directories
#UPLOAD_DIR = Path('uploads')
#UPLOAD_DIR.mkdir(exist_ok=True)

# Serve images as static files
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

# Include API routes/endpoints
app.include_router(users.public_router) # /users public
app.include_router(users.protected_router) # /users protected
app.include_router(simulation.router) # /simulations
app.include_router(cases.router) # /cases
app.include_router(file_router) # /files

# Websocket route
app.include_router(websocket_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Beds2Bytes root!!!"}
