from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
from config import PORT
from main import executar_processo
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

def background_task():
    executar_processo(socketio)

if __name__ == '__main__':
    thread = Thread(target=background_task)
    thread.start()
    socketio.run(app, port=PORT)
