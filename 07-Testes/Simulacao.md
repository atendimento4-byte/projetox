---
title: "Simulacao"
description: "4 modos: Dry Run, Sandbox, Simulacao, Producao"
status: "novo"
---

# SimulaÃ§Ã£o

> **Modos de execuÃ§Ã£o, ambientes controlados e transiÃ§Ãµes entre modos.**

---

## 1. VisÃ£o Geral

Todo loop do sistema deve executar primeiro em ambiente simulado antes de poder executar aÃ§Ãµes reais. Quatro modos de execuÃ§Ã£o sÃ£o definidos, com progressÃ£o controlada:

```
Dry Run  â†’  Sandbox  â†’  SimulaÃ§Ã£o  â†’  ProduÃ§Ã£o
  (validaÃ§Ã£o)  (lÃ³gica)    (dados)       (real)
```

Cada modo adiciona permissÃµes e remove restriÃ§Ãµes. Nunca se pula um modo.

---

## 2. Dry Run

**PropÃ³sito:** Validar estrutura, sintaxe e fluxo sem executar nada.

| Aspecto | Comportamento |
|---------|--------------|
| AÃ§Ãµes externas | Bloqueadas â€” nenhuma chamada Ã© feita |
| LLM | NÃ£o chamado â€” usa resposta mock prÃ©-definida |
| Banco de dados | NÃ£o acessado |
| Arquivos | NÃ£o criados/modificados |
| SaÃ­da | Log detalhado do que SERIA executado |
| DuraÃ§Ã£o | < 1s (independente da complexidade) |

**AtivaÃ§Ã£o:** `hermes <comando> --dry-run`

**CritÃ©rio de aprovaÃ§Ã£o:** Log mostra sequÃªncia esperada sem erros.

---

## 3. Sandbox

**PropÃ³sito:** Testar a lÃ³gica completa do loop em ambiente totalmente isolado.

| Aspecto | Comportamento |
|---------|--------------|
| AÃ§Ãµes externas | Mockadas â€” respostas prÃ©-programadas |
| LLM | Chamado com prompt real, mas resposta validada contra schema |
| Banco de dados | PostgreSQL + Redis + Qdrant em Docker local |
| Arquivos | DiretÃ³rio temporÃ¡rio (limpo apÃ³s teste) |
| SaÃ­da | Resultado completo + mÃ©tricas + logs |

**AtivaÃ§Ã£o:** `hermes <comando> --sandbox` ou via CI

**CritÃ©rio de aprovaÃ§Ã£o:** Resultado corresponde ao esperado na [[07-Testes/Plano-Testes.md|matriz de testes]].

---

## 4. SimulaÃ§Ã£o

**PropÃ³sito:** Executar com dados sintÃ©ticos realistas, validando comportamento de ponta a ponta.

| Aspecto | Comportamento |
|---------|--------------|
| AÃ§Ãµes externas | Mockadas â€” mas com latÃªncia simulada realista |
| LLM | Chamado real (se disponÃ­vel) ou replay de respostas gravadas |
| Banco de dados | Real (Docker) |
| Arquivos | Criados em diretÃ³rio de simulaÃ§Ã£o |
| SaÃ­da | RelatÃ³rio completo com comparaÃ§Ã£o esperado vs real |

**Dados de simulaÃ§Ã£o:** Ver [[07-Testes/Dados-Teste.md|Dados de Teste]].

**AtivaÃ§Ã£o:** `hermes <comando> --simular` ou agendado

**CritÃ©rio de aprovaÃ§Ã£o:** Todas as mÃ©tricas dentro do limite especificado em [[07-Testes/Limites-Execucao.md|Limites de ExecuÃ§Ã£o]].

---

## 5. ProduÃ§Ã£o

**PropÃ³sito:** ExecuÃ§Ã£o real com dados reais e aÃ§Ãµes reais.

**PrÃ©-requisitos:**
- âœ… Aprovado em SimulaÃ§Ã£o
- âœ… AprovaÃ§Ã£o humana explÃ­cita (Quality Gate 7)
- âœ… Logs e mÃ©tricas configurados
- âœ… Limites de execuÃ§Ã£o ativos

**Comportamento:** AÃ§Ãµes reais em serviÃ§os externos, dados reais, sem mocks.

---

## 6. Tabela Comparativa

| CaracterÃ­stica | Dry Run | Sandbox | SimulaÃ§Ã£o | ProduÃ§Ã£o |
|---------------|:-------:|:-------:|:---------:|:--------:|
| LLM chamado | âŒ | âœ… | âœ… (ou replay) | âœ… |
| Banco real | âŒ | âœ… (Docker) | âœ… (Docker) | âœ… |
| Mocks externos | Sim | Sim | Sim | NÃ£o |
| AÃ§Ãµes reais | âŒ | âŒ | âŒ | âœ… |
| AprovaÃ§Ã£o humana | âŒ | âŒ | âŒ | âœ… (Gate 7) |
| Logs | âœ… | âœ… | âœ… | âœ… |
| MÃ©tricas | âŒ | âœ… | âœ… | âœ… |
| Tempo mÃ¡ximo | 1s | 30s | 60s | ConfigurÃ¡vel |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

