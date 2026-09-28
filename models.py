from sqlalchemy import Column, Integer, String
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(String, nullable=False)
    progress = Column(Integer, nullable=False, default=0)