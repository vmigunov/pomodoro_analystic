from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///pomodoro.sqlite")


Session = sessionmaker


def get_db_session() -> Session:
    return Session
