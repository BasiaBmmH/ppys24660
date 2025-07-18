from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.database import Base
from .game_stats import GameStats

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    statistics = relationship("Statistics", uselist=False, back_populates="player")
    game_stats = relationship("GameStats", back_populates="player")