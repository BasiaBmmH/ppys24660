from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base

class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    points = Column(Integer, default=0)

    player = relationship("Player", back_populates="statistics")
