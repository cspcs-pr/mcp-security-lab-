# Capítulo 5 — DevSecOps e CI/CD

⚠️ Material educacional.

Este capítulo cobre como o lab integra segurança no pipeline de CI/CD usando os
workflows em `.github/workflows/`.

## Pipeline do lab

Há dois workflows:

| Workflow | Arquivo | O que faz |
|----------|---------|-----------|
| CI | `.github/workflows/ci.yml` | Testes (pytest) + SAST (Bandit) |
| CodeQL | `.github/workflows/codeql.yml` | Análise de código (SAST avançado) |

## `ci.yml` — Testes + SAST

Dispara em `push` e `pull_request` na branch `main`. Tem dois jobs:

### Job `test`
Instala dependências e roda a suíte com segredos de CI injetados via `env`:

```yaml
env:
  MCP_HMAC_SECRET: segredo-de-ci
  APP_API_KEY: chave-de-ci
```

> Aqui os segredos são valores de teste. Em um projeto real, use
> **GitHub Secrets** (`${{ secrets.NOME }}`) em vez de valores em texto claro.

### Job `sast`
Roda o **Bandit** (SAST para Python). Note o `|| true` ao final:

```yaml
run: bandit -r secure_server client attacks || true
```

O `|| true` impede que o job falhe, porque o `vulnerable_server/` contém falhas
**propositais** — ele é intencionalmente excluído da varredura. Em um projeto
real sem código vulnerável de propósito, você removeria o `|| true` para que
achados de SAST **bloqueiem** o merge.

## `codeql.yml` — Análise estática avançada

Dispara em push, PR e por agendamento semanal (`cron: "0 6 * * 1"`, toda
segunda às 06:00 UTC). Usa o CodeQL do GitHub para encontrar padrões de
vulnerabilidade em Python e publicar os achados na aba Security.

```yaml
permissions:
  actions: read
  contents: read
  security-events: write   # necessario para publicar alertas
```

## SAST × DAST

- **SAST** (Static Application Security Testing): analisa o código sem executá-lo
  (Bandit, CodeQL). Bom para pegar padrões inseguros cedo.
- **DAST** (Dynamic Application Security Testing): testa a aplicação em execução,
  enviando entradas maliciosas. Os scripts de `attacks/` funcionam como um DAST
  rudimentar contra os servidores do lab.

## Pipeline envenenado (exercício de ameaça)

Um atacante que comprometa o CI pode injetar código no build (ex.: um step que
baixa e executa um script, ou uma Action de terceiros não fixada). Defesas:

- Fixar Actions por **SHA** em vez de tag móvel (`uses: actions/checkout@<sha>`).
- Mínimo privilégio em `permissions:`.
- Revisar PRs que alterem arquivos em `.github/workflows/`.
- Separar segredos por ambiente e nunca ecoá-los em logs.

## Boas práticas de DevSecOps aplicadas aqui

1. Segurança roda a cada push/PR (shift-left).
2. SAST + testes como gates de qualidade.
3. Varredura agendada (CodeQL semanal) além da sob demanda.
4. Segredos fora do código (via `env`/secrets).

## Exercício

1. Leia `ci.yml` e explique por que o job `sast` usa `|| true`.
2. Altere o `codeql.yml` para fixar as Actions por SHA.
3. Adicione um step que gere o SBOM (ver [capítulo 6](capitulo-6.md)) e o
   publique como artefato do build.
4. Descreva um cenário de pipeline envenenado e a defesa correspondente.

---

_Última atualização: 8 de outubro de 2026._
