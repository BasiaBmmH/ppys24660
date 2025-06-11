from models.database import Base, engine
from models import player, statistics

Base.metadata.create_all(bind=engine)
