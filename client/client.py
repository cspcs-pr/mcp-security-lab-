"""
Cliente MCP didatico (JSON-RPC 2.0 sobre stdin/stdout).

Inicia um servidor (vulneravel ou seguro) como subprocesso e troca
mensagens JSON-RPC linha a linha.

Uso:
    python client/client.py vuln      # conversa com o servidor vulneravel
    python client/client.py secure    # conversa com o servidor seguro
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERVERS = {
    "vuln": ["python", "-m", "vulnerable_server.server"],
    "secure": ["python", "-m", "secure_server.server"],
}


class MCPClient:
    """Cliente minimo que envia requisicoes JSON-RPC e le respostas."""

    def __init__(self, server_cmd):
        self._proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            cwd=str(ROOT),
        )
        self._id = 0

    def call(self, method, params=None):
        self._id += 1
        req = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            req["params"] = params
        self._proc.stdin.write(json.dumps(req) + "\n")
        self._proc.stdin.flush()
        line = self._proc.stdout.readline()
        return json.loads(line) if line else None

    def close(self):
        try:
            self._proc.stdin.close()
        finally:
            self._proc.terminate()


def demo(target: str):
    cmd = SERVERS[target]
    client = MCPClient(cmd)
    try:
        print(f"== Servidor: {target} ==")
        print("tools/list ->", client.call("tools/list"))

        if target == "vuln":
            # Sem auth: qualquer chamada funciona (demonstra vuln #4)
            print("get_secret ->", client.call(
                "tools/call", {"name": "get_secret"}))
        else:
            # Sem token o servidor seguro recusa (mitiga #4)
            print("sem token ->", client.call(
                "tools/call", {"name": "get_secret"}))
    finally:
        client.close()


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "vuln"
    if target not in SERVERS:
        print(f"alvo invalido: {target}. Use 'vuln' ou 'secure'.")
        sys.exit(1)
    demo(target)


if __name__ == "__main__":
    main()
