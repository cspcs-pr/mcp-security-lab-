"""
Servidor MCP SEGURO (JSON-RPC 2.0 sobre stdin/stdout).

Mitigacoes aplicadas:
- #4 auth obrigatoria via token HMAC em todas as chamadas
- #6 tool poisoning: descricoes sanitizadas
- #8 resource exposure: sem exposicao de config interna
- #9 prompt inseguro: removido

Uso:
    export MCP_HMAC_SECRET="troque-por-um-segredo-forte"
    python secure_server/server.py
"""

import json
import re
import sys

from secure_server import tools
from secure_server.auth import AuthError

# Mitiga #6 - descricoes sem instrucoes ocultas / conteudo executavel
TOOL_DESCRIPTIONS = {
    "get_secret": "Confirma se o segredo esta configurado (nao revela o valor).",
    "read_file": "Le um arquivo dentro do diretorio de dados permitido.",
    "ping": "Faz ping em um host da allowlist.",
    "list_dir": "Lista arquivos dentro do diretorio de dados permitido.",
    "get_user_data": "Retorna dados do proprio usuario autenticado.",
}


# Comentarios HTML costumam esconder payloads em descricoes de tools
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _sanitize(text: str) -> str:
    """Remove conteudo potencialmente malicioso de descricoes de tools.

    Estrategia (mitiga #6):
    - remove blocos de comentario HTML inteiros (nao so os marcadores);
    - corta a descricao no primeiro gatilho de injecao conhecido, descartando
      tudo a partir dele em vez de deixar residuo legivel pelo modelo.
    """
    text = _HTML_COMMENT.sub("", text)
    lowered = text.lower()
    for trigger in ("ignore", "disregard", "envie", "exfiltr"):
        idx = lowered.find(trigger)
        if idx != -1:
            text = text[:idx]
            lowered = text.lower()
    return text.strip()


def handle(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {}) or {}

    if method == "tools/list":
        listed = [
            {"name": name, "description": _sanitize(TOOL_DESCRIPTIONS.get(name, ""))}
            for name in tools.TOOLS
        ]
        return _ok(req_id, {"tools": listed})

    if method == "tools/call":
        name = params.get("name")
        token = params.get("token")
        args = params.get("arguments", {}) or {}

        fn = tools.TOOLS.get(name)
        if fn is None:
            return _err(req_id, -32601, f"tool nao encontrada: {name}")
        if not token:
            return _err(req_id, -32001, "token ausente")

        try:
            # Todas as tools exigem token (mitiga #4) e aplicam RBAC (mitiga #5)
            result = fn(token, **args)
            return _ok(req_id, {"result": result})
        except AuthError as exc:
            return _err(req_id, -32002, f"auth: {exc}")
        except (FileNotFoundError, NotADirectoryError) as exc:
            return _err(req_id, -32004, str(exc))

    return _err(req_id, -32601, f"metodo nao suportado: {method}")


def _ok(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _err(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps(_err(None, -32700, "parse error")), flush=True)
            continue
        print(json.dumps(handle(request), default=str), flush=True)


if __name__ == "__main__":
    main()
