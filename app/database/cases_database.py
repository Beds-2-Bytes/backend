from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import sessionmaker, relationship
from .database import Base

# Cases Item Model
class CaseItem(Base):
    __tablename__ = "cases"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    case_name = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    base_values = Column(MutableDict.as_mutable(JSONB), nullable=False, default=dict)
    base_problem = Column(Text, nullable=False)
    learning_goals = Column(Text, nullable=False)
    start_point = Column(Text, nullable=False)

    simulations = relationship("SimulationItem", back_populates="case")
    user = relationship('UserItem', back_populates="cases")