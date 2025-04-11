import sqlite3
from settings import settings

def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(settings.sqlite_db_name)
