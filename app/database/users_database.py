from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv
from constants import RoleEnum

load_dotenv()  # Load environment variables from .env file
DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@localhost:5432/{os.getenv('DBNAME')}"

# Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Users Item Model
class UserItem(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False) # Hashed password
    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False) # I.E admin, student...

# Create Tables if they don’t exist
Base.metadata.create_all(bind=engine)
