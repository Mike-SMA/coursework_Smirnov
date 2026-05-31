from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5434
    POSTGRES_DB: str = "auth_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5434/auth_db"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380

    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
