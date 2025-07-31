import os
import json
import time
import threading
from flask import Flask, render_template, request, redirect, url_for, session, Response
from dotenv import load_dotenv
import bling_api
import gemini_api

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- Controles da Thread ---
pause_event = threading.Event()
task_thread = None

# --- Função Utilitária para criar lotes ---
def criar_lotes(lista, tamanho_lote):
    """Divide uma lista em lotes de um tamanho específico."""
    for i in range(0, len(lista), tamanho_lote):
        yield lista[i:i + tamanho_lote]

# --- Rotas da Aplicação (sem mudanças aqui) ---
@app.route('/')
def index():
    if 'bling_access_token' in session:
        return render_template('index.html', authenticated=True)
    return render_template('index.html', authenticated=False)

@app.route('/login')
# ... (código do login sem alteração)
def login():
    client_id = os.getenv('BLING_CLIENT_ID')
    redirect_uri = os.getenv('BLING_REDIRECT_URI')
    auth_url = (
        f"https://www.bling.com.br/Api/v3/oauth/authorize?"
        f"response_type=code&client_id={client_id}&state=s&redirect_uri={redirect_uri}"
    )
    return redirect(auth_url)

@app.route('/callback')
# ... (código do callback sem alteração)
def callback():
    code = request.args.get('code')
    if not code:
        return "Erro: Código de autorização não encontrado.", 400
    
    token_info = bling_api.get_access_token(code)
    
    if token_info and 'access_token' in token_info:
        session['bling_access_token'] = token_info['access_token']
        session['bling_refresh_token'] = token_info['refresh_token']
        session['expires_in'] = token_info['expires_in']
        session['token_creation_time'] = time.time()
        return redirect(url_for('index'))
    
    return "Erro ao obter token de acesso do Bling. Verifique o terminal para mais detalhes.", 500

@app.route('/logout')
# ... (código do logout sem alteração)
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- Lógica de Processamento em Lote ---
def process_products_task(access_token, limit=100, tamanho_lote=5):
    global task_status_stream
    if not access_token:
        task_status_stream.append({"status": "error", "message": "Token de acesso inválido."})
        return

    # 1. Busca todos os produtos
    products = bling_api.get_products(access_token, limit=limit)
    if not products:
        task_status_stream.append({"status": "error", "message": "Nenhum produto encontrado."})
        return
        
    # 2. Filtra produtos consignados ANTES de criar os lotes
    produtos_validos = [p for p in products if not any(term in p.get('nome','').lower() for term in ['consignado', 'consig'])]
    
    # 3. Cria os lotes para processamento
    lotes_de_produtos = list(criar_lotes(produtos_validos, tamanho_lote))

    for i, lote in enumerate(lotes_de_produtos):
        if pause_event.is_set():
            task_status_stream.append({"status": "paused", "message": f"Processo pausado antes do lote {i+1}/{len(lotes_de_produtos)}."})
            pause_event.wait()

        try:
            # Pega os detalhes completos para cada produto no lote
            lote_detalhado = []
            task_status_stream.append({"status": "info", "message": f"Buscando detalhes do lote {i+1}/{len(lotes_de_produtos)}..."})
            for p_resumo in lote:
                detalhes = bling_api.get_product_by_id(access_token, p_resumo['id'])
                if detalhes:
                    lote_detalhado.append(detalhes)
            
            if not lote_detalhado:
                task_status_stream.append({"status": "error", "message": f"Falha ao buscar detalhes para o lote {i+1}."})
                continue

            # Envia o lote completo para a IA
            task_status_stream.append({"status": "processing", "message": f"Analisando lote de {len(lote_detalhado)} produtos com IA..."})
            lote_atualizado_ia = gemini_api.consultar_gemini_em_lote(lote_detalhado)

            if not lote_atualizado_ia or len(lote_atualizado_ia) != len(lote_detalhado):
                task_status_stream.append({"status": "error", "message": f"Falha na análise do lote {i+1} pela IA."})
                # Pula para o próximo lote
                for produto in lote_detalhado: # Marca todos no lote como erro
                     task_status_stream.append({
                        "product_id": produto['id'], "product_name": produto.get('nome'), "status": "error",
                        "message": "Falha na análise do lote pela IA.", "color": "red"
                    })
                continue
            
            # Atualiza cada produto do lote retornado pela IA no Bling
            for produto_atualizado in lote_atualizado_ia:
                prod_id = produto_atualizado.get('id')
                prod_nome = produto_atualizado.get('nome')

                task_status_stream.append({
                    "product_id": prod_id, "product_name": prod_nome, "status": "processing",
                    "message": "Atualizando no Bling...", "color": "yellow", "full_data": produto_atualizado
                })
                time.sleep(1) # Delay para não sobrecarregar a API do Bling

                result = bling_api.update_product(access_token, prod_id, produto_atualizado)
                if result:
                    task_status_stream.append({
                        "product_id": prod_id, "product_name": prod_nome, "status": "success",
                        "message": "Atualizado com sucesso!", "color": "green"
                    })
                else:
                    task_status_stream.append({
                        "product_id": prod_id, "product_name": prod_nome, "status": "error",
                        "message": "Falha ao atualizar no Bling.", "color": "red"
                    })

        except Exception as e:
            task_status_stream.append({"status": "error", "message": f"Erro inesperado no lote {i+1}: {str(e)}"})
    
    task_status_stream.append({"status": "finished", "message": "Processo concluído."})


# --- Rotas de Controle e Stream (sem mudanças significativas) ---
@app.route('/start-processing')
def start_processing():
    global task_status_stream, task_thread
    if task_thread and task_thread.is_alive():
        return "Processo já está em andamento.", 409

    task_status_stream = [] 
    pause_event.clear()
    
    access_token = session.get('bling_access_token')
    if not access_token:
        return "Erro: Você não está autenticado.", 401

    task_thread = threading.Thread(target=process_products_task, args=(access_token,))
    task_thread.start()
    
    return "Processo iniciado.", 202

@app.route('/pause', methods=['POST'])
def pause_processing():
    pause_event.set()
    return "Comando de pausa enviado.", 200

@app.route('/resume', methods=['POST'])
def resume_processing():
    pause_event.set()
    pause_event.clear()
    return "Comando para continuar enviado.", 200

@app.route('/stream')
def stream():
    def event_stream():
        last_index = 0
        while True:
            if len(task_status_stream) > last_index:
                for i in range(last_index, len(task_status_stream)):
                    data = task_status_stream[i]
                    yield f"data: {json.dumps(data)}\n\n"
                    if data.get("status") == "finished":
                        return
                last_index = len(task_status_stream)
            time.sleep(0.5) 
    
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='127.0.0.1', port=port, debug=True)