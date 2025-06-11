from models.database import engine, Base
from models.game_stats import GameStats
from models import player, statistics
Base.metadata.create_all(bind=engine)
print("Tabele zostały utworzone (jeśli nie istniały).")
