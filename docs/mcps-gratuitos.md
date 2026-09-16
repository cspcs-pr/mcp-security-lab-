# 🧩 MCPs Gratuitos para Estudar e Praticar

⚠️ Material educacional. Sempre revise o código e as permissões de um servidor
MCP antes de conectá-lo — lembre-se das aulas de tool poisoning e rug pull.

Todos os itens abaixo são open source e gratuitos. Muitos rodam sem API key.

---

## Servidores de referência oficiais

Mantidos pelo steering group do MCP no repositório
[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers).
São implementações de referência, feitas como exemplos educacionais (não
"production-ready" por padrão — avalie seu próprio modelo de ameaças).
Conteúdo resumido da documentação oficial; rephrase para conformidade de licença.

| Servidor | Para que serve | Executar |
|----------|----------------|----------|
| **Everything** | Servidor de teste com prompts, resources e tools | `npx -y @modelcontextprotocol/server-everything` |
| **Fetch** | Buscar e converter conteúdo web para uso pelo LLM | `uvx mcp-server-fetch` |
| **Filesystem** | Operações de arquivo com controle de acesso configurável | `npx -y @modelcontextprotocol/server-filesystem /caminho/permitido` |
| **Git** | Ler, buscar e manipular repositórios Git | `uvx mcp-server-git --repository /caminho/repo` |
| **Memory** | Memória persistente baseada em grafo de conhecimento | `npx -y @modelcontextprotocol/server-memory` |
| **Sequential Thinking** | Raciocínio passo a passo / reflexivo | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| **Time** | Conversão de tempo e fuso horário | `uvx mcp-server-time` |

> No Windows, envolva `npx` com `cmd /c` na config do cliente. Entradas `uvx`
> ficam iguais. Requer Node/`npx` (para os TypeScript) e `uv`/`uvx` (para os Python).

### Exemplo de configuração (formato mcp.json)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/caminho/permitido"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/caminho/repo"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

No Windows, para as entradas `npx`, troque `"command": "npx"` por
`"command": "cmd"` e adicione `"/c", "npx"` no início de `args`.

---

## Onde encontrar mais servidores

- **MCP Registry** — catálogo oficial de servidores publicados:
  [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/)
- **Documentação oficial** — guias e melhores práticas:
  [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Listas comunitárias "awesome"** (variam em qualidade — aplique senso crítico):
  - [TensorBlock/awesome-mcp-servers](https://github.com/TensorBlock/awesome-mcp-servers)
  - [AlexMili/Awesome-MCP](https://github.com/AlexMili/Awesome-MCP)

> Servidores arquivados (GitHub, GitLab, PostgreSQL, SQLite, Puppeteer, Redis,
> Slack, Sentry, Brave Search etc.) foram movidos para
> [servers-archived](https://github.com/modelcontextprotocol/servers-archived);
> alguns têm substitutos oficiais mantidos por outras organizações.

---

## Como usar estes MCPs para praticar segurança

1. **Filesystem** — configure um diretório permitido e tente path traversal
   fora dele. Compare com o `_safe_path` do nosso `secure_server`.
2. **Fetch** — observe como conteúdo externo é trazido; pense em prompt
   injection vindo de páginas web (dado não confiável).
3. **Git** — inspecione que operações a tool expõe; relacione com RBAC/allowlist.
4. **Memory** — pense em envenenamento de memória (dados persistidos maliciosos).
5. Para qualquer servidor de terceiros, antes de conectar:
   - leia a descrição das tools (procure instruções ocultas — tool poisoning);
   - fixe a versão (evita rug pull / typosquatting);
   - rode com o mínimo de privilégio possível.

---

## ⚠️ Aviso

Conectar um MCP dá a ele acesso real a recursos (arquivos, rede, dados). Trate
cada servidor como código de terceiros: revise, fixe versão e limite escopo.
Nunca aponte um servidor de terceiros para diretórios sensíveis sem entender o
que ele faz.

_Fontes: documentação oficial do Model Context Protocol. Conteúdo reescrito para
conformidade com restrições de licença._
