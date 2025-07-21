# utils.py

import html
import json
from datetime import datetime

def salvar_log_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def formatar_html(texto):
    return html.escape(texto).replace("\n", "<br>")
