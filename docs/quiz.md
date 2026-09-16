# 📝 Quiz de Autoavaliação — MCP Security

⚠️ Material educacional. Responda antes de olhar o gabarito no fim.

---

## Parte 1 — Múltipla escolha

**1.** Qual mitigação evita path traversal na leitura de arquivos?
- a) Aumentar o tamanho do buffer
- b) Resolver o caminho com `.resolve()` e confinar a um diretório base
- c) Usar `shell=True`
- d) Confiar na entrada do usuário

**2.** Por que `shell=False` + `shlex.split` ajuda contra command injection?
- a) Deixa o comando mais rápido
- b) Evita que o shell interprete metacaracteres como `;` e `|`
- c) Criptografa o comando
- d) Não tem efeito de segurança

**3.** O que caracteriza um ataque de "tool poisoning"?
- a) Sobrecarregar o servidor com requisições
- b) Injetar instruções ocultas na descrição de uma tool
- c) Roubar a senha do banco
- d) Desligar o servidor

**4.** Em RBAC, o que a allowlist por papel controla?
- a) A velocidade da rede
- b) Quais tools cada papel pode chamar
- c) O tamanho do log
- d) A versão do Python

**5.** O que é um "rug pull" no contexto de tools MCP?
- a) Uma tool que sempre falha
- b) Uma tool que muda de comportamento após ganhar confiança
- c) Um erro de digitação
- d) Um tipo de criptografia

**6.** Qual prática ajuda contra segredos hardcoded?
- a) Escrever a chave em um comentário
- b) Ler o segredo de variável de ambiente (`os.getenv`)
- c) Commitar o `.env` no git
- d) Usar a mesma senha em tudo

---

## Parte 2 — Verdadeiro ou Falso

**7.** ( ) Comparação de assinaturas HMAC deve usar comparação em tempo constante.

**8.** ( ) É seguro expor um endpoint `prompt/get` com instruções para ignorar políticas.

**9.** ( ) IDOR ocorre quando um usuário acessa dados de outro sem verificação de identidade.

**10.** ( ) Fixar versões de dependências reduz o risco de typosquatting.

---

## Parte 3 — Dissertativa

**11.** Explique, com suas palavras, por que remover o comentário HTML inteiro é
mais robusto do que apagar apenas a palavra "IGNORE" na sanitização de descrições.

**12.** Aponte uma trust boundary do MCP e descreva um ataque possível ali e a defesa.

---

## ✅ Gabarito

| Q | Resposta |
|---|----------|
| 1 | b |
| 2 | b |
| 3 | b |
| 4 | b |
| 5 | b |
| 6 | b |
| 7 | Verdadeiro (evita timing attack) |
| 8 | Falso (é a vuln #9) |
| 9 | Verdadeiro |
| 10 | Verdadeiro |

**11.** Apagar só "IGNORE" deixa o resto do texto malicioso legível pelo modelo,
que ainda pode ser induzido. Remover o bloco `<!-- ... -->` inteiro (e truncar em
gatilhos) elimina o payload por completo, não apenas uma palavra-chave.

**12.** Exemplos aceitáveis:
- Boundary Cliente↔Servidor: ataque = chamada sem autenticação; defesa = token HMAC obrigatório (#4).
- Boundary Servidor↔Recursos: ataque = path traversal / command injection; defesa = `_safe_path` (#2) e `shlex`+`shell=False`+allowlist (#3).
- Boundary Host/LLM↔Cliente: ataque = prompt injection / tool poisoning; defesa = sanitização de descrições (#6) e não expor prompts inseguros (#9).
