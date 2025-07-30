import requests

TOKEN = "388f040ff2ba87dcabbe6171f039cbeba32d4c0a8e801b0ae493a7448e1851035ca28811"  # substitua pelo seu token do Bling

def testar_api_bling():
    url = f"https://www.bling.com.br/Api/v3/produtos?apikey={TOKEN}&limite=1&pagina=1"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # vai gerar erro se status != 200
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
