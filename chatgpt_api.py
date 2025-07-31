# chatgpt_api.py
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
Você é um especialista em catalogar produtos para lojas virtuais.

Abaixo está uma lista de produtos no formato JSON do Bling. Para cada item, retorne um novo JSON com os seguintes campos atualizados ou adicionados:

- modelo
- tamanho (se aplicável)
- genero (masculino, feminino ou unissex)
- peso (kg) → campo no Bling: pesoLiq
- largura (cm)
- altura (cm)
- profundidade (cm)
- descricao_curta (até 300 caracteres)
- descricao_longa (até 1000 caracteres)
- categoria
- subcategoria

OBSERVAÇÕES:
- Nunca invente um modelo se não encontrar um real.
- Se não encontrar uma informação, deixe o campo em branco ("").
- Sempre retorne um JSON válido, com um array chamado "produtos".
- Nunca inclua explicações ou texto fora do JSON.
- Use medidas razoáveis se não houver dados exatos.

Produtos:
{json_produtos}
"""

def consultar_chatgpt_lista(produtos: list):
    if not openai.api_key:
        return {"erro": "Chave da OpenAI não configurada."}

    json_produtos = json.dumps(produtos, ensure_ascii=False)
    prompt = PROMPT_TEMPLATE.format(json_produtos=json_produtos)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000,
        )
        raw_output = response.choices[0].message.content.strip()
        data = json.loads(raw_output)
        return data
    except Exception as e:
        return {"erro": str(e)}
