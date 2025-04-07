from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    database_echo: bool
    api_host: str
    api_port: int
    telegram_bot_token: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()