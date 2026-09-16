# Makefile do MCP Security Lab
# Uso educacional.

PY ?= python
export MCP_HMAC_SECRET ?= segredo-de-desenvolvimento
export APP_API_KEY ?= chave-de-desenvolvimento

.PHONY: setup lab1 attack secure test clean

setup:
	$(PY) -m pip install -r requirements.txt

lab1:
	$(PY) client/client.py vuln

attack:
	$(PY) attacks/tool_poisoning.py
	$(PY) attacks/prompt_injection.py
	$(PY) attacks/rug_pull.py

secure:
	$(PY) client/client.py secure

test:
	$(PY) -m pytest -q

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
