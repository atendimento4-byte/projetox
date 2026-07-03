---
title: "Estrategia de Testes"
description: "Piramide de testes, 10 categorias, modos de execucao"
status: "novo"
---

# EstratÃ©gia de Testes

> **Filosofia, categorias, ferramentas e responsabilidades para a validaÃ§Ã£o de todos os loops do sistema.**

---

## 1. Filosofia

- **Test-first:** Nenhum loop Ã© implementado sem antes ter seu plano de testes documentado.
- **SimulaÃ§Ã£o primeiro:** Todo loop funciona primeiro em ambiente simulado. Somente apÃ³s aprovaÃ§Ã£o executa aÃ§Ãµes reais.
- **Nenhuma aÃ§Ã£o externa durante testes:** Todos os serviÃ§os externos (Movidesk, Whisper, LLM, SMTP) sÃ£o mockados.
- **AuditÃ¡vel por padrÃ£o:** Toda execuÃ§Ã£o de teste gera logs, mÃ©tricas e trilha de auditoria.
- **ReproduzÃ­vel:** Mesmo cenÃ¡rio, mesmo mock, mesmo resultado â€” independente de ordem ou ambiente.

---

## 2. PirÃ¢mide de Testes

```
        â•±â•²
       â•± E2E â•²               ~5% â€” fluxo completo com mocks
      â•±â”€â”€â”€â”€â”€â”€â”€â”€â•²
     â•±  Fluxo    â•²           ~15% â€” cada etapa do loop
    â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
   â•±  IntegraÃ§Ã£o    â•²        ~20% â€” comunicaÃ§Ã£o entre agentes
  â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
 â•±   UnitÃ¡rios           â•²    ~30% â€” funÃ§Ãµes, validaÃ§Ãµes, parsing
â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
â•±  SimulaÃ§Ã£o (modo sandbox) â•² ~30% â€” loop completo em ambiente controlado
â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
```

---

## 3. Categorias de Testes

### 3.1 â€” Testes UnitÃ¡rios
**O que validam:** FunÃ§Ãµes puras, validaÃ§Ã£o de entrada/saÃ­da, parsing de LLM, formataÃ§Ã£o.
**Ferramenta:** pytest
**Mock:** Nenhum (funÃ§Ãµes sem dependÃªncia externa)
**Cobertura:** 95% no domÃ­nio

### 3.2 â€” Testes de Fluxo
**O que validam:** Cada etapa de um loop â€” entrada â†’ processamento â†’ saÃ­da â†’ prÃ³xima etapa.
**Ferramenta:** pytest + pytest-asyncio
**Mock:** DependÃªncias diretas do agente
**Cobertura:** 90% dos fluxos alternativos

### 3.3 â€” Testes de IntegraÃ§Ã£o
**O que validam:** ComunicaÃ§Ã£o entre agentes, troca de mensagens via Event Bus, IPC CLI â†” Daemon.
**Ferramenta:** pytest + docker (serviÃ§os reais: Postgres, Redis)
**Mock:** ServiÃ§os externos (Movidesk, Whisper, LLM)
**Cobertura:** 80% das interfaces

### 3.4 â€” Testes de RegressÃ£o
**O que validam:** AlteraÃ§Ãµes nÃ£o quebram funcionalidades existentes.
**Ferramenta:** pytest + snapshot testing
**Trigger:** A cada push para main

### 3.5 â€” Testes de RecuperaÃ§Ã£o
**O que validam:** Comportamento do sistema apÃ³s falhas (LLM timeout, API off, arquivo corrompido).
**Ferramenta:** CenÃ¡rios prÃ©-programados nos mocks
**CritÃ©rio:** Sistema retorna estado consistente

### 3.6 â€” Testes de SeguranÃ§a
**O que validam:** PermissÃµes corretas, acesso indevido negado, dados nÃ£o vazam em logs.
**Ferramenta:** Testes especÃ­ficos + revisÃ£o de cÃ³digo
**CritÃ©rio:** Zero aÃ§Ãµes externas sem aprovaÃ§Ã£o explÃ­cita

### 3.7 â€” Testes de Observabilidade
**O que validam:** Logs gerados, estrutura JSON, correlation_id propagado, mÃ©tricas emitidas.
**Ferramenta:** Captura de logs em testes + assertions

### 3.8 â€” Testes de Performance
**O que validam:** Tempo de execuÃ§Ã£o por loop, consumo de memÃ³ria, chamadas LLM, latÃªncia.
**Ferramenta:** pytest-benchmark
**CritÃ©rio:** Cada loop deve completar em < 30s

### 3.9 â€” Testes de Escalabilidade
**O que validam:** MÃºltiplos loops simultÃ¢neos, mÃºltiplos agentes, fila de tarefas.
**Ferramenta:** Testes com concorrÃªncia controlada

### 3.10 â€” Testes Humanos
**O que validam:** Checklist de validaÃ§Ã£o manual para cenÃ¡rios que exigem julgamento humano.
**Formato:** Script de teste manual + planilha de resultados

---

## 4. Modos de ExecuÃ§Ã£o

| Modo | AÃ§Ãµes Reais | Mocks | AprovaÃ§Ã£o | Uso |
|------|:-----------:|:-----:|:---------:|-----|
| **Dry Run** | âŒ | Sim | âŒ | ValidaÃ§Ã£o de sintaxe e fluxo |
| **Sandbox** | âŒ | Sim | âŒ | Teste completo de lÃ³gica |
| **SimulaÃ§Ã£o** | âŒ | Parcial | âŒ | Teste com dados sintÃ©ticos |
| **ProduÃ§Ã£o** | âœ… | NÃ£o | âœ… | Uso real (apÃ³s aprovaÃ§Ã£o em simulaÃ§Ã£o) |

> Ver [[07-Testes/Simulacao.md|SimulaÃ§Ã£o]] para detalhes de cada modo.

---

## 5. Ferramentas

| Ferramenta | FunÃ§Ã£o |
|-----------|--------|
| pytest | Framework de testes principal |
| pytest-asyncio | Testes assÃ­ncronos |
| pytest-cov | RelatÃ³rio de cobertura |
| pytest-benchmark | Testes de performance |
| factory-boy | Factories para dados de teste |
| docker | ServiÃ§os reais em testes de integraÃ§Ã£o |
| structlog | Captura de logs em testes |
| httpx-mock | Mock de chamadas HTTP |

---

## 6. Responsabilidades

| Papel | Responsabilidade |
|-------|-----------------|
| **Arquiteto** | Define estratÃ©gia, aprova planos, garante consistÃªncia |
| **Implementador** | Cria testes conforme o plano, mantÃ©m mocks atualizados |
| **Revisor** | Verifica cobertura, qualidade e aderÃªncia Ã  estratÃ©gia |
| **UsuÃ¡rio (Supervisor)** | Executa testes humanos, valida resultados, aprova gates |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

