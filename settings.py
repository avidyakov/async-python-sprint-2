from pydantic import BaseSettings


class Settings(BaseSettings):
    default_pool_size: int = 10

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
