---
title: "Estrategia de Rollback"
description: "4 niveis de rollback com mecanismo de compensacao"
status: "novo"
---

# EstratÃ©gia de Rollback

> **PolÃ­tica, procedimentos e mecanismos para reverter aÃ§Ãµes executadas por loops em caso de falha, erro ou intervenÃ§Ã£o.**

---

## 1. Filosofia

- Toda aÃ§Ã£o externa (chamada de API, criaÃ§Ã£o de arquivo, envio de e-mail) Ã© **potencialmente reversÃ­vel**.
- AÃ§Ãµes sÃ£o executadas em **transaÃ§Ãµes lÃ³gicas** â€” se uma falha, as anteriores sÃ£o revertidas.
- Rollback automÃ¡tico para falhas de infraestrutura. Rollback manual (com aprovaÃ§Ã£o) para erros de domÃ­nio.

---

## 2. NÃ­veis de Rollback

| NÃ­vel | DescriÃ§Ã£o | Gatilho |
|-------|-----------|---------|
| **N1 â€” Etapa** | Reverte a Ãºltima aÃ§Ã£o do agente | Falha de validaÃ§Ã£o pÃ³s-aÃ§Ã£o |
| **N2 â€” IteraÃ§Ã£o** | Reverte todas as aÃ§Ãµes da iteraÃ§Ã£o atual | Erro crÃ­tico na iteraÃ§Ã£o |
| **N3 â€” Loop** | Reverte todas as aÃ§Ãµes do loop | Falha fatal, cancelamento |
| **N4 â€” SessÃ£o** | Reverte todas as aÃ§Ãµes da sessÃ£o | Erro irrecuperÃ¡vel |

---

## 3. Mecanismo de Rollback

Cada aÃ§Ã£o executada registra informaÃ§Ãµes de reversÃ£o:

```json
{
  "id_acao": "act_001",
  "tipo": "movidesk.atualizar_chamado",
  "comando_reversao": {
    "metodo": "movidesk.atualizar_chamado",
    "params": {"id": "CH-001", "dados": {"status": "estado_anterior"}}
  },
  "compensacao": "chamada_api",
  "timestamp": "2026-07-02T10:30:00Z"
}
```

**Tipos de compensaÃ§Ã£o:**

| AÃ§Ã£o | CompensaÃ§Ã£o |
|------|-------------|
| Criar nota Obsidian | Deletar nota criada |
| Atualizar chamado Movidesk | Reverter para estado anterior |
| Enviar e-mail | Enviar e-mail de retrataÃ§Ã£o (manual) |
| Salvar no banco | Deletar registro ou reverter transaÃ§Ã£o |
| Iniciar gravaÃ§Ã£o | Deletar arquivo de Ã¡udio |

---

## 4. Quando Acionar Rollback

| SituaÃ§Ã£o | NÃ­vel | AutomÃ¡tico |
|----------|:-----:|:----------:|
| Falha de validaÃ§Ã£o pÃ³s-LLM | N1 | âœ… |
| Erro de persistÃªncia | N2 | âœ… |
| Timeout de serviÃ§o externo | N2 | âœ… |
| Loop infinito detectado | N3 | âœ… |
| UsuÃ¡rio cancelou execuÃ§Ã£o | N3 | âœ… |
| Contexto corrompido | N4 | âŒ (notificar) |
| AÃ§Ã£o executada com dados errados | N3 | âŒ (aprovaÃ§Ã£o) |
| E-mail enviado incorretamente | N3 | âŒ (manual) |

---

## 5. Procedimento de Rollback

```
1. Detectar falha
2. Identificar nÃ­vel de rollback (N1-N4)
3. Coletar comandos de reversÃ£o das aÃ§Ãµes no escopo
4. Executar comandos de reversÃ£o em ordem inversa
5. Verificar sucesso de cada reversÃ£o
6. Se reversÃ£o falhar, escalar para N+1
7. Registrar rollback no log de auditoria
8. Notificar usuÃ¡rio com resumo do rollback
```

---

## 6. Log de Rollback

Cada rollback gera um registro completo:

```json
{
  "id_rollback": "rb_001",
  "id_execucao": "exec_001",
  "nivel": "N2",
  "motivo": "Erro de persistÃªncia - Postgres indisponÃ­vel",
  "acoes_revertidas": [
    {"id": "act_001", "tipo": "criar_nota", "revertida": true},
    {"id": "act_002", "tipo": "atualizar_chamado", "revertida": true}
  ],
  "acoes_nao_revertidas": [],
  "estado_final": "sessao_001_estado_anterior",
  "timestamp": "2026-07-02T10:30:05Z"
}
```

---

## 7. LimitaÃ§Ãµes

| AÃ§Ã£o | ReversÃ­vel? | Nota |
|------|:-----------:|------|
| E-mail enviado | Parcial | Enviar e-mail de errata, nÃ£o "desenvia" |
| API externa (POST) | Depende | Se API suportar reversÃ£o |
| Webhook | NÃ£o | Registrar e notificar |
| Arquivo deletado | Parcial | Se houver backup |
| Nota do Obsidian | Sim | Deletar nota criada |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

