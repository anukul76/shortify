import os
from urllib import parse
from pydantic_settings import BaseSettings

# Load environment variables from .env.db.db file
# from dotenv import load_dotenv

# load_dotenv(".env.db.db")


class MySQLSettingsW(BaseSettings):
    """MySQL Database Settings for Writer

    Args:
        BaseSettings (BaseSettings): Base Class
    """

    W_HOST: str = "localhost"
    W_PORT: int = 5432
    W_DB: str = "shortify"
    W_USER: str = "postgres"
    W_PASSWORD: str = "1234"

    class Config:
        env_file = ".env.db"
        validate_by_name = True
        extra = "ignore"

    @property
    def uri(self):
        return (
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        ).format(
            user=self.W_USER,
            password=parse.quote_plus(self.W_PASSWORD),
            host=self.W_HOST,
            port=self.W_PORT,
            db=self.W_DB
        )


class MySQLSettingsR(BaseSettings):
    """MySQL Database Settings for Reader

    Args:
        BaseSettings (BaseSettings): Base Class
    """

    R_HOST: str = "localhost"
    R_PORT: int = 5432
    R_DB: str = "shortify"
    R_USER: str = "postgres"
    R_PASSWORD: str = "1234"

    class Config:
        env_file = ".env.db"
        validate_by_name = True
        extra = "ignore"

    @property
    def uri(self):
        return (
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        ).format(
            user=self.R_USER,
            password=parse.quote_plus(self.R_PASSWORD),
            host=self.R_HOST,
            port=self.R_PORT,
            db=self.R_DB
        )
