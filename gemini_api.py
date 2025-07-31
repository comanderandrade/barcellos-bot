import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def consultar_gemini_em_lote(lote_produtos_json):
    """
    Envia um LOTE de produtos para o Gemini e retorna a análise em lote.
    """
    prompt = f"""
    Análise e enriquecimento de dados de um LOTE de produtos para e-commerce.

    **Tarefa:**
    Você é um especialista em catalogação de produtos para a "Barcellos Bike Shop".
    Analise o ARRAY JSON de produtos fornecido. Para CADA produto no array, enriqueça seus dados seguindo as regras de negócio.
    Retorne um novo ARRAY JSON contendo TODOS os produtos analisados, na MESMA ORDEM em que foram recebidos.

    **Array de Produtos (Entrada):**
    ```json
    {json.dumps(lote_produtos_json, indent=4)}
    ```

    **Regras de Negócio (aplicar a cada produto individualmente):**
    1.  **Estrutura e Ordem:** O JSON de saída deve ser um array com o mesmo número de objetos do array de entrada e na mesma ordem. A estrutura de cada objeto deve ser idêntica à do objeto de entrada correspondente.
    2.  **`nome`:** Corrija e otimize para SEO.
    3.  **`descricaoCurta`:** Crie uma descrição curta e atrativa (máx 150 caracteres).
    4.  **`descricao`:** Crie uma descrição detalhada em HTML.
    5.  **`peso`:** Em kg. Mínimo 0.1. Estime se for 0.
    6.  **`dimensoes`:** Em cm. Mínimo 10 para cada lado. Estime se for 0.
    7.  **`camposPersonalizados`:**
        * **`modelo`:** Identifique e preencha o modelo. Campo OBRIGATÓRIO.
        * **`genero`:** Preencha (Masculino, Feminino, Unissex) apenas se aplicável.
        * **`tamanho`:** Preencha (P, M, G, 39, 42) apenas se aplicável.

    **Responda APENAS com o código do ARRAY JSON final, sem nenhum texto ou explicação adicional.**
    """

    try:
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        
        analysis_json_text = convo.last.text
        
        # Validação extra para garantir que a resposta é uma lista
        parsed_response = json.loads(analysis_json_text)
        if isinstance(parsed_response, list):
            return parsed_response
        else:
            print("Erro: Resposta da IA não é uma lista JSON.")
            return None

    except Exception as e:
        print(f"Erro ao consultar Gemini em lote: {e}")
        return None