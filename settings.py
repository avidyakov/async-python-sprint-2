from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    default_pool_size: int = 10
    default_lang: str = 'en'
    default_dir: Path = Path(__file__) / '../calendar'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
