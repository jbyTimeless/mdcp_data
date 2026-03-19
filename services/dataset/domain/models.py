from sqlalchemy import Column, Integer, String
from common.dependencies.database import Base

class DatasetItem(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(255))
