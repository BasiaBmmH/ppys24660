from sqlalchemy import Column, Integer, String, ForeignKey
from models.database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    word = Column(String, unique=True, nullable=False)
