import sys
import os

# Adiciona a raiz do projeto no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from unittest.mock import patch
from types import SimpleNamespace
from utils.nome_tools import limpar_nome, nome_invalido, consultar_chatgpt

@pytest.mark.parametrize("entrada, esperado", [
    ("José", "jose"),
    ("ÁÉÍÓÚ", "aeiou"),
    ("Çãõá", "caoa"),
    ("Nome Normal", "nome normal"),
])
def test_limpar_nome(entrada, esperado):
    assert limpar_nome(entrada) == esperado

@pytest.mark.parametrize("nome, esperado", [
    ("Consignado Especial", True),
    ("produto CONSIG", True),
    ("NOME COMPLETO MAIUSCULO", True),
    ("Nome Normal", False),
    ("consig Produto", True),
    ("nome invalido", False),
])
def test_nome_invalido(nome, esperado):
    assert nome_invalido(nome) == esperado


@pytest.mark.asyncio
@patch("utils.nome_tools.client.chat.completions.create")
async def test_consultar_chatgpt_mock(mock_create):
    produtos = [
        {"nome": "Produto Teste", "marca": "", "peso": None},
        {"nome": "Outro Produto", "marca": "MarcaX"}
    ]

    # Simula objeto real do OpenAI com atributos (não dict)
    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=json.dumps(produtos)
                )
            )
        ]
    )

    mock_create.return_value = mock_response

    resultado = await consultar_chatgpt(produtos)
    assert isinstance(resultado, list)
    assert resultado == produtos
