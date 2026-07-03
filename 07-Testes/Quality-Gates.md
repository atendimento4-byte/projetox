---
title: "Quality Gates"
description: "7 gates obrigatorios: requisitos ao aceite humano"
status: "novo"
---

# Quality Gates

> **Gates obrigatÃ³rios que todo loop deve atravessar antes, durante e depois da execuÃ§Ã£o. Nenhum gate pode ser ignorado.**

---

## 1. VisÃ£o Geral

```
Gate 1 â”€â”€â”€â”€ Gate 2 â”€â”€â”€â”€ Gate 3 â”€â”€â”€â”€ Gate 4 â”€â”€â”€â”€ Gate 5 â”€â”€â”€â”€ Gate 6 â”€â”€â”€â”€ Gate 7
Requisitos  Planej.     Contexto    Doc.        SimulaÃ§Ã£o   Resultados  Humano
```

---

## 2. Gate 1 â€” ValidaÃ§Ã£o dos Requisitos

**Quando:** Antes de projetar o loop.
**Quem:** Arquiteto.
**O que valida:**

- [ ] Requisito funcional existe e estÃ¡ documentado ([[02-Requisitos/Requisitos-Funcionais.md|RF]])
- [ ] Caso de uso relacionado existe ([[02-Requisitos/Casos-de-Uso.md|UC]])
- [ ] CritÃ©rios de aceitaÃ§Ã£o definidos
- [ ] Origem do requisito conhecida
- [ ] Prioridade atribuÃ­da

**AprovaÃ§Ã£o:** Arquiteto assina que o requisito Ã© vÃ¡lido.

---

## 3. Gate 2 â€” ValidaÃ§Ã£o do Planejamento

**Quando:** Antes de iniciar a implementaÃ§Ã£o do loop.
**Quem:** Arquiteto.
**O que valida:**

- [ ] Plano de testes documentado ([[07-Testes/Plano-Testes.md|Plano de Testes]])
- [ ] Limites de execuÃ§Ã£o definidos ([[07-Testes/Limites-Execucao.md|Limites]])
- [ ] CenÃ¡rios de falha mapeados ([[07-Testes/Cenarios-Falha.md|CenÃ¡rios]])
- [ ] Mocks identificados e disponÃ­veis ([[07-Testes/Servicos-Mock.md|Mocks]])
- [ ] Dados de teste definidos ([[07-Testes/Dados-Teste.md|Dados]])
- [ ] EsforÃ§o estimado

**AprovaÃ§Ã£o:** Arquiteto assina que o plano Ã© completo.

---

## 4. Gate 3 â€” ValidaÃ§Ã£o do Contexto

**Quando:** Antes de cada execuÃ§Ã£o do loop.
**Quem:** Sistema (automÃ¡tico).
**O que valida:**

- [ ] Contexto da sessÃ£o Ã© consistente
- [ ] Dados de entrada sÃ£o vÃ¡lidos
- [ ] ServiÃ§os necessÃ¡rios estÃ£o disponÃ­veis
- [ ] UsuÃ¡rio estÃ¡ autenticado
- [ ] Limites de recurso nÃ£o foram excedidos

**AprovaÃ§Ã£o:** AutomÃ¡tica via validaÃ§Ã£o de schema + health check.

---

## 5. Gate 4 â€” ValidaÃ§Ã£o da DocumentaÃ§Ã£o

**Quando:** Antes de aprovar o loop para simulaÃ§Ã£o.
**Quem:** Arquiteto + Revisor.
**O que valida:**

- [ ] Fluxo do loop documentado
- [ ] DecisÃµes de design registradas em ADR
- [ ] Interfaces definidas (Ports)
- [ ] Testes documentados
- [ ] Riscos identificados e mitigados

**AprovaÃ§Ã£o:** Revisor assina documentaÃ§Ã£o completa.

---

## 6. Gate 5 â€” ValidaÃ§Ã£o da ExecuÃ§Ã£o Simulada

**Quando:** ApÃ³s testes em sandbox.
**Quem:** Sistema (automÃ¡tico) + Arquiteto.
**O que valida:**

- [ ] Modo sandbox passou ([[07-Testes/Simulacao.md|Sandbox]])
- [ ] Todos os cenÃ¡rios de falha cobertos
- [ ] MÃ©tricas dentro dos limites
- [ ] Logs de auditoria completos
- [ ] Nenhum efeito colateral nÃ£o intencional

**AprovaÃ§Ã£o:** RelatÃ³rio de simulaÃ§Ã£o aprovado pelo arquiteto.

---

## 7. Gate 6 â€” ValidaÃ§Ã£o dos Resultados

**Quando:** Antes de liberar para produÃ§Ã£o.
**Quem:** Arquiteto.
**O que valida:**

- [ ] Resultados correspondem aos critÃ©rios de aceitaÃ§Ã£o
- [ ] Performance dentro do esperado
- [ ] Cobertura de testes >= 80%
- [ ] Nenhum cenÃ¡rio de falha crÃ­tico sem cobertura
- [ ] MÃ©tricas de qualidade aceitÃ¡veis

**AprovaÃ§Ã£o:** Pipeline de CI/CD aprovado + arquiteto.

---

## 8. Gate 7 â€” AprovaÃ§Ã£o Humana

**Quando:** Antes da primeira execuÃ§Ã£o em produÃ§Ã£o.
**Quem:** UsuÃ¡rio (Supervisor).
**O que valida:**

- [ ] Funcionalidade faz sentido no dia a dia
- [ ] Fluxo estÃ¡ claro
- [ ] Riscos sÃ£o aceitÃ¡veis
- [ ] Comportamento em caso de erro Ã© aceitÃ¡vel
- [ ] Limites de custo estÃ£o configurados

**AprovaÃ§Ã£o:** UsuÃ¡rio executa e aprova o comando.

---

## 9. Resumo

| Gate | O quÃª | Quem | AutomÃ¡tico |
|:----:|-------|:----:|:----------:|
| G1 | Requisitos | Arquiteto | âŒ |
| G2 | Planejamento | Arquiteto | âŒ |
| G3 | Contexto | Sistema | âœ… |
| G4 | DocumentaÃ§Ã£o | Revisor | âŒ |
| G5 | SimulaÃ§Ã£o | Arquiteto | Parcial |
| G6 | Resultados | Arquiteto | Parcial |
| G7 | AprovaÃ§Ã£o humana | UsuÃ¡rio | âŒ |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

