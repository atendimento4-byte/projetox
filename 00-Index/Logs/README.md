---
title: "Logs de Sessão"
description: "Registro e handover das sessões de trabalho do Hermes"
---

# Logs de Sessão

> Ponto de partida para toda sessão do Hermes. Ao iniciar, leia o log mais recente para retomar de onde parou.

---

## Protocolo de Handover

### Ao Finalizar

1. Criar `sessao-YYYY-MM-DD.md` com o template abaixo
2. Atualizar a última task em `06-Planejamento/Tasks/`
3. Salvar: última task, próximo passo, pendências, decisões

### Ao Iniciar

1. **Ler o log mais recente** (pelo nome do arquivo, ordem decrescente)
2. Verificar tasks abertas em `06-Planejamento/Tasks/`
3. Revisar `00-Index/Decisoes-Pendentes.md`
4. Retomar do último próximo passo

---

## Template de Log de Sessão

```markdown
---
date: YYYY-MM-DD
status: encerrada
ultima_task: TASK-NNN
proximo_passo: "..."
---

# Sessão YYYY-MM-DD

## O que foi feito
- ...

## O que foi decidido
- ...

## Handover

### Estado Salvo
- Última task: TASK-NNN
- Status: aberta | revisao | concluida
- Próximo passo: ...
- Bloqueios: ...

### Pendências
- ...

### Decisões da Sessão
- ...

### Contexto para Retomada
- O que foi entendido até agora?
- O que o próximo executor precisa saber?
```

---

## Últimas Sessões

*Nenhuma sessão registrada ainda.*

---

> Ver protocolo completo em [[00-Index/HERMES.md#8-handover-entre-sessões]]
