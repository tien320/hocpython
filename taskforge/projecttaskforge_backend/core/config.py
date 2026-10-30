from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str = "TaskForge API"
    ENVIRONMENT : str = "development"
    DEBUG : bool = True
    #DB
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST : str = "localhost"
    DB_PORT: int = 1521
    DB_SERVICE : str = "XEPDB1"
    #jwt
    SECRET_KEY : str
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding= "utf-8", extra= "ignore")
    @property
    def database_url(self):
        return f"oracle+oracledb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/?service_name={self.DB_SERVICE}"
settings = Settings()