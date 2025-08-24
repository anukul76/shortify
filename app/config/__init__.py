from app.config.db_config import MySQLSettingsR, MySQLSettingsW
from app.config.api_config import APISettings
from app.constants import Environments
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_w: MySQLSettingsW = MySQLSettingsW()
    database_r: MySQLSettingsR = MySQLSettingsR()
    api: APISettings = APISettings()
    env: str = Environments.local
    kafka_broker: str = "localhost:9092"
    # KAFKA_CONFIG: dict = {
    #     'bootstrap.servers': kafka_broker,
    #     'auto.offset.reset': 'earliest',
    #     'enable.auto.commit': True,
    # }

    release_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        fields = {
            "env": {"env": "ENV"},
            "kafka_broker": {"env": "KAFKA_BROKER"},
        }
        extra = "ignore"

    @property
    def KAFKA_CONFIG(self):
        return {
            'bootstrap.servers': self.kafka_broker,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
        }


settings = Settings()
