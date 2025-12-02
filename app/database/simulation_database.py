from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from .database import Base

# Simulation Item Model
class SimulationItem(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Associate created simulation with a user
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    name = Column(String, nullable=False)
    patient_notes = Column(Text, nullable=True)
    passphrase = Column(String, nullable=False, default="beds2bytes")
    state = Column(Boolean, nullable=False, default=True)

    user = relationship("UserItem", back_populates="simulations")
    case = relationship("CaseItem", back_populates="simulations")
    files = relationship("FileItem", back_populates='simulation') 