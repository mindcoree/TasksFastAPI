from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    port: int = 8000
    host: str = "127.0.0.1"


class UserPrefix(BaseModel):
    prefix: str = "/users"


class AdminPrefix(BaseModel):
    prefix: str = "/admins"


class ProductPrefix(BaseModel):
    prefix: str = "/products"


class MembersPrefix(BaseModel):
    prefix: str = "/members"
    users: UserPrefix = UserPrefix()
    admin: AdminPrefix = AdminPrefix()


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    members: MembersPrefix = MembersPrefix()


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
    access_expire_min: int = 15
    refresh_expire_days: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,  # чувствительность к регистрам
        env_nested_delimiter="__",  # это деления как путь будет
        env_prefix="CONFIG__",
        env_file=".env",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth: AuthJWT = AuthJWT()


settings = Settings()
