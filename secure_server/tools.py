"""
Ferramentas (tools) do servidor MCP SEGURO.

Cada funcao corrige uma das 9 vulnerabilidades do servidor vulneravel.
Todas exigem 'claims' (identidade autenticada) como primeiro parametro,
injetado pelo decorator require_auth.
"""

import os
import shlex
import subprocess
from pathlib import Path

from secure_server.auth import AuthError, require_auth

# Diretorio raiz permitido para leitura (mitiga vuln #2)
_BASE_DIR = Path(os.getenv("MCP_DATA_DIR", "./data")).resolve()

# Allowlist de hosts para ping (mitiga vuln #3/#5)
_ALLOWED_HOSTS = {"127.0.0.1", "localhost", "8.8.8.8", "1.1.1.1"}

_USER_DATA = {
    "alice": {"saldo": 1000, "email": "alice@example.com"},
    "bob": {"saldo": 50, "email": "bob@example.com"},
}


# ---------------------------------------------------------------------------
# Mitiga #1 - Segredo via ambiente, nunca hardcoded
# ---------------------------------------------------------------------------
@require_auth("get_secret")
def get_secret(claims: dict) -> str:
    secret = os.getenv("APP_API_KEY")
    if not secret:
        raise AuthError("APP_API_KEY nao configurada")
    # Nao retorna o valor bruto; apenas confirma presenca (defesa em profundidade)
    return "configured"


# ---------------------------------------------------------------------------
# Mitiga #2 - Path traversal via _safe_path()
# ---------------------------------------------------------------------------
def _safe_path(path: str) -> Path:
    candidate = (_BASE_DIR / path).resolve()
    if _BASE_DIR not in candidate.parents and candidate != _BASE_DIR:
        raise AuthError("acesso fora do diretorio permitido")
    return candidate


@require_auth("read_file")
def read_file(claims: dict, path: str) -> str:
    safe = _safe_path(path)
    if not safe.is_file():
        raise FileNotFoundError(f"arquivo nao encontrado: {path}")
    return safe.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Mitiga #3 - Command injection via shlex + shell=False + allowlist
# ---------------------------------------------------------------------------
@require_auth("ping")
def ping(claims: dict, host: str) -> str:
    if host not in _ALLOWED_HOSTS:
        raise AuthError(f"host nao permitido: {host}")
    # shell=False + args em lista evita injecao
    args = shlex.split(f"ping -c 1 {host}")
    result = subprocess.run(args, shell=False, capture_output=True, text=True)
    return result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Mitiga #5 - Excesso de privilegio: lista apenas dentro do BASE_DIR
# ---------------------------------------------------------------------------
@require_auth("list_dir")
def list_dir(claims: dict, path: str = ".") -> list:
    safe = _safe_path(path)
    if not safe.is_dir():
        raise NotADirectoryError(f"nao e diretorio: {path}")
    return [p.name for p in safe.iterdir()]


# ---------------------------------------------------------------------------
# Mitiga #7 - IDOR: usuario so acessa os proprios dados
# ---------------------------------------------------------------------------
@require_auth("get_user_data")
def get_user_data(claims: dict, user_id: str) -> dict:
    if claims["role"] != "admin" and claims["user_id"] != user_id:
        raise AuthError("acesso negado: voce so pode ver seus proprios dados")
    return _USER_DATA.get(user_id, {})


# Registro de tools (nomes espelham o servidor vulneravel para comparacao)
TOOLS = {
    "get_secret": get_secret,
    "read_file": read_file,
    "ping": ping,
    "list_dir": list_dir,
    "get_user_data": get_user_data,
}
