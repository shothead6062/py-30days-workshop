from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False


__all__ = ["AppSettings"]
