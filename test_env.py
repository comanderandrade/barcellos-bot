from dotenv import load_dotenv
import os
from pathlib import Path

# Caminho absoluto do .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("Client ID:", os.getenv("BLING_CLIENT_ID"))
print("Client Secret:", os.getenv("BLING_CLIENT_SECRET"))
print("Redirect URI:", os.getenv("BLING_REDIRECT_URI"))
print("API URL:", os.getenv("BLING_API_URL"))