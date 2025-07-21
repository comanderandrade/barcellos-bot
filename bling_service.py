# bling_service.py
import requests
from config import BLING_API_KEY

BLING_BASE_URL = "https://bling.com.br/Api/v2"

def get_products(limit=100):
    url = f"{BLING_BASE_URL}/produtos/json"
    params = {
        "apikey": BLING_API_KEY,
        "pagina": 1,
        "quantidade": limit
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        produtos = data.get("retorno", {}).get("produtos", [])
        return produtos
    except Exception as e:
        print(f"Erro ao buscar produtos no Bling: {e}")
        return []
