import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env de forma segura
load_dotenv(dotenv_path=Path('.') / '.env')

# Lê o token fixo do Postman
ACCESS_TOKEN = os.getenv("BLING_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise Exception("A variável BLING_ACCESS_TOKEN não foi encontrada no .env.")

BASE_URL = "https://www.bling.com.br/Api/v3"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

def buscar_produtos(limit=100, pagina=1):
    url = f"{BASE_URL}/produtos?limite={limit}&pagina={pagina}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"[ERRO] ({response.status_code}) - {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao buscar produtos: {e}")
        return None

def criar_campo_personalizado(nome, tipo="texto"):
    url = f"{BASE_URL}/produtos/campos-personalizados"
    payload = {"nome": nome, "tipo": tipo}
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code != 201:
            print(f"[ERRO] Falha ao criar campo '{nome}': {response.status_code} - {response.text}")
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao criar campo personalizado: {e}")
        return False

def buscar_campo_personalizado(nome):
    url = f"{BASE_URL}/produtos/campos-personalizados?nome={nome}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao buscar campo '{nome}': {e}")
        return None

def atualizar_campo_personalizado(nome, valor, produto_id):
    url = f"{BASE_URL}/produtos/camposPersonalizados"
    url += f"/{produto_id}/{nome}"
    if not valor:
        print(f"[AVISO] Valor vazio para o campo '{nome}', não será atualizado.")
        return None
    payload = {"nome": nome, "valor": valor}
    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao atualizar campo '{nome}': {e}")
        return None

def excluir_campo_personalizado(nome, produto_id):
    url = f"{BASE_URL}/produtos/{produto_id}/campos-personalizados/{nome}"
    try:
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao excluir campo '{nome}': {e}")
        return None

def listar_campos_personalizados(produto_id):
    url = f"{BASE_URL}/produtos/{produto_id}/campos-personalizados"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao listar campos personalizados: {e}")
        return None
