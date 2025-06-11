from models.database import engine, Base
from models import player, statistics
from models.game_stats import GameStats

Base.metadata.create_all(bind=engine)
print("Tabele zostały utworzone (jeśli nie istniały).")
