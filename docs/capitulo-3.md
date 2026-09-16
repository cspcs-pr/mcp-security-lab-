# Capítulo 3 — Modelagem de Ameaças (STRIDE) no MCP

⚠️ Material educacional.

## Diagrama de fluxo de dados (DFD) simplificado

```
[Host/LLM] --(1)--> [Cliente MCP] --(2)--> [Servidor MCP] --(3)--> [Recursos: FS, shell, dados]
```

Trust boundaries (fronteiras de confiança):
- **B1** entre Host/LLM e Cliente MCP
- **B2** entre Cliente MCP e Servidor MCP
- **B3** entre Servidor MCP e os recursos do sistema

## STRIDE aplicado

| Categoria | Ameaça no MCP | Mitigação no lab |
|-----------|---------------|------------------|
| **S**poofing | Cliente ou servidor se passar por outro | Tokens HMAC (`secure_server/auth.py`) |
| **T**ampering | Adulterar payload JSON-RPC ou definição de tool | Assinatura HMAC + pinning de tool (`attacks/rug_pull.py`) |
| **R**epudiation | Ações sem rastro | Claims com `user_id` para logging/auditoria |
| **I**nformation Disclosure | Vazar segredo / config interna | `os.getenv` (#1), sem `internal_config` no servidor seguro (#8) |
| **D**enial of Service | Comandos custosos / loops | Allowlist de hosts e tools, escopo restrito |
| **E**levation of Privilege | Chamar tool sem permissão | RBAC via `ROLE_ALLOWLIST` (#5) |

## Trust boundaries e riscos-chave

- **B1**: prompt injection e tool poisoning atravessam o LLM. Defesa: sanitizar descrições (#6) e não expor prompts inseguros (#9).
- **B2**: falta de autenticação. Defesa: exigir token válido em toda chamada (#4).
- **B3**: acesso irrestrito a FS/shell. Defesa: `_safe_path` (#2), `shlex`+`shell=False`+allowlist (#3), escopo por papel (#5).

## Exercício

1. Desenhe o DFD do seu próprio servidor MCP.
2. Marque as três trust boundaries.
3. Para cada letra de STRIDE, aponte uma ameaça concreta e a mitigação correspondente.
4. Priorize os riscos (ex.: DREAD ou simples alto/médio/baixo).

## Ferramentas de apoio

- IriusRisk — modelagem de ameaças assistida.
- STRIDEGPT — geração de cenários STRIDE com IA.
