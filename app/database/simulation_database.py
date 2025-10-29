from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@postgresql/{os.getenv('DBNAME')}"

# Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Simulation Item Model
class SimulationItem(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Associate created simulation with a user
    case_id = Column(Integer, nullable=False)
    patient_notes = Column(Text, nullable=True)
    passphrase = Column(String, nullabe=False, default="beds2bytes")
    state = Column(Boolean, nullable=False, default=True)


# Create Tables if they don’t exist
Base.metadata.create_all(bind=engine)