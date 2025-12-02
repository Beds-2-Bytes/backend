from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship
from constants import RoleEnum
from .database import Base

# Users Item Model
class UserItem(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False) # Hashed password
    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False) # I.E admin, student...

    simulations = relationship("SimulationItem", back_populates="user", cascade="all, delete")
    files = relationship("FileItem", back_populates="user", cascade="all, delete")
    cases = relationship("CaseItem", back_populates="user", cascade="all, delete")