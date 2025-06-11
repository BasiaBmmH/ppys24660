from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class GameStats(Base):
    __tablename__ = "game_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    score = Column(Integer, default=0)
    result = Column(String)  # "win" lub "loss"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player", back_populates="game_stats")
