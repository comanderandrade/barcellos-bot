# server.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import logging
import openai
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

produtos = [
    "BICICLETA CONSIG. TRINX TEMPO 3.0 CINZA / AZUL TAM. 54 - LUIS FERNANDO DOS SANTOS",
    "BICICLETA GROOVE SKA 90 29 12V 2024"
]

@app.route('/')
def index():
    return render_template('index.html')

def simular_processamento():
    print("🚀 Iniciando processo de análise e atualização de produtos...")

    for nome in produtos:
        if "CONSIG" in nome.upper() or any(p in nome.upper() for p in ["LUIS", "FERNANDO", "SANTOS"]):
            status = 'red'
        else:
            status = 'blue'

        print(f"[{status.upper()}] {nome}")
        print(f"[EMITINDO] {nome} -> {status}")
        socketio.emit('status', {'nome': nome, 'status': status})
        time.sleep(1)

    print("✅ Processo finalizado.")
    socketio.emit('finalizado', {'mensagem': '✅ Processo finalizado.'})

@socketio.on('connect')
def handle_connect(auth):
    print("✅ Cliente conectado via Socket.IO")
    threading.Thread(target=simular_processamento).start()

if __name__ == '__main__':
    print("[INFO] Iniciando servidor Flask...")
    socketio.run(app, debug=True)
