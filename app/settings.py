from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db_name = "sqlite3"


settings = Settings()
