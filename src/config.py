from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str


settings = Settings()
DATABASE_URL_SYNC = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
