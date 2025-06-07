from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix='DB_',
        extra='ignore',
    )


settings = Settings()
DATABASE_URL_SYNC = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
