# prompts.py

def gerar_prompt(nome_produto):
    return f"""
Você é um assistente que ajuda a estruturar informações de produtos para cadastro em sistemas de e-commerce.

Com base no nome e/ou descrição do seguinte produto, pesquise ou deduza as seguintes informações:

Produto: {nome_produto}

Requerido (nessa ordem):
- Marca
- Modelo
- Peso líquido (do produto) [em kg ou g]
- Peso bruto (produto + embalagem) [em kg ou g]
- Largura [em cm]
- Altura [em cm]
- Profundidade [em cm]
- Descrição curta (até 300 caracteres)
- Descrição longa (até 1000 caracteres)
- Categoria (ex: Ciclismo)
- Subcategoria (ex: Pneus de bicicleta)

⚠️ Observações:
- Se não encontrar dimensões da embalagem, forneça uma estimativa razoável.
- Inclua sempre o peso bruto e dimensões da embalagem.
- Não inclua as fontes das informações.
"""
