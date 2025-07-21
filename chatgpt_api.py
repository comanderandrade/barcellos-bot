# chatgpt_api.py
import openai
import os

# Defina sua chave da OpenAI como variável de ambiente ou insira diretamente aqui (não recomendado em produção)
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
Por favor, localize na internet sobre o seguinte item estas informações Requeridas (nesta ordem): 

Marca  
Modelo  
Peso líquido (do produto)  
Peso bruto (produto + embalagem)  
Largura (do produto ou embalagem, em cm)  
Altura (do produto ou embalagem, em cm)  
Profundidade (do produto ou embalagem, em cm)  
Descrição curta (até 300 caracteres)  
Descrição longa (até 1000 caracteres)  
Categoria (ex: Ciclismo)  
Subcategoria (ex: Pneus de bicicleta)

Observações:  
Caso não encontre as dimensões exatas da embalagem, forneça estimativas razoáveis.  
Inclua as dimensões e peso da embalagem nas informações de peso bruto, largura, altura e profundidade.  
Não inclua as fontes das informações.
Produto: {product_name}
"""

def consultar_chatgpt(product_name):
    prompt = PROMPT_TEMPLATE.format(product_name=product_name)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"ERRO: {str(e)}"
