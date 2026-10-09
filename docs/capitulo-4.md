# Capítulo 4 — Defesas no Servidor Seguro

⚠️ Material educacional.

Este capítulo detalha como o `secure_server/` corrige cada uma das 9
vulnerabilidades. A ideia central é **defesa em profundidade**: autenticação na
borda (B2), autorização por papel e validação em cada acesso a recurso (B3).

## Visão geral das mitigações

| # | Vulnerabilidade | Mitigação | Arquivo |
|---|-----------------|-----------|---------|
| 1 | Segredo hardcoded | `os.getenv("APP_API_KEY")`, retorna só `"configured"` | `tools.py` |
| 2 | Path traversal | `_safe_path()` com `.resolve()` confinado ao BASE_DIR | `tools.py` |
| 3 | Command injection | `shlex.split` + `shell=False` + allowlist de hosts | `tools.py` |
| 4 | Falta de auth | `@require_auth` + token HMAC obrigatório | `auth.py` |
| 5 | Excesso de privilégio | RBAC via `ROLE_ALLOWLIST` | `auth.py` |
| 6 | Tool poisoning | `_sanitize()` nas descrições | `server.py` |
| 7 | IDOR | verifica `claims["user_id"]` / `role` | `tools.py` |
| 8 | Resource exposure | `internal_config` não existe no servidor seguro | `tools.py` |
| 9 | Prompt inseguro | `prompt/get` não implementado | `server.py` |

## #1 — Segredo via ambiente

Nunca embuta segredos no código. O servidor seguro lê de variável de ambiente e,
como defesa extra, **não retorna o valor** — apenas confirma presença.

```python
secret = os.getenv("APP_API_KEY")
if not secret:
    raise AuthError("APP_API_KEY nao configurada")
return "configured"
```

## #2 — Path traversal: `_safe_path()`

Resolve o caminho absoluto e confirma que ele está dentro do diretório base.
`../../etc/passwd` é bloqueado porque sai do `_BASE_DIR`.

```python
def _safe_path(path: str) -> Path:
    candidate = (_BASE_DIR / path).resolve()
    if _BASE_DIR not in candidate.parents and candidate != _BASE_DIR:
        raise AuthError("acesso fora do diretorio permitido")
    return candidate
```

## #3 — Command injection: `shlex` + `shell=False` + allowlist

Sem shell, metacaracteres como `;` e `|` não são interpretados. Além disso, o
host precisa estar na allowlist.

```python
if host not in _ALLOWED_HOSTS:
    raise AuthError(f"host nao permitido: {host}")
args = shlex.split(f"ping -c 1 {host}")
subprocess.run(args, shell=False, capture_output=True, text=True)
```

## #4 / #5 — Autenticação HMAC + RBAC

Token no formato `user:role:exp:hmac`, verificado com **comparação em tempo
constante** (`hmac.compare_digest`) para evitar timing attack. O decorator
`require_auth` valida o token e checa a allowlist por papel antes de executar.

```python
ROLE_ALLOWLIST = {
    "admin": {"get_secret", "read_file", "list_dir", "get_user_data"},
    "user":  {"read_file", "get_user_data"},
    "guest": {"read_file"},
}
```

## #6 — Sanitização de descrições

`_sanitize()` remove comentários HTML inteiros e trunca no primeiro gatilho de
injeção, eliminando o payload por completo em vez de apagar só uma palavra.

## #7 — IDOR: checagem de identidade

```python
if claims["role"] != "admin" and claims["user_id"] != user_id:
    raise AuthError("acesso negado: voce so pode ver seus proprios dados")
```

## #8 / #9 — Reduzir superfície

O servidor seguro simplesmente **não expõe** `internal_config` nem um
`prompt/get` inseguro. A melhor defesa para uma superfície é não tê-la.

## Comprovação

```bash
export MCP_HMAC_SECRET="segredo-de-teste"
export APP_API_KEY="chave-de-teste"
python -m pytest -q          # 10 testes cobrindo #1,#2,#3,#4,#5,#7
python client/client.py secure   # recusa por falta de token
```

As mitigações #6, #8 e #9 são demonstradas pelos scripts de `attacks/` e pela
comparação de `tools/list` entre os dois servidores (não por pytest).

## Além do lab (próximos passos)

- **OAuth 2.0** no lugar de tokens HMAC caseiros para cenários reais.
- **HashiCorp Vault** (ou AWS Secrets Manager) para gestão de segredos.
- **AI Firewall / guardrails** em runtime para filtrar prompt injection.

## Exercício

1. Rode `pytest` e associe cada teste à vulnerabilidade que ele cobre.
2. Adicione um novo papel `auditor` com acesso somente a `read_file` e escreva
   um teste de RBAC para ele.
3. Esboce como trocar o token HMAC por OAuth 2.0 sem mudar as tools.

---

_Última atualização: 8 de outubro de 2026._
