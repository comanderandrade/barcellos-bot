# chatgpt_batch.py

import openai
import os
import logging
from typing import List
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatGPTBatch")

PROMPT_BASE = """
Você é um assistente responsável por analisar e revisar produtos cadastrados em um sistema de ERP.

Seu trabalho é:
1. Verificar se o produto possui informações corretas nos campos de `modelo`, `tamanho`, `genero`, `peso`, `dimensoes`, `marca` e `descrição`.
2. Se os campos estiverem corretos, mantê-los.
3. Se estiverem incorretos ou ausentes, corrigi-los com base no nome e código universal do produto.
4. Nunca apagar ou sobrescrever informações que estejam corretas.
5. O formato da resposta deve ser uma **lista JSON de produtos**, cada produto com estrutura igual ao recebido.

Nunca modifique o `id`, `codigo`, `nome` ou `preço` original do produto. Corrija apenas os campos técnicos e informativos.
"""

def dividir_em_lotes(lista, tamanho_lote):
    for i in range(0, len(lista), tamanho_lote):
        yield lista[i:i + tamanho_lote]

def processar_lote_com_chatgpt(produtos: List[dict]) -> List[dict]:
    """
    Envia lote de produtos para o ChatGPT e retorna os produtos atualizados.
    """
    try:
        logger.info(f"Enviando {len(produtos)} produtos ao ChatGPT...")
        
        mensagem_usuario = f"""
Abaixo está a lista de produtos a serem revisados:

{produtos}
"""

        resposta = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            temperature=0.2,
            messages=[
                {"role": "system", "content": PROMPT_BASE},
                {"role": "user", "content": mensagem_usuario}
            ]
        )

        resultado = resposta['choices'][0]['message']['content']

        # Tentar interpretar a resposta como JSON válido
        import json
        produtos_corrigidos = json.loads(resultado)

        if not isinstance(produtos_corrigidos, list):
            logger.error("Resposta do ChatGPT não é uma lista.")
            return []

        logger.info("Resposta recebida com sucesso.")
        return produtos_corrigidos

    except Exception as e:
        logger.error(f"Erro ao processar lote com ChatGPT: {e}")
        return []
