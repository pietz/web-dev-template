from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_url: str
    database_url: str
    session_key: str
    github_client_id: str
    github_client_secret: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
