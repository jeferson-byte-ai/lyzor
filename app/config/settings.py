import os
from dotenv import load_dotenv

# Load .env if exists
load_dotenv()

class Settings:
    APP_NAME: str = "LYZOR"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"
    
    # Paths
    TEMP_DIR: str = os.path.join(os.getcwd(), "temp")
    VOICE_DIR: str = os.path.join(os.getcwd(), "voices")
    LOG_DIR: str = os.path.join(os.getcwd(), "logs")
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
