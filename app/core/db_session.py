import databases
from sqlalchemy import create_engine

from app.config import settings

engine_r = create_engine(settings.database_r.uri)
engine_w = create_engine(settings.database_w.uri)
database_r = databases.Database(settings.database_r.uri)
database_w = databases.Database(settings.database_w.uri)
