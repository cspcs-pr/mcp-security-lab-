# Capítulo 1 — Fundamentos do MCP

⚠️ Material educacional.

O **Model Context Protocol (MCP)** é um protocolo aberto que padroniza como
aplicações de IA (hosts/LLMs) se conectam a ferramentas e fontes de dados
externas. Em vez de cada integração ser feita de forma ad hoc, o MCP define um
contrato comum de comunicação.

## Arquitetura: Host, Cliente e Servidor

```
[Host / LLM] <--> [Cliente MCP] <--> [Servidor MCP] <--> [Recursos]
```

- **Host / LLM** — a aplicação que usa o modelo (ex.: um assistente). Decide
  quando e quais tools chamar.
- **Cliente MCP** — intermediário que fala o protocolo. Inicia o servidor,
  descobre as tools e encaminha chamadas. Neste lab: `client/client.py`.
- **Servidor MCP** — expõe capacidades (tools, resources, prompts) e acessa os
  recursos reais do sistema (filesystem, shell, dados). Neste lab:
  `vulnerable_server/` e `secure_server/`.
- **Recursos** — arquivos, comandos, bancos de dados, APIs.

## Primitivas do MCP

| Primitiva | O que é | Exemplo no lab |
|-----------|---------|----------------|
| **Tools** | Funções que o modelo pode invocar | `get_secret`, `read_file`, `ping` |
| **Resources** | Dados que o servidor expõe para leitura | `internal_config` (vulnerável) |
| **Prompts** | Templates de prompt reutilizáveis | `prompt/get` (vulnerável, vuln #9) |

## Transporte: JSON-RPC 2.0

O MCP usa **JSON-RPC 2.0** como formato de mensagem. Neste lab o transporte é
`stdin/stdout` (o cliente inicia o servidor como subprocesso e troca uma
mensagem JSON por linha).

Uma requisição típica:

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
```

Uma resposta de sucesso:

```json
{"jsonrpc": "2.0", "id": 1, "result": {"tools": ["get_secret", "read_file"]}}
```

Uma resposta de erro:

```json
{"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "metodo nao suportado"}}
```

Os métodos usados no lab:
- `tools/list` — lista as tools disponíveis
- `tools/call` — invoca uma tool (no servidor seguro exige `token`)
- `prompt/get` — recupera o prompt de sistema (só existe no servidor vulnerável)

## Mão na massa

```bash
# Lista as tools do servidor vulnerável e chama get_secret (sem auth)
python client/client.py vuln

# Mesmo fluxo no servidor seguro: a chamada é recusada por falta de token
python client/client.py secure
```

Observe no `vulnerable_server/server.py` que `tools/call` executa a função sem
qualquer verificação. Já no `secure_server/server.py`, toda chamada passa por
`token` + RBAC antes de rodar.

## Por que isso importa para segurança

Cada aresta do fluxo (Host↔Cliente, Cliente↔Servidor, Servidor↔Recursos) é uma
**trust boundary** — ponto onde dados cruzam de uma zona de confiança para
outra. O resto do lab explora os ataques e defesas em cada fronteira. Veja
[arquitetura.md](arquitetura.md) para o mapa completo.

## Exercício

1. Rode `python client/client.py vuln` e identifique quais primitivas (tools,
   resources, prompts) o servidor expõe.
2. Envie manualmente uma requisição `tools/list` via `stdin` para cada servidor
   e compare as respostas.
3. Explique com suas palavras o papel de cada ator (Host, Cliente, Servidor).

---

_Última atualização: 8 de outubro de 2026._
