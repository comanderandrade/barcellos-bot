from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BLING_API_KEY")
print(f"Token carregado: {token}")
