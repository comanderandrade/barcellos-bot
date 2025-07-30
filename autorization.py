import os
import requests
from flask import Flask, redirect, request, session, render_template_string
from dotenv import load_dotenv
from pathlib import Path
import json

# Carregar variáveis do .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Flask setup
app = Flask(__name__)
app.secret_key = 'chave-super-secreta'

# Constantes de ambiente
CLIENT_ID = os.getenv("BLING_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLING_CLIENT_SECRET")
REDIRECT_URI = os.getenv("BLING_REDIRECT_URI") or "https://da0291f2bbdb.ngrok-free.app/callback"

AUTH_URL = "https://www.bling.com.br/Api/v3/oauth/authorize"
TOKEN_URL = "https://www.bling.com.br/Api/v3/oauth/token"
API_URL = os.getenv("BLING_API_URL") or "https://www.bling.com.br/Api/v3/produtos"
TOKEN_FILE = "bling_tokens.json"


# Função para salvar tokens em JSON

def save_tokens(data):
    print("🔐 Salvando tokens em bling_tokens.json...")
    with open("bling_tokens.json", "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Tokens salvos com sucesso.")





# Função para carregar tokens
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None


# Renovar access token automaticamente
def refresh_access_token():
    tokens = load_tokens()
    if not tokens or 'refresh_token' not in tokens:
        return None

    response = requests.post(TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    if response.ok:
        new_tokens = response.json()
        save_tokens(new_tokens)
        return new_tokens['access_token']
    else:
        print("Erro ao renovar token:", response.text)
        return None


@app.route('/')
def index():
    tokens = load_tokens()
    if not tokens:
        return render_template_string('<a href="/auth">Autorizar com o Bling</a>')

    access_token = tokens.get('access_token')
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 401:
        # Token expirado ou inválido
        access_token = refresh_access_token()
        if not access_token:
            return redirect('/auth')
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(API_URL, headers=headers)

    if response.ok:
        produtos = response.json()
        return f"<pre>{json.dumps(produtos, indent=4, ensure_ascii=False)}</pre>"
    else:
        return f"Erro: {response.status_code} - {response.text}"


@app.route('/auth')
def auth():
    url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=xyz"
    return redirect(url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Código de autorização ausente."

    response = requests.post(TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    })

    if response.ok:
        tokens = response.json()
        save_tokens(tokens)
        return redirect('/')
    else:
        return f"Erro ao obter token: {response.text}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
