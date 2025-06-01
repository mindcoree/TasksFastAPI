from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiUsersPrefix(BaseModel):
    prefix: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    users: ApiUsersPrefix = ApiUsersPrefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50  # кол-во соединений в пуле
    max_overflow: int = 10  # кол-во дополнительных соединений
    naming_convertion: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    private_key: str = BASE_DIR / "certs" / "private_key.pem"
    public_key: str = BASE_DIR / "certs" / "public_key.pem"
    algorithm: str = "RS256"
    expire_min: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,  # чувствительность к регистрам
        env_nested_delimiter="__",  # это деления как путь будет
        env_prefix="APP_CONFIG__",
        env_file=".env",
    )
    # вместо APP_CONFIG__ можно написать что угодно FASTAPI__ к примеру
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthJWT = AuthJWT()


settings = Settings()
print(settings.db.url)
