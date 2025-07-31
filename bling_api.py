import requests
import os

API_V3_URL = "https://www.bling.com.br/Api/v3"

def get_access_token(code):
    """Troca o código de autorização por um token de acesso."""
    url = "https://www.bling.com.br/Api/v3/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("BLING_REDIRECT_URI")
    }
    # Bling requer autenticação Basic com client_id e client_secret
    auth = (os.getenv("BLING_CLIENT_ID"), os.getenv("BLING_CLIENT_SECRET"))
    
    response = requests.post(url, data=payload, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter token: {response.status_code} - {response.text}")
        return None

def get_products(access_token, page=1, limit=100):
    """Busca uma lista paginada de produtos do Bling."""
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limite": limit, "pagina": page}
    url = f"{API_V3_URL}/produtos"
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erro ao buscar produtos: {response.status_code} - {response.text}")
        return []

def get_product_by_id(access_token, product_id):
    """Busca os detalhes completos de um único produto."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_V3_URL}/produtos/{product_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {})
    else:
        print(f"Erro ao buscar produto {product_id}: {response.status_code} - {response.text}")
        return None


def update_product(access_token, product_id, data):
    """Atualiza um produto no Bling usando o método PUT."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = f"{API_V3_URL}/produtos/{product_id}"
    
    # Garantir que a estrutura está correta, especialmente para campos complexos
    update_payload = {
        "nome": data.get("nome"),
        "preco": data.get("preco"),
        "descricaoCurta": data.get("descricaoCurta"),
        "descricao": data.get("descricao"),
        "peso": data.get("peso"),
        "dimensoes": data.get("dimensoes"),
        # Adicione outros campos que a IA pode modificar
    }

    # A API de atualização pode ser diferente da de criação.
    # Vamos usar PATCH para atualizar apenas os campos enviados
    # NOTA: A API v3 usa PUT para substituição total. 
    # Precisamos montar o payload completo. O ideal é usar o retorno da IA.
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Produto {product_id} atualizado com sucesso.")
        return response.json()
    else:
        print(f"Erro ao atualizar produto {product_id}: {response.status_code} - {response.text}")
        return None

# Funções para campos personalizados (ainda não implementadas, mas planejadas)
def find_or_create_custom_field(access_token, field_name):
    """Verifica se um campo personalizado existe e o cria se não existir."""
    # Lógica a ser implementada:
    # 1. Listar campos personalizados
    # 2. Verificar se `field_name` existe
    # 3. Se não, criar o campo e retornar seu ID
    # 4. Se sim, retornar o ID existente
    print(f"A LÓGICA para criar o campo '{field_name}' será implementada aqui.")
    # Retornar um ID falso por enquanto para o fluxo continuar
    return 123456