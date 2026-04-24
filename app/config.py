import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)
load_dotenv(APP_DIR / ".env", override=True)


class Config:
    DB_NAME = os.getenv("DB_NAME", "german_scenario")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_IN_HOURS = int(os.getenv("JWT_EXPIRES_IN_HOURS", "24"))
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "llama-3.3-70b-versatile")
    GROQ_STRUCTURED_MODEL = os.getenv("GROQ_STRUCTURED_MODEL", "openai/gpt-oss-20b")
    GROQ_TIMEOUT = float(os.getenv("GROQ_TIMEOUT", "60"))
    MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "18"))
    SOFT_CONVERSATION_END_AFTER_USER_MESSAGES = int(os.getenv("SOFT_CONVERSATION_END_AFTER_USER_MESSAGES", "6"))
    DEFAULT_OPENING_MESSAGE = os.getenv("DEFAULT_OPENING_MESSAGE", "true").lower() == "true"
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
