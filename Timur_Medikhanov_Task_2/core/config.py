from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    post: str = 222


class UsersPrefix(BaseModel):
    prefix: str = "/users"


class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    echo: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="USER_CONFIG_",
        env_file=".env",
    )
    users: UsersPrefix = UsersPrefix()
    run: RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()
