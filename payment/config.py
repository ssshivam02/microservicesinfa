from pydantic import BaseSettings

# this is for setting enviroment
class Settings(BaseSettings):
    database_hostname: str  # ------------------
    database_port: str  # ------ HERE WE can add default value also
    database_password: str  # ---------- this will take value from .env
    database_name_payment: str  # ------
    database_username: str  # ----------

    class Config:
        env_file = ".env"


settings = Settings()
