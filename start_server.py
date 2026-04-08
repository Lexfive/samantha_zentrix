"""
start_server.py
Script de inicialização do Samantha_Zentrix.
Lexfive, todas as mudanças serão logadas em changes.log para controle remoto.
"""

import os
import subprocess
import sys
from datetime import datetime

# 1. Caminho do projeto
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, "venv")

# 2. Log de mudanças
LOG_FILE = os.path.join(PROJECT_DIR, "changes.log")

def log_change(message: str):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

# 3. Ativar virtualenv
activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
if not os.path.exists(activate_script):
    log_change("ERROR: virtualenv não encontrado.")
    sys.exit("Virtualenv não encontrado. Crie com: python -m venv venv")

log_change("Ativando virtualenv")
if os.name == "nt":
    subprocess.run(f"{activate_script} && pip install -r requirements.txt", shell=True)
else:
    subprocess.run(f"source {activate_script} && pip install -r requirements.txt", shell=True)

log_change("Dependências instaladas/atualizadas")

# 4. Configurações de ambiente (para produção ou dev)
os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY", "CHANGE_ME_RANDOM_KEY")
log_change("SECRET_KEY definido")

# 5. Inicializa servidor Uvicorn
log_change("Iniciando servidor Uvicorn")
subprocess.run(f"{os.path.join(VENV_DIR, 'Scripts', 'python')} -m uvicorn main:app --reload", shell=True)