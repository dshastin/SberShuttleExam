import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str = Field(default="auth service", validation_alias="AUTH_SERVICE_NAME")
    cache_expire_in_seconds: int = Field(default=300, validation_alias="CACHE_EXPIRE_IN_SECONDS")
    handlers_logging_lvl: str = Field(default="DEBUG", validation_alias="HANDLERS_LOGGING_LEVEL")
    logger_logging_lvl: str = Field(default="INFO", validation_alias="LOGGER_LOGGING_LEVEL")
    root_logging_lvl: str = Field(default="INFO", validation_alias="ROOT_LOGGING_LEVEL")

    pg_user: str = Field(default="postgres", validation_alias="POSTGRES_USER")
    pg_password: str = Field(default="123qwe", validation_alias="POSTGRES_PASSWORD")
    pg_host: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    pg_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    pg_db: str = Field(default="auth", validation_alias="POSTGRES_DB")

    jwt_secret_key: str = Field(default="jwt_secret_key", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")

    access_token_expire_minutes: int = Field(
        default=50, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=1500, validation_alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )

    num_bytes: int = Field(default=6, validation_alias="NUM_PASSWORD_BYTES")

    # router regexp
    path_mask: str = (
        r"^\/api\/(v1\/auth\/login|v1\/auth\/register|v1\/auth\/refresh|openapi-auth|"
        r"openapi-auth.json)\/*"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    def get_db_url(self):
        pg_url = (
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        )
        print(pg_url)
        return pg_url


settings = Settings()
