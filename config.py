from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = str(Path(__file__).parent)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR, env_file_encoding="utf-8")

    MONGO_DATABASE_HOST: str = (
        "mongodb://localhost:30001,localhost:30002,localhost:30003/persona_ai_writer?replicaSet=my-replica-set"
    )
    MONGO_DATABASE_NAME: str = "persona_ai_writer"

    # Optional LinkedIn credentials for scraping your profile
    LINKEDIN_USERNAME: str | None = None
    LINKEDIN_PASSWORD: str | None = None


settings = Settings()
