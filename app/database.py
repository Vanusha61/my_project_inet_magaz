from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATA_BASE_URL

Base = declarative_base()

engine = create_engine(
    url = DATA_BASE_URL,
    echo = False,
    future = True,
)

SessionLocal = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    autoflush = True,
)