import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env da raiz do projeto
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configurações gerais
class Settings:
    CONSUMER_KEY_TWITTER: str = os.getenv("CONSUMER_KEY_TWITTER", "")
    CONSUMER_SECRET_TWITTER: str = os.getenv("CONSUMER_SECRET_TWITTER", "")
    CLIENT_ID_TWITTER: str = os.getenv("CLIENT_ID_TWITTER", "")
    CLIENT_SECRET_TWITTER: str = os.getenv("CLIENT_SECRET_TWITTER", "")
    ACCESS_TOKEN_TWITTER: str = os.getenv("ACCESS_TOKEN_TWITTER", "")
    ACCESS_TOKEN_TWITTER_SECRET: str = os.getenv("ACCESS_TOKEN_TWITTER_SECRET", "")
    BEARER_TOKEN_TWITTER: str = os.getenv("BEARER_TOKEN_TWITTER", "")

    DB_URL: str = os.getenv("DB_URL", "")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Você pode adicionar mais variáveis aqui se quiser
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
