# 🔐 MCP Security Lab — Study Kit

Laboratório prático de segurança para o Model Context Protocol (MCP).

⚠️ Uso exclusivamente educacional. Não execute ataques contra sistemas sem autorização.

---

## 📁 Estrutura do Projeto

```
mcp-security-lab/
├── .github/workflows/ci.yml
├── .github/workflows/codeql.yml
├── vulnerable_server/server.py
├── vulnerable_server/tools.py
├── secure_server/server.py
├── secure_server/tools.py
├── secure_server/auth.py
├── client/client.py
├── attacks/tool_poisoning.py
├── attacks/prompt_injection.py
├── attacks/rug_pull.py
├── tests/test_secure_tools.py
├── requirements.txt
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## 🎯 Mapeamento de Tópicos

| Cap | Tema | Arquivo |
|-----|------|---------|
| 1 | Fundamentos MCP | client/client.py |
| 2 | Ataques | attacks/*.py |
| 3 | Modelagem de ameaças | docs/capitulo-3.md |
| 4 | Defesas | secure_server/*.py |
| 5 | DevSecOps | .github/workflows/*.yml |
| 6 | Supply chain | docs/capitulo-6.md |

### 📚 Material de apoio

- [Guia prático de testes](docs/guia-pratico.md) — roteiro passo a passo por vulnerabilidade
- [Arquitetura e trust boundaries](docs/arquitetura.md) — diagrama do fluxo MCP
- [Quiz de autoavaliação](docs/quiz.md) — perguntas e gabarito
- [MCPs gratuitos](docs/mcps-gratuitos.md) — servidores open source para praticar

---

## 🔐 9 Vulnerabilidades × Mitigações

| # | Vulnerabilidade | Mitigação |
|---|-----------------|-----------|
| 1 | Segredo hardcoded | os.getenv() obrigatório |
| 2 | Path traversal | _safe_path() com .resolve() |
| 3 | Command injection | shlex.split + shell=False |
| 4 | Falta de auth | @require_auth + HMAC |
| 5 | Excess privilege | Allowlist + RBAC |
| 6 | Tool poisoning | Descrição sanitizada |
| 7 | IDOR | Verificação de identidade |
| 8 | Resource exposure | Escopo público explícito |
| 9 | Prompt inseguro | Removido no servidor seguro |

---

## 🚀 Como usar (3 formas)

### Forma 1 — Termux (Android, recomendado)

```bash
pkg install git zip python nano -y
mkdir -p ~/lab && cd ~/lab
nano build_lab.sh
# colar o conteúdo do ARQUIVO 2 (script gerador)
# salvar: Ctrl+O, Enter | sair: Ctrl+X
bash build_lab.sh

# Copiar o zip para Download (visível no gerenciador de arquivos)
termux-setup-storage
cp mcp-security-lab.zip /sdcard/Download/
```

### Forma 2 — iSH (iOS)

```bash
apk add bash zip python3 py3-pip nano
mkdir -p ~/lab && cd ~/lab
nano build_lab.sh
# colar o conteúdo do ARQUIVO 2
sh build_lab.sh
ls -lh mcp-security-lab.zip
```

### Forma 3 — PC (mais confortável)

```bash
mkdir ~/lab && cd ~/lab
nano build_lab.sh
# colar o conteúdo do ARQUIVO 2
bash build_lab.sh
unzip mcp-security-lab.zip
cd mcp-security-lab
make setup
make lab1
make attack
make secure
make test
```

---

## 📋 Checklist de Estudo (60 dias)

### Semana 1-2 — Fundamentos (Cap 1)
- [ ] Entender arquitetura Hosts/Clientes/Servidores
- [ ] Rodar `python client/client.py`
- [ ] Listar tools do servidor vulnerável
- [ ] Observar comunicação JSON-RPC 2.0

### Semana 3-4 — Ataques (Cap 2)
- [ ] Tool Poisoning (`attacks/tool_poisoning.py`)
- [ ] Prompt Injection (`attacks/prompt_injection.py`)
- [ ] Rug Pull (`attacks/rug_pull.py`)
- [ ] Mapear primitivas no MITRE ATLAS
- [ ] Estudar cross-server privilege escalation

### Semana 5-6 — Modelagem (Cap 3)
- [ ] Aplicar STRIDE em DFD MCP
- [ ] Identificar trust boundaries
- [ ] Documentar riscos com IriusRisk
- [ ] Praticar com STRIDEGPT

### Semana 7-8 — Defesas (Cap 4)
- [ ] Rodar `python secure_server/server.py`
- [ ] Comparar comportamentos
- [ ] Rodar `make test`
- [ ] Implementar OAuth 2.0
- [ ] Integrar HashiCorp Vault

### Semana 9 — DevSecOps (Cap 5)
- [ ] Estudar `.github/workflows/ci.yml`
- [ ] Entender SAST + DAST em CI
- [ ] Configurar CodeQL
- [ ] Simular pipeline envenenado

### Semana 10 — Supply Chain (Cap 6)
- [ ] Gerar SBOM
- [ ] Assinar release
- [ ] Aplicar SLSA
- [ ] Implementar provenance attestations

---

## 🧰 Ferramentas citadas no curso

| Ferramenta | Uso |
|------------|-----|
| IriusRisk | Modelagem de ameaças |
| STRIDEGPT | Modelagem assistida por IA |
| HashiCorp Vault | Gestão de segredos |
| AI Firewall | Proteção em runtime |
| MITRE ATLAS | Ameaças em IA |
| MITRE ATT&CK | Táticas gerais |
| OWASP Top 10 LLM | Vulnerabilidades LLM |
| OWASP ASVS | Verificação de segurança |
| NIST AI RMF | Gestão de risco IA |
| NIST SP 800-53 | Controles |
| ISO/IEC 42001 | Governança IA |
| SLSA | Integridade de build |
| SCVS | Verificação de componentes |

---

## 📌 Comandos rápidos — Pocket Edition

Alternativa sem estrutura de pastas (arquivo único):

```bash
python mcp-lab-pocket.py attacks   # mostra os 6 vetores
python mcp-lab-pocket.py test      # valida mitigações
python mcp-lab-pocket.py vuln      # servidor vulnerável
python mcp-lab-pocket.py secure    # servidor seguro
```

---

## ⚠️ Aviso Legal

Uso exclusivamente educacional. O uso indevido pode configurar crime:

- **Brasil:** Lei 12.737/2012 (Lei Carolina Dieckmann)
- **EUA:** Computer Fraud and Abuse Act (CFAA)
- **UE:** Diretiva 2013/40/UE

Nunca execute os vetores em `attacks/` contra sistemas que você não possui
ou para os quais não tem autorização escrita.
