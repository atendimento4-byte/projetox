---
title: "Validacao de Loop"
description: "4 gates por iteracao com criterios de parada e rollback"
status: "novo"
---

# ValidaÃ§Ã£o de Loop

> **Checkpoints obrigatÃ³rios, validaÃ§Ã£o de contexto, detecÃ§Ã£o de anomalias e critÃ©rios de parada para todos os loops do sistema.**

---

## 1. Ciclo de ValidaÃ§Ã£o

Cada iteraÃ§Ã£o de um loop passa por 4 fases de validaÃ§Ã£o:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                 ITERAÃ‡ÃƒO DO LOOP                      â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚   Gate   â”‚  Gate    â”‚  Gate    â”‚      Gate            â”‚
â”‚ PrÃ©-     â”‚  PÃ³s-    â”‚  PÃ³s-    â”‚     PÃ³s-             â”‚
â”‚ ExecuÃ§Ã£o â”‚ LLM      â”‚ Ferram.  â”‚     AÃ§Ã£o             â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Contexto â”‚ Schema   â”‚ Status   â”‚ Objetivo mantido?    â”‚
â”‚ vÃ¡lido?  â”‚ vÃ¡lido?  â”‚ cÃ³digo?  â”‚ Contexto consistente?â”‚
â”‚ Limites  â”‚ DÃ©jÃ  vu? â”‚ Log ok?  â”‚ PrÃ³ximo passo?       â”‚
â”‚ ok?      â”‚          â”‚          â”‚                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. Gate 1 â€” PrÃ©-ExecuÃ§Ã£o

Antes de cada aÃ§Ã£o do loop, validar:

| VerificaÃ§Ã£o | DescriÃ§Ã£o |
|-------------|-----------|
| Contexto vÃ¡lido | Estado da sessÃ£o Ã© consistente |
| Limites ok | Nenhum limite foi excedido |
| Objetivo vÃ¡lido | Objetivo original permanece relevante |
| Agente autorizado | Agente tem permissÃ£o para a aÃ§Ã£o |
| Sem conflito | Nenhum outro loop estÃ¡ executando aÃ§Ã£o conflitante |

**Se falhar:** Abortar iteraÃ§Ã£o. Logar motivo. Se for limite ou conflito, notificar usuÃ¡rio.

---

## 3. Gate 2 â€” PÃ³s-LLM

ApÃ³s cada chamada ao LLM, validar:

| VerificaÃ§Ã£o | DescriÃ§Ã£o |
|-------------|-----------|
| Schema vÃ¡lido | Resposta segue o schema esperado (Pydantic) |
| DÃ©jÃ  vu | Resposta Ã© idÃªntica Ã  anterior? (possÃ­vel loop) |
| ConfianÃ§a | Score de confianÃ§a acima do limiar (se disponÃ­vel) |
| ConteÃºdo vÃ¡lido | Campos preenchidos, sem placeholders vazios |
| AlucinaÃ§Ã£o | Resposta contradiz contexto conhecido |

**CritÃ©rio de dÃ©jÃ  vu:** Se 3 respostas consecutivas sÃ£o idÃªnticas â†’ loop infinito detectado.

**Se falhar schema:** Re-prompt com instruÃ§Ã£o mais explÃ­cita (mÃ¡ximo 3x).
**Se falhar dÃ©jÃ  vu:** Abortar loop.

---

## 4. Gate 3 â€” PÃ³s-Ferramenta

ApÃ³s cada uso de ferramenta (API, banco, arquivo), validar:

| VerificaÃ§Ã£o | DescriÃ§Ã£o |
|-------------|-----------|
| Status cÃ³digo | HTTP 200 ou similar |
| Resposta vÃ¡lida | Dados retornados sÃ£o consistentes |
| Log registrado | AÃ§Ã£o foi registrada no log de auditoria |
| Side effect | Efeito colateral esperado ocorreu |

**Se falhar:** Seguir recuperaÃ§Ã£o conforme [[07-Testes/Cenarios-Falha.md|CenÃ¡rios de Falha]].

---

## 5. Gate 4 â€” PÃ³s-AÃ§Ã£o

ApÃ³s cada aÃ§Ã£o executada, validar:

| VerificaÃ§Ã£o | DescriÃ§Ã£o |
|-------------|-----------|
| Objetivo mantido | AÃ§Ã£o contribuiu para o objetivo? |
| Contexto consistente | Estado do sistema nÃ£o divergiu |
| PrÃ³ximo passo existe | Loop tem uma prÃ³xima etapa vÃ¡lida |
| Checkpoint salvo | Estado atual foi persistido |
| MÃ©tricas emitidas | MÃ©tricas da iteraÃ§Ã£o foram registradas |

**Se falhar:** Reavaliar plano. Se objetivo nÃ£o for mais atingÃ­vel, abortar.

---

## 6. CritÃ©rios de Parada

### 6.1 â€” Parada Normal

| CritÃ©rio | DescriÃ§Ã£o |
|----------|-----------|
| Objetivo alcanÃ§ado | Resultado desejado foi produzido |
| Aprovado pelo usuÃ¡rio | UsuÃ¡rio confirmou o resultado |
| Sem prÃ³ximos passos | Loop chegou ao fim natural do fluxo |

### 6.2 â€” Parada por Erro

| CritÃ©rio | DescriÃ§Ã£o |
|----------|-----------|
| Erro crÃ­tico | Falha irrecuperÃ¡vel detectada |
| Limite excedido | Algum limite de execuÃ§Ã£o foi atingido |
| Loop infinito detectado | DÃ©jÃ  vu ou iteraÃ§Ãµes mÃ¡ximas |
| ValidaÃ§Ã£o falhou | Contexto inconsistente ou resposta invÃ¡lida |
| Ferramenta crÃ­tica indisponÃ­vel | DependÃªncia essencial nÃ£o responde |

### 6.3 â€” Parada por IntervenÃ§Ã£o

| CritÃ©rio | DescriÃ§Ã£o |
|----------|-----------|
| UsuÃ¡rio cancelou | Ctrl+C, comando cancelar |
| UsuÃ¡rio rejeitou | AÃ§Ã£o necessÃ¡ria rejeitada |
| AprovaÃ§Ã£o necessÃ¡ria | Gate que exige humano nÃ£o foi aprovado |
| Risco detectado | AnÃ¡lise de risco identificou perigo |

---

## 7. Checkpoints

A cada iteraÃ§Ã£o do loop, um checkpoint Ã© salvo contendo:

```json
{
  "id_execucao": "exec_001",
  "iteracao": 5,
  "timestamp": "2026-07-02T10:30:00Z",
  "estado": {
    "contexto": { "sessao_id": "sess_001", "etapa": "transcricao" },
    "agente": "A01",
    "ferramentas_usadas": ["whisper", "llm"],
    "resultados_parciais": {"transcricao": "..."}
  },
  "limites": {
    "iteracoes_restantes": 5,
    "tempo_gasto_segundos": 12
  }
}
```

**Rollback:** Ã‰ possÃ­vel restaurar qualquer checkpoint anterior se necessÃ¡rio.

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

