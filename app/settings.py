from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    # DB_DRIVER: str = 'postgresql+psycopg2' синхронный драйвер
    DB_DRIVER: str = "postgresql+asyncpg"  # aсинхронный драйвер
    DB_NAME: str = "pomodoro"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6380
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = "secret+key"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str = (
        "1091754126117-a5j86hfpqa240vqmocg49gv882uim3vg.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET: str = "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"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google"
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    @property
    def db_url(self):
        print(
            f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"


settings = Settings()
