from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Notes API"
    mongo_url: str
    database_name: str
    access_token_expire_minutes: int
    log_file: str
    app_port: int
    admin_username: str
    admin_password: str
    debug: bool = False
    # JWT Settings
    access_token_secret: str
    token_algorithm: str = "HS256"


    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
