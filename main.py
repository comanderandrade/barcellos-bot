import time
import os
from chatgpt_api import consultar_chatgpt
from bling_api import buscar_produtos, criar_campo_personalizado
from dotenv import load_dotenv, find_dotenv

# Garante que o .env será encontrado e carregado de qualquer local
load_dotenv(find_dotenv())

SIMULAR = True  # Continua em modo simulado (NÃO envia para o Bling)

def executar_processo(socketio):
    print("Iniciando processo...")

    resposta = buscar_produtos(limit=100)
    
    if not resposta:
        print("Nenhuma resposta recebida da API.")
        return

    produtos = resposta.get("data", [])
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        nome = produto.get("nome", "Sem Nome")
        produto_id = produto.get("id", 0)

        emitir_status(socketio, nome, "blue")  # Verificando
        time.sleep(0.3)

        resposta = consultar_chatgpt(nome)
        if "ERRO" in resposta:
            emitir_status(socketio, nome, "red")
            continue

        emitir_status(socketio, nome, "orange")  # Processando
        time.sleep(0.3)

        # Simulação: não envia nada para o Bling
        sucesso = True

        if sucesso:
            emitir_status(socketio, nome, "green")
        else:
            emitir_status(socketio, nome, "red")

        time.sleep(0.3)

    print("Processo finalizado.")

def emitir_status(socketio, nome_produto, cor):
    print(f"[{cor.upper()}] {nome_produto}")
    if socketio:
        socketio.emit('progress', {'productName': nome_produto, 'step': cor})