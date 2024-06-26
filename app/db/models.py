from sqlalchemy import Column, Integer, String
from .database import Base

class Gas(Base):
    __tablename__ = "gases"
    id = Column(Integer, primary_key=True, index=True)
    data_unique_id = Column(String, index=True)