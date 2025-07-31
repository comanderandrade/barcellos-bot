import re
import json
import unicodedata
from typing import List
from openai import OpenAI
import logger

# Inicializa cliente OpenAI
client = OpenAI()

def limpar_nome(nome: str) -> str:
    """
    Remove acentuação e converte para minúsculas.
    """
    return unicodedata.normalize('NFD', nome.lower()).encode('ascii', 'ignore').decode('utf-8')

def nome_invalido(nome: str) -> bool:
    """
    Verifica se o nome contém termos proibidos ou está em caixa alta.
    """
    nome_limpo = limpar_nome(nome)
    termos_invalidos = ['consignado', 'consig']
    if any(t in nome_limpo for t in termos_invalidos):
        return True
    if re.search(r'\b[A-Z]{2,}(?:\s[A-Z]{2,}){1,}', nome):  # detecta nomes todos em maiúsculas
        return True
    return False

async def consultar_chatgpt(produtos: List[dict]):
    """
    Consulta o ChatGPT para validar/corrigir produtos.
    """
    prompt = (
        "Você é um sistema de análise de dados de produtos para e-commerce. "
        "Para cada produto, corrija ou preencha os campos conforme necessário: "
        "'marca', 'modelo', 'peso' (kg), 'largura', 'altura', 'profundidade' (cm), "
        "'descricao', 'categoria', 'subcategoria'.\n\n"
        "Nunca invente informações absurdas. Se não tiver dados confiáveis, deixe como está. "
        "NUNCA ofereça frete grátis e NUNCA remova dados existentes. "
        "Sempre mantenha a estrutura original dos produtos no JSON de retorno.\n\n"
        "Produtos:\n"
    )

    for p in produtos:
        prompt += json.dumps(p, ensure_ascii=False) + "\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.log_chatgpt(f"Erro ao interpretar resposta do ChatGPT: {e}", level="error")
        return []
