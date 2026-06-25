from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Котики'
    database_url: str | None = 'sqlite+aiosqlite:///./fastapi.db'
    app_description: str = 'благотворительность'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
