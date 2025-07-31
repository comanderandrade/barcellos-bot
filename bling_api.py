# bling_api.py
import requests
import os

from token_manager import get_valid_access_token

API_KEY = os.getenv("BLING_API_KEY")
BASE_URL = "https://www.bling.com.br/Api/v3"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


def obter_produtos_bling(limite=100):
    get_valid_access_token()
    url = f"{BASE_URL}/produtos?limit={limite}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []

    produtos = response.json().get("data", [])
    resultado = []
    for item in produtos:
        prod = item.get("produto", {})
        resultado.append({
            "id": prod.get("id"),
            "nome": prod.get("nome"),
            "codigo": prod.get("codigo"),
            "gtin": prod.get("gtin"),
            "descricao": prod.get("descricao", "")
        })

    return resultado


def atualizar_produto(id_bling, dados):
    url = f"{BASE_URL}/produtos/{id_bling}"
    get_valid_access_token()

    payload = {
        "produto": {
            "pesoLiq": round(dados.get("pesoLiq", 0.05), 3),
            "larguraProduto": int(dados.get("largura", 10)),
            "alturaProduto": int(dados.get("altura", 10)),
            "profundidadeProduto": int(dados.get("profundidade", 10)),
            "descricaoCurta": dados.get("descricaoCurta", ""),
            "descricao": dados.get("descricao", "")
        },
        "camposPersonalizados": []
    }

    # Adiciona campos personalizados apenas se existirem
    if dados.get("modelo"):
        payload["camposPersonalizados"].append({
            "nome": "modelo",
            "valor": dados["modelo"]
        })

    if dados.get("tamanho"):
        payload["camposPersonalizados"].append({
            "nome": "tamanho",
            "valor": dados["tamanho"]
        })

    if dados.get("genero"):
        payload["camposPersonalizados"].append({
            "nome": "genero",
            "valor": dados["genero"]
        })

    response = requests.put(url, headers=HEADERS, json=payload)
    response.raise_for_status()
