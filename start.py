# start.py
import os
import subprocess

def start_bot():
    # Carrega o .env automaticamente se existir
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()

    print("Iniciando Barcellos Bot...")
    # Pode ser main.py ou server.py, conforme o seu fluxo principal
    subprocess.run(["python", "main.py"], check=True)

if __name__ == "__main__":
    start_bot()
