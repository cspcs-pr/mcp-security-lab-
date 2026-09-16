# Capítulo 6 — Supply Chain Security

⚠️ Material educacional.

## Riscos de cadeia de suprimentos no MCP

- Dependências maliciosas ou typosquatting em `requirements.txt`.
- Servidores MCP de terceiros com comportamento que muda após instalação (rug pull).
- Pipelines de CI/CD envenenados que injetam código no build.
- Falta de proveniência: não dá pra provar de onde veio o artefato.

## Práticas do capítulo

### 1. SBOM (Software Bill of Materials)
Gere um inventário de componentes:

```bash
pip install cyclonedx-bom
cyclonedx-py requirements -o sbom.json
```

### 2. Fixar versões (pinning)
Use versões exatas em `requirements.txt` para builds reprodutíveis e para
reduzir a janela de typosquatting.

### 3. Assinar releases
Assine tags/artefatos (ex.: Sigstore/cosign, ou GPG) para garantir integridade.

### 4. SLSA (Supply-chain Levels for Software Artifacts)
Progrida pelos níveis SLSA:
- Nível 1: build documentado e proveniência básica.
- Nível 2+: build isolado, proveniência assinada e verificável.

### 5. Provenance attestations
Emita atestados de proveniência no CI (ex.: GitHub `attestations`) para
comprovar como e onde o artefato foi construído.

## Frameworks e referências

| Referência | Uso |
|------------|-----|
| SLSA | Integridade de build |
| SCVS (OWASP) | Verificação de componentes |
| NIST SP 800-53 | Controles de segurança |
| ISO/IEC 42001 | Governança de IA |

## Exercício

1. Gere o SBOM deste projeto.
2. Fixe todas as versões em `requirements.txt`.
3. Configure um passo de assinatura no `ci.yml`.
4. Descreva como você detectaria um rug pull em um servidor MCP de terceiros.
