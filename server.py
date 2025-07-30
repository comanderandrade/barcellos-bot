# server.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
from config import PORT
from main import executar_processo


app = Flask(__name__)
import os
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

def background_task():
    executar_processo(socketio)

if __name__ == '__main__':
    Thread(target=background_task).start()
    socketio.run(app, port=PORT, debug=True)
