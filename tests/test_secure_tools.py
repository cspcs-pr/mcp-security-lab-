"""
Testes das mitigacoes do servidor SEGURO.

Executar:
    export MCP_HMAC_SECRET="segredo-de-teste"
    export APP_API_KEY="chave-de-teste"
    pytest -q
"""

import importlib
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Garante segredos necessarios ANTES de importar os modulos que os leem
os.environ.setdefault("MCP_HMAC_SECRET", "segredo-de-teste")
os.environ.setdefault("APP_API_KEY", "chave-de-teste")

from secure_server import auth  # noqa: E402
from secure_server import tools  # noqa: E402


@pytest.fixture
def admin_token():
    return auth.issue_token("alice", "admin")


@pytest.fixture
def user_token():
    return auth.issue_token("bob", "user")


# --- Mitiga #4: autenticacao obrigatoria -----------------------------------
def test_token_valido_gera_claims(admin_token):
    claims = auth.verify_token(admin_token)
    assert claims["user_id"] == "alice"
    assert claims["role"] == "admin"


def test_token_adulterado_e_rejeitado(admin_token):
    forjado = admin_token[:-1] + ("0" if admin_token[-1] != "0" else "1")
    with pytest.raises(auth.AuthError):
        auth.verify_token(forjado)


def test_chamada_sem_token_falha():
    with pytest.raises(auth.AuthError):
        tools.get_user_data("token-invalido", user_id="bob")


# --- Mitiga #5: RBAC / allowlist -------------------------------------------
def test_rbac_bloqueia_tool_fora_do_papel(user_token):
    # 'user' nao tem 'list_dir' na allowlist
    with pytest.raises(auth.AuthError):
        tools.list_dir(user_token, path=".")


def test_rbac_permite_tool_do_papel(tmp_path):
    os.environ["MCP_DATA_DIR"] = str(tmp_path)
    importlib.reload(tools)
    admin = auth.issue_token("alice", "admin")
    (tmp_path / "a.txt").write_text("ok", encoding="utf-8")
    assert "a.txt" in tools.list_dir(admin, path=".")


# --- Mitiga #2: path traversal ---------------------------------------------
def test_path_traversal_bloqueado(tmp_path):
    os.environ["MCP_DATA_DIR"] = str(tmp_path)
    importlib.reload(tools)
    admin = auth.issue_token("alice", "admin")
    with pytest.raises(auth.AuthError):
        tools.read_file(admin, path="../../etc/passwd")


# --- Mitiga #3: command injection ------------------------------------------
def test_ping_host_fora_da_allowlist():
    admin = auth.issue_token("alice", "admin")
    # 'ping' nao esta na allowlist de nenhum papel -> RBAC barra antes
    with pytest.raises(auth.AuthError):
        tools.ping(admin, host="8.8.8.8; rm -rf /")


# --- Mitiga #7: IDOR --------------------------------------------------------
def test_idor_usuario_nao_ve_dados_de_outro(user_token):
    with pytest.raises(auth.AuthError):
        tools.get_user_data(user_token, user_id="alice")


def test_usuario_ve_proprios_dados(user_token):
    dados = tools.get_user_data(user_token, user_id="bob")
    assert dados["email"] == "bob@example.com"


# --- Mitiga #1: segredo via ambiente ---------------------------------------
def test_get_secret_nao_revela_valor():
    admin = auth.issue_token("alice", "admin")
    assert tools.get_secret(admin) == "configured"
