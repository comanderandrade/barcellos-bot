import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BLING_API_KEY")  # Usa a variável do .env

def testar_api_bling():
    url = f"https://www.bling.com.br/Api/v3/produtos?apikey={TOKEN}&limite=1&pagina=1"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        print("API respondeu com sucesso!")
        print(dados)
    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP: {err}")
        print(f"Conteúdo da resposta: {resposta.text}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    testar_api_bling()
