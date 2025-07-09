from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str = "mongodb://root:example@localhost:27017/store?authSource=admin"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
print(f"DEBUG: DATABASE_URL carregada (RUNTIME): {settings.DATABASE_URL}")
