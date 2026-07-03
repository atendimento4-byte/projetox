---
title: "Servicos Mock"
description: "Mocks para Movidesk, Whisper, LLM, SMTP, Obsidian, Qdrant"
status: "novo"
---

# ServiÃ§os Mock

> **DefiniÃ§Ã£o de todos os mocks de serviÃ§os externos e internos utilizados nos testes.**

---

## 1. Filosofia

- Todo serviÃ§o externo possui um mock correspondente.
- Mocks implementam a mesma interface (Port) que o serviÃ§o real.
- Mocks permitem configurar comportamento (sucesso, falha, timeout, erro).
- Mocks registram todas as chamadas recebidas para auditoria.
- Nenhum teste de loop pode depender de serviÃ§o externo real.

---

## 2. Mock â€” Movidesk API

**Interface:** `contexto/integracao/dominio/repositorios/repositorio_movidesk.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `consultar_chamado(id)` | Retorna chamado fictÃ­cio | Timeout ou 404 |
| `atualizar_chamado(id, dados)` | Retorna sucesso | Erro de autenticaÃ§Ã£o |
| `listar_chamados(filtro)` | Retorna lista paginada | Rate limit excedido |

**Dados mockados:**
```python
CHAMADO_PADRAO = {
    "id": "CH-001",
    "cliente": "Empresa ABC Ltda",
    "status": "Em andamento",
    "data_abertura": "2026-07-02T10:00:00Z",
    "descricao": "Roteador caindo intermitentemente"
}
```

**CenÃ¡rios de erro prÃ©-configurados:**
- `MOVIDESK_TIMEOUT` â€” servidor nÃ£o responde em 30s
- `MOVIDESK_401` â€” token invÃ¡lido
- `MOVIDESK_429` â€” rate limit excedido
- `MOVIDESK_500` â€” erro interno do servidor

---

## 3. Mock â€” Whisper API

**Interface:** `contexto/audio/dominio/repositorios/repositorio_transcricao.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `transcrever(audio)` | Retorna transcriÃ§Ã£o simulada | Ãudio corrompido |
| `transcrever_parcial(audio)` | Retorna texto parcial | Timeout |

**TranscriÃ§Ã£o mock padrÃ£o:**
```text
"Cliente reportou que o roteador estÃ¡ reiniciando sozinho a cada 30 minutos.
TÃ©cnico verificou cabo de rede e identificou oxidaÃ§Ã£o no conector.
Foi realizada a troca do cabo e teste de conectividade.
Problema resolvido."
```

---

## 4. Mock â€” LLM API (Anthropic/OpenAI)

**Interface:** `infra/llm/cliente.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `gerar(prompt, schema)` | Retorna resposta no schema | Resposta inconsistente |
| `gerar_stream(prompt)` | Retorna chunks | Timeout parcial |

**Respostas mock disponÃ­veis:**
- `RESUMO_PADRAO` â€” resumo estruturado de atendimento
- `EMAIL_COMPRA_PADRAO` â€” e-mail de solicitaÃ§Ã£o de compra
- `EMAIL_COMUNICADO_PADRAO` â€” e-mail de comunicado
- `ENTIDADES_PADRAO` â€” extraÃ§Ã£o de entidades (cliente, equipamento)
- `SUGESTAO_SOLUCAO_PADRAO` â€” sugestÃ£o de soluÃ§Ã£o baseada em histÃ³rico

---

## 5. Mock â€” SMTP (E-mail)

**Interface:** `contexto/comunicacao/dominio/repositorios/repositorio_email.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `enviar(email)` | Simula envio, registra em log | Servidor SMTP off |
| `enviar_com_anexo(email, anexo)` | Simula envio com anexo | Anexo muito grande |

**VerificaÃ§Ã£o:** Mock captura todos os e-mails "enviados" em lista em memÃ³ria para assertions.

---

## 6. Mock â€” Obsidian Filesystem

**Interface:** `contexto/memoria/dominio/repositorios/repositorio_obsidian.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `criar_nota(caminho, conteudo)` | Cria arquivo em diretÃ³rio temp | PermissÃ£o negada |
| `ler_nota(caminho)` | Retorna conteÃºdo | Arquivo inexistente |
| `atualizar_nota(caminho, conteudo)` | Atualiza arquivo | ConteÃºdo invÃ¡lido |
| `listar_notas(pasta)` | Retorna lista de arquivos | Erro de leitura |

---

## 7. Mock â€” Qdrant (Banco Vetorial)

**Interface:** `contexto/memoria/dominio/repositorios/repositorio_vetorial.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `inserir(collection, pontos)` | Insere em coleÃ§Ã£o em memÃ³ria | Erro de schema |
| `buscar(collection, query, k)` | Retorna k resultados simulados | ColeÃ§Ã£o inexistente |
| `deletar(collection, ids)` | Remove pontos | Timeout |

---

## 8. Mock â€” Named Pipe (IPC)

**Interface:** `infra/cli/cliente_ipc.py`

| OperaÃ§Ã£o | Comportamento PadrÃ£o | Falha ConfigurÃ¡vel |
|----------|:--------------------:|:------------------:|
| `enviar_comando(metodo, params)` | Retorna resposta mock | Pipe desconectado |
| `conectar()` | Conecta ao mock | Daemon nÃ£o disponÃ­vel |

---

## 9. Registro de Chamadas

Todos os mocks mantÃªm um **registro de chamadas** em memÃ³ria:

```json
{
  "servico": "movidesk",
  "operacao": "consultar_chamado",
  "params": {"id": "CH-001"},
  "timestamp": "2026-07-02T10:00:00.000Z",
  "duracao_ms": 45,
  "erro": null
}
```

Este registro Ã© exposto para assertions nos testes.

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

