import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # <-- ESSENCIAL para carregar o .env

BLING_API_KEY = os.getenv("BLING_API_KEY")
if not BLING_API_KEY:
    raise Exception("A variável de ambiente BLING_API_KEY não foi carregada.")

BASE_URL = "https://www.bling.com.br/Api/v3"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {BLING_API_KEY}",
}

def buscar_produtos(limit=100, pagina=1):
    url = f"{BASE_URL}/produtos?limite={limit}&pagina={pagina}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return None


def criar_campo_personalizado(nome, tipo="texto"):
    url = f"{BASE_URL}/produtos/campos-personalizados"
    payload = {
        "nome": nome,
        "tipo": tipo
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code == 201


def buscar_campo_personalizado(nome):
    url = f"{BASE_URL}/produtos/campos-personalizados?nome={nome}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar campo personalizado: {e}")
        return None
def atualizar_campo_personalizado(nome, valor, produto_id):
    url = f"{BASE_URL}/produtos/{produto_id}/campos-personalizados"
    payload = {
        "nome": nome,
        "valor": valor
    }
    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar campo personalizado: {e}")
        return None
def excluir_campo_personalizado(nome, produto_id):
    url = f"{BASE_URL}/produtos/{produto_id}/campos-personalizados/{nome}"
    try:
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao excluir campo personalizado: {e}")
        return None
def listar_campos_personalizados(produto_id):
    url = f"{BASE_URL}/produtos/{produto_id}/campos-personalizados"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao listar campos personalizados: {e}")
        return None
