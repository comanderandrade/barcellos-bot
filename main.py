# main.py
import time
import re
from chatgpt_api import consultar_chatgpt
from bling_api import buscar_produtos, criar_campo_personalizado, atualizar_campo_personalizado
from utils import emitir_status

LIMIT_PRODUTOS = 5
SIMULAR = False

IGNORAR_PADROES = [
    r"consig", r"consignado",
    r"\b(jos[eé]|carlos|fernando|manuel|andrade|lu[ií]z|maria|paulo|silva|santos)\b"
]

def garantir_campo(nome):
    try:
        criar_campo_personalizado(nome)
    except:
        pass

def deve_ignorar(nome):
    nome_lower = nome.lower()
    for padrao in IGNORAR_PADROES:
        if re.search(padrao, nome_lower):
            return True
    return False

def executar_processo(socketio=None):
    print("🚀 Iniciando processo de análise e atualização de produtos...")
    resposta = buscar_produtos(limit=LIMIT_PRODUTOS)
    if not resposta:
        print("[ERRO] Nenhuma resposta recebida da API.")
        return

    produtos = resposta.get("data", [])
    if not produtos:
        print("[ERRO] Nenhum produto encontrado.")
        return

    for produto in produtos:
        nome = produto.get("nome", "").strip()
        produto_id = produto.get("id")
        codigo_universal = produto.get("gtin", "").strip()

        if deve_ignorar(nome):
            emitir_status(socketio, nome, "red")
            continue

        emitir_status(socketio, nome, "blue")
        time.sleep(0.2)

        print(f"Consultando ChatGPT para o produto: {nome} (Código Universal: {codigo_universal})")
        resposta = consultar_chatgpt(nome, codigo_universal)
        if not resposta or "ERRO" in resposta:
            emitir_status(socketio, nome, "red")
            continue

        emitir_status(socketio, nome, "orange")
        time.sleep(0.2)

        modelo = resposta.get("modelo")
        tamanho = resposta.get("tamanho")
        genero = resposta.get("genero")
        peso = resposta.get("peso")
        altura = resposta.get("altura")
        largura = resposta.get("largura")
        comprimento = resposta.get("comprimento")

        sucesso = True

        if not SIMULAR:
            if modelo:
                garantir_campo("modelo")
                sucesso &= atualizar_campo_personalizado("modelo", modelo, produto_id) is not None
            if tamanho:
                garantir_campo("tamanho")
                sucesso &= atualizar_campo_personalizado("tamanho", tamanho, produto_id) is not None
            if genero:
                garantir_campo("genero")
                sucesso &= atualizar_campo_personalizado("genero", genero, produto_id) is not None

            atualizacoes = {}
            if peso and peso < 0.05:
                peso = 0.05
            if peso:
                atualizacoes["pesoLiq"] = peso

            dimensoes = {"largura": largura, "altura": altura, "profundidade": comprimento}
            for chave, valor in dimensoes.items():
                if valor and valor < 10:
                    dimensoes[chave] = 10

            atualizacoes.update(dimensoes)

            if atualizacoes:
                print(f"[🔄] Atualizando dimensões e peso do produto {nome}... → {atualizacoes}")
                # Aqui poderá ser usado: atualizar_produto(produto_id, atualizacoes)

        emitir_status(socketio, nome, "green" if sucesso else "red")
        time.sleep(0.3)

    print("✅ Processo finalizado.")
