from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
from app.settings import Settings

settings = Settings()

engine = create_engine(
    "postgresql+psycopg2://postgres:123@localhost:5433/pomodoro"
)  # "sqlite:///pomodoro.sqlite"


Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
