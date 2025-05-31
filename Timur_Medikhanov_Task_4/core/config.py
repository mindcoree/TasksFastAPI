from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: str = 222


class UsersPrefix(BaseModel):
    prefix: str = "/users"


class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    echo: bool = True


class AuthJWT(BaseModel):
    private_key: str = BASE_DIR / "certs" / "private_key.pem"
    publib_key: str = BASE_DIR / "certs" / "public_key.pem"
    algorithm: str = "RS256"
    expire_min: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,  # чувствительность к регистрам
        env_nested_delimiter="__",  # это деления как путь будет
        env_prefix="USER_CONFIG__",
        env_file=".env",
    )
    users: UsersPrefix = UsersPrefix()
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    auth: AuthJWT = AuthJWT()


settings = Settings()
