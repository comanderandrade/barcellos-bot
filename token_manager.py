import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("BLING_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLING_CLIENT_SECRET")
TOKEN_FILE = ".env"  # arquivo onde estão suas variáveis de ambiente

def get_tokens():
    access_token = os.getenv("BLING_ACCESS_TOKEN")
    refresh_token = os.getenv("BLING_REFRESH_TOKEN")
    return access_token, refresh_token

def refresh_access_token():
    _, refresh_token = get_tokens()
    if not refresh_token:
        raise Exception("Refresh token não encontrado. Faça login novamente.")

    url = "https://www.bling.com.br/Api/v3/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens.get("access_token")
        new_refresh_token = tokens.get("refresh_token")

        # Atualiza .env
        set_key(TOKEN_FILE, "BLING_ACCESS_TOKEN", new_access_token)
        set_key(TOKEN_FILE, "BLING_REFRESH_TOKEN", new_refresh_token)

        # Recarrega variáveis de ambiente
        load_dotenv(override=True)

        return new_access_token
    else:
        raise Exception(f"Falha ao atualizar token: {response.text}")

def get_valid_access_token():
    access_token, _ = get_tokens()
    # Aqui você pode implementar uma checagem mais avançada de validade do token
    # Por simplicidade, se token estiver vazio tenta fazer refresh

    if not access_token:
        return refresh_access_token()
    return access_token
