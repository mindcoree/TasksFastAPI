from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn, BaseModel


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: str = 8000
    reload: str = True


class ApiNotePrefix(BaseModel):
    prefix: str = "/note"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    note: ApiNotePrefix = ApiNotePrefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",  # чувствительность к регистрам
        env_prefix="NOTE_CONFIG__",  # это деления как путь будет
        env_file=".env",
    )

    api: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()
