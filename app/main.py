from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#from app.database import SessionLocal, CartItem
from security.verify import verify_jwt_token
from routers import simulation, users

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

@app.get("/debug")
async def debug_header(authorization: str | None = Header(...)):
    print(f"Authorization header received: {authorization!r}")
    return {"authorization": authorization}

# Include routes
app.include_router(users.public_router) # /users public
app.include_router(users.protected_router) # /users protected
app.include_router(simulation.router) # /simulations

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Beds2Bytes root!!!"}
