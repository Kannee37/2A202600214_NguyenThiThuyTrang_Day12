import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "TravelBuddy API")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("PORT", os.getenv("APP_PORT", 8000)))

    API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN", "travelbuddy-secret")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"

    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 20))
    MONTHLY_BUDGET_USD = float(os.getenv("MONTHLY_BUDGET_USD", 10))

    SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "system_prompt.txt")


settings = Settings()