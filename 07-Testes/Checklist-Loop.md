---
title: "Checklist de Loop"
description: "10 secoes de verificacao: riscos, cenario, gates, agentes"
status: "novo"
---

# Checklist de ValidaÃ§Ã£o de Loop

> **Checklist final que todo loop deve satisfazer antes de ser considerado "pronto". Nenhum loop pode ser implementado enquanto nÃ£o existir documentaÃ§Ã£o comprovando todos os itens abaixo.**

---

## 1. Check â€” Riscos

- [ ] Todos os riscos do loop foram identificados e documentados
- [ ] Riscos tÃªm probabilidade e impacto estimados
- [ ] MitigaÃ§Ãµes para cada risco foram definidas
- [ ] Riscos aceitos tÃªm aprovaÃ§Ã£o explÃ­cita

---

## 2. Check â€” CenÃ¡rios

- [ ] CenÃ¡rio de sucesso documentado
- [ ] CenÃ¡rios de falha documentados (mÃ­nimo: LLM erro, timeout, ferramenta off, API off, interrupÃ§Ã£o)
- [ ] CenÃ¡rio de loop infinito documentado
- [ ] CenÃ¡rio de dependÃªncia circular documentado (se aplicÃ¡vel)
- [ ] Cada cenÃ¡rio tem: causa, detecÃ§Ã£o, recuperaÃ§Ã£o, log

---

## 3. Check â€” Limites

- [ ] NÃºmero mÃ¡ximo de iteraÃ§Ãµes definido
- [ ] Tempo mÃ¡ximo de execuÃ§Ã£o definido
- [ ] NÃºmero mÃ¡ximo de chamadas LLM definido
- [ ] Limite de custo definido
- [ ] Limite de memÃ³ria definido
- [ ] Limite de tokens definido
- [ ] AÃ§Ã£o ao atingir cada limite documentada

---

## 4. Check â€” CritÃ©rios de Parada

- [ ] CritÃ©rios de parada normal (objetivo alcanÃ§ado, sem prÃ³ximos passos)
- [ ] CritÃ©rios de parada por erro (limite excedido, erro crÃ­tico, loop infinito)
- [ ] CritÃ©rios de parada por intervenÃ§Ã£o (cancelamento, rejeiÃ§Ã£o, risco)
- [ ] CondiÃ§Ã£o de parada Ã© verificada a cada iteraÃ§Ã£o

---

## 5. Check â€” Testes

- [ ] Testes unitÃ¡rios documentados
- [ ] Testes de fluxo documentados
- [ ] Testes de integraÃ§Ã£o documentados
- [ ] Testes de recuperaÃ§Ã£o documentados
- [ ] Testes de seguranÃ§a documentados
- [ ] Testes de observabilidade documentados
- [ ] Testes de performance documentados
- [ ] Testes humanos documentados (se aplicÃ¡vel)
- [ ] Cada teste tem: ID, objetivo, prÃ©-condiÃ§Ãµes, entradas, resultado esperado, prioridade

---

## 6. Check â€” Quality Gates

- [ ] Gate 1 â€” Requisitos validados
- [ ] Gate 2 â€” Planejamento validado
- [ ] Gate 3 â€” Contexto validado (automÃ¡tico)
- [ ] Gate 4 â€” DocumentaÃ§Ã£o validada
- [ ] Gate 5 â€” SimulaÃ§Ã£o aprovada
- [ ] Gate 6 â€” Resultados validados
- [ ] Gate 7 â€” AprovaÃ§Ã£o humana concedida

---

## 7. Check â€” Agentes

- [ ] Objetivo do agente documentado
- [ ] Entradas esperadas documentadas
- [ ] SaÃ­das esperadas documentadas
- [ ] Responsabilidades documentadas
- [ ] RestriÃ§Ãµes documentadas
- [ ] Casos de sucesso documentados
- [ ] Casos de falha documentados
- [ ] CritÃ©rios de aprovaÃ§Ã£o do agente documentados

---

## 8. Check â€” Auditoria

- [ ] ID Ãºnico de execuÃ§Ã£o gerado
- [ ] Objetivo registrado
- [ ] Entradas registradas
- [ ] SaÃ­das registradas
- [ ] Ferramentas utilizadas registradas
- [ ] Agentes envolvidos registrados
- [ ] DecisÃµes tomadas registradas
- [ ] Tempo total registrado
- [ ] Falhas registradas
- [ ] IntervenÃ§Ãµes humanas registradas
- [ ] Resultado final registrado

---

## 9. Check â€” Observabilidade

- [ ] Logs estruturados emitidos
- [ ] Correlation ID propagado em toda a cadeia
- [ ] MÃ©tricas obrigatÃ³rias emitidas
- [ ] Alertas configurados para limiares crÃ­ticos
- [ ] Checkpoints salvos a cada iteraÃ§Ã£o
- [ ] Log de rollback disponÃ­vel

---

## 10. Check â€” AprovaÃ§Ã£o Final

- [ ] DocumentaÃ§Ã£o completa revisada
- [ ] Testes em sandbox passaram
- [ ] Riscos aceitÃ¡veis
- [ ] Limites configurados
- [ ] UsuÃ¡rio aprovou explicitamente

**Loop pode ser implementado?** [ ] Sim  [ ] NÃ£o

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

