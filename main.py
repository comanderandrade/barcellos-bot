import os
import json
import httpx
import asyncio
from typing import List
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
import uvicorn
import logger

# Importa funções agora centralizadas em utils/nome_tools
from utils.nome_tools import limpar_nome, nome_invalido, consultar_chatgpt

# Inicialização do FastAPI
app = FastAPI()

def main():
    try:
        logger.log_info("Iniciando execução principal do bot...")

        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        BLING_API_KEY = os.getenv("BLING_API_KEY")

        bling_base_url = "https://www.bling.com.br/Api/v3"
        headers_bling = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BLING_API_KEY}"
        }

        # ========================
        # FUNÇÕES DE UTILIDADE
        # ========================

        async def notificar_front(ws: WebSocket, nome, cor, etapa):
            await ws.send_json({
                "nome": nome,
                "cor": cor,
                "etapa": etapa
            })

        # ========================
        # INTEGRAÇÃO COM BLING
        # ========================

        async def buscar_produtos_bling():
            url = f"{bling_base_url}/produtos?page=1&limit=100"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers_bling)
                return response.json().get("data", [])

        async def atualizar_produto(produto_id, dados):
            url = f"{bling_base_url}/produtos/{produto_id}"
            payload = {"produto": dados}
            async with httpx.AsyncClient() as client:
                await client.put(url, headers=headers_bling, json=payload)

        # ========================
        # WEBSOCKET
        # ========================

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await notificar_front(websocket, "Iniciando processo...", "azul", "Carregando produtos do Bling...")

            produtos = await buscar_produtos_bling()
            produtos_validos = []

            for item in produtos:
                produto = item.get("produto", {})
                nome = produto.get("nome", "")
                if nome_invalido(nome):
                    continue
                produtos_validos.append(produto)

            await notificar_front(websocket, "Consultando IA...", "azul", "Enviando produtos para análise do ChatGPT...")

            resultados_corrigidos = []
            for i in range(0, len(produtos_validos), 10):
                lote = produtos_validos[i:i + 10]
                corrigidos = await consultar_chatgpt(lote)
                resultados_corrigidos.extend(corrigidos)

            for produto in resultados_corrigidos:
                nome = produto.get("nome", "Sem nome")
                produto_id = produto.get("id")

                if not produto_id:
                    await notificar_front(websocket, nome, "vermelho", "ID não encontrado, ignorando.")
                    continue

                try:
                    await notificar_front(websocket, nome, "amarelo", "Atualizando produto no Bling...")
                    await atualizar_produto(produto_id, produto)
                    await notificar_front(websocket, nome, "verde", "Atualização concluída.")
                except Exception as e:
                    logger.log_bling(f"Erro ao atualizar produto {nome}: {e}", level="error")
                    await notificar_front(websocket, nome, "vermelho", "Erro ao atualizar produto.")

            await notificar_front(websocket, "Finalizado!", "verde", "Todos os produtos foram processados.")

    except Exception as e:
        logger.log_error(f"Erro fatal no bot: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
