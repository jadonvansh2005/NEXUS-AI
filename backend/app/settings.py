from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "UPSS"

    DEBUG: bool = True

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    CLAUDE_API_KEY: str = ""

    MISTRAL_API_KEY: str = ""

    DATABASE_URL: str

    REDIS_HOST: str

    REDIS_PORT: int

    QDRANT_HOST: str

    QDRANT_PORT: int

    POSTGRES_BIN: str = r"C:\Program Files\PostgreSQL\18\bin"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_SENDER_EMAIL: str = ""
    SMTP_SENDER_PASSWORD: str = ""
    GOOGLE_CLIENT_ID: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()