import logging
import os

# Criar pasta logs se não existir
os.makedirs("logs", exist_ok=True)

# Logger principal
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Loggers específicos
bling_logger = logging.getLogger("bling")
chatgpt_logger = logging.getLogger("chatgpt")

# Handlers separados
bling_handler = logging.FileHandler("logs/bling.log")
chatgpt_handler = logging.FileHandler("logs/chatgpt.log")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
bling_handler.setFormatter(formatter)
chatgpt_handler.setFormatter(formatter)

bling_logger.addHandler(bling_handler)
chatgpt_logger.addHandler(chatgpt_handler)

# Funções auxiliares
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message, exc_info=True)

def log_bling(message, level="info"):
    if level == "error":
        bling_logger.error(message, exc_info=True)
    else:
        bling_logger.info(message)

def log_chatgpt(message, level="info"):
    if level == "error":
        chatgpt_logger.error(message, exc_info=True)
    else:
        chatgpt_logger.info(message)
