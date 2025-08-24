from pydantic_settings import BaseSettings
from typing import Optional

class APISettings(BaseSettings):
    PROJECT_NAME: str = "shortify"
    PROJECT_VERSION: str = "1.0.0"
    origins: str = "*"
    

    class Config:
        env_file = ".env"
        env_prefix = "API_"
        validate_by_name = True
        extra = "ignore"