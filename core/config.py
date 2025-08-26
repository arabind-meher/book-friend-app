import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

settings = Settings()
