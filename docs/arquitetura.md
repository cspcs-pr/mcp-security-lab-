# 🏗️ Arquitetura do Lab e Trust Boundaries

⚠️ Material educacional.

O diagrama mostra o fluxo MCP (Host/LLM → Cliente → Servidor → Recursos) e as
três fronteiras de confiança (B1, B2, B3), com os ataques e defesas em cada uma.

```mermaid
flowchart LR
    subgraph HostZone["Zona do Host / LLM"]
        LLM["Host / LLM"]
    end

    subgraph ClientZone["Zona do Cliente"]
        Client["Cliente MCP<br/>client/client.py"]
    end

    subgraph ServerZone["Zona do Servidor"]
        Vuln["Servidor Vulneravel<br/>vulnerable_server/"]
        Secure["Servidor Seguro<br/>secure_server/"]
    end

    subgraph ResZone["Recursos do Sistema"]
        FS[("Filesystem")]
        Shell["Shell / Comandos"]
        Data[("Dados de Usuario")]
    end

    LLM -->|"B1: prompt/tools"| Client
    Client -->|"B2: JSON-RPC 2.0"| Vuln
    Client -->|"B2: JSON-RPC + token"| Secure
    Vuln --> FS
    Vuln --> Shell
    Vuln --> Data
    Secure -->|"B3: _safe_path / allowlist"| FS
    Secure -->|"B3: shlex + shell=False"| Shell
    Secure -->|"B3: RBAC / IDOR check"| Data

    classDef danger fill:#ffe0e0,stroke:#c00;
    classDef safe fill:#e0ffe0,stroke:#0a0;
    class Vuln danger;
    class Secure safe;
```

## Trust boundaries

- **B1 — Host/LLM ↔ Cliente**: superfície de prompt injection (#9) e tool
  poisoning (#6). Defesa: sanitizar descrições e não expor prompts inseguros.
- **B2 — Cliente ↔ Servidor**: superfície de falta de autenticação (#4).
  Defesa: token HMAC obrigatório em toda chamada + RBAC (#5).
- **B3 — Servidor ↔ Recursos**: superfície de path traversal (#2), command
  injection (#3), IDOR (#7) e exposição de recursos (#8). Defesa: `_safe_path`,
  `shlex`+`shell=False`+allowlist, verificação de identidade e escopo explícito.

## Como ler o contraste

- O **servidor vulnerável** acessa Filesystem, Shell e Dados sem qualquer
  controle nas fronteiras.
- O **servidor seguro** aplica um controle específico em cada aresta B3, além de
  exigir autenticação em B2.
