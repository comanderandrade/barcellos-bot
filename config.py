# config.py

# API KEYs
# config.py
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

BLING_API_KEY = os.getenv("BLING_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 5000))


# Configuração da loja (id, nome, etc.)
LOJA_ID = "1"

# Endpoint base da API do Bling
BLING_BASE_URL = "https://www.bling.com.br/Api/v3"

# OpenAI
OPENAI_MODEL = "gpt-4o"

# Outras configurações
HTML_REFRESH_INTERVAL = 2  # segundos
