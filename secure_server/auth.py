"""
Autenticacao e autorizacao do servidor MCP SEGURO.

Mitigacoes:
- #4 Falta de auth  -> tokens HMAC verificados com comparacao constante
- #5 Excesso de privilegio -> RBAC via allowlist por papel (role)
"""

import hashlib
import hmac
import os
import time
from functools import wraps

# Segredo obrigatorio via ambiente (mitiga vuln #1). Sem valor padrao inseguro.
_SECRET = os.getenv("MCP_HMAC_SECRET")

# RBAC: papel -> tools permitidas (mitiga vuln #5)
ROLE_ALLOWLIST = {
    "admin": {"get_secret", "read_file", "list_dir", "get_user_data"},
    "user": {"read_file", "get_user_data"},
    "guest": {"read_file"},
}


class AuthError(Exception):
    """Falha de autenticacao ou autorizacao."""


def _require_secret() -> bytes:
    if not _SECRET:
        raise AuthError(
            "MCP_HMAC_SECRET nao definido. Configure a variavel de ambiente."
        )
    return _SECRET.encode("utf-8")


def issue_token(user_id: str, role: str, ttl: int = 3600) -> str:
    """Emite um token assinado: user:role:exp:hmac."""
    exp = int(time.time()) + ttl
    payload = f"{user_id}:{role}:{exp}"
    sig = hmac.new(_require_secret(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_token(token: str) -> dict:
    """Valida assinatura e expiracao. Retorna claims ou levanta AuthError."""
    try:
        user_id, role, exp, sig = token.split(":")
    except (ValueError, AttributeError):
        raise AuthError("token malformado")

    payload = f"{user_id}:{role}:{exp}"
    expected = hmac.new(_require_secret(), payload.encode(), hashlib.sha256).hexdigest()

    # Comparacao em tempo constante (evita timing attack)
    if not hmac.compare_digest(sig, expected):
        raise AuthError("assinatura invalida")

    if int(exp) < int(time.time()):
        raise AuthError("token expirado")

    return {"user_id": user_id, "role": role, "exp": int(exp)}


def can_call(role: str, tool_name: str) -> bool:
    """Verifica RBAC: o papel pode chamar a tool? (mitiga vuln #5)."""
    return tool_name in ROLE_ALLOWLIST.get(role, set())


def require_auth(tool_name: str):
    """Decorator que exige token valido e autorizacao RBAC (mitiga vuln #4/#5).

    A funcao decorada deve receber 'claims' como primeiro parametro.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(token: str, *args, **kwargs):
            claims = verify_token(token)
            if not can_call(claims["role"], tool_name):
                raise AuthError(
                    f"papel '{claims['role']}' nao autorizado para '{tool_name}'"
                )
            return func(claims, *args, **kwargs)

        return wrapper

    return decorator
