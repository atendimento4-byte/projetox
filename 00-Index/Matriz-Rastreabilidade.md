---
title: "Matriz de Rastreabilidade"
description: "Rastreamento: OE a RF, RF a UC, UC a Fluxo, Risco a ADR, ADR a Arquitetura"
status: "novo"
---

# Matriz de Rastreabilidade

> **Rastreia a consistÃªncia e completude da documentaÃ§Ã£o: Objetivos â†’ Requisitos â†’ Casos de Uso â†’ Fluxos â†’ Riscos â†’ ADRs.**

---

## 1. Objetivos vs Requisitos Funcionais

| OE | RFs Relacionados |
|----|------------------|
| OE01 â€” ReduÃ§Ã£o BurocrÃ¡tica | RF-OS-001, RF-OS-002, RF-EMAIL-001 |
| OE02 â€” MemÃ³ria Persistente | RF-MEM-001, RF-MEM-002, RF-MEM-003 |
| OE03 â€” RecuperaÃ§Ã£o Inteligente | RF-IA-001, RF-IA-002, RF-CONSULTA-001 |
| OE04 â€” TransparÃªncia e Controle | RF-SEG-001, RF-SEG-002 |
| OE05 â€” TranscriÃ§Ã£o e Resumo | RF-AUDIO-001, RF-AUDIO-002, RF-TRANS-001, RF-TRANS-002 |
| OE06 â€” IntegraÃ§Ã£o Movidesk | RF-INT-001, RF-INT-002, RF-INT-003 |
| OE07 â€” ComunicaÃ§Ãµes | RF-EMAIL-001, RF-EMAIL-002 |

> Ver [[01-Fundacao/Objetivos.md|Objetivos]] e [[02-Requisitos/Requisitos-Funcionais.md|Requisitos Funcionais]].

---

## 2. Requisitos vs Casos de Uso

| RF | Caso de Uso Relacionado |
|----|------------------------|
| RF-ACOMP-001, RF-ACOMP-002 | UC-001 â€” Iniciar/Finalizar Acompanhamento |
| RF-AUDIO-001 a RF-AUDIO-005 | UC-002 â€” Gravar Ãudio do Atendimento |
| RF-TRANS-001 a RF-TRANS-004 | UC-003 â€” Transcrever e Resumir Atendimento |
| RF-MEM-001 a RF-MEM-004 | UC-004 â€” Registrar Conhecimento no Obsidian |
| RF-OS-001, RF-OS-002, RF-OS-003, RF-OS-005 | UC-005 â€” Sugerir Fechamento de OS |
| RF-EMAIL-001 | UC-006 â€” Gerar E-mail de SolicitaÃ§Ã£o de Compra |
| RF-EMAIL-002 | UC-007 â€” Gerar E-mail de Comunicado |
| RF-IA-001, RF-CONSULTA-001, RF-CONSULTA-002 | UC-008 â€” Consultar HistÃ³rico e Sugerir SoluÃ§Ã£o |
| RF-IA-003, RF-IA-004 | UC-009 â€” Responder Pergunta Durante Atendimento |
| RF-SEG-001, RF-SEG-004 | UC-010 â€” Revisar e Aprovar AÃ§Ãµes Pendentes |

> Ver [[02-Requisitos/Casos-de-Uso.md|Casos de Uso]].

---

## 3. Casos de Uso vs Fluxos

| Caso de Uso | Fluxo Relacionado |
|-------------|-------------------|
| UC-001 a UC-010 | Fluxo 1 â€” Macro do Atendimento Completo |
| UC-002, UC-003 | Fluxo 2 â€” GravaÃ§Ã£o e TranscriÃ§Ã£o de Ãudio |
| UC-004 | Fluxo 3 â€” Registro de Conhecimento no Obsidian |
| UC-005 | Fluxo 4 â€” Fechamento de OS |
| UC-006, UC-007 | Fluxo 5 â€” GeraÃ§Ã£o de E-mail |
| UC-008 | Fluxo 6 â€” Consulta de HistÃ³rico e SugestÃ£o de SoluÃ§Ã£o |
| UC-010 | Fluxo 7 â€” Painel de AprovaÃ§Ãµes |

> Ver [[03-Comportamento/Fluxos.md|Fluxos]].

---

## 4. Riscos vs ADRs

| Risco | ADR Relacionada |
|-------|-----------------|
| RISK-TEC-001 â€” Falha na transcriÃ§Ã£o | [[04-Arquitetura/ADRs.md\|ADR-003]] |
| RISK-TEC-002 â€” LatÃªncia do LLM | [[04-Arquitetura/ADRs.md\|ADR-002]] |
| RISK-TEC-003 â€” DependÃªncia API Movidesk | [[04-Arquitetura/ADRs.md\|ADR-007]] |
| RISK-TEC-005 â€” Perda de dados Obsidian | [[04-Arquitetura/ADRs.md\|ADR-001]] |
| RISK-SEG-001 â€” GravaÃ§Ã£o nÃ£o autorizada | [[04-Arquitetura/ADRs.md\|ADR-012]] |
| RISK-SEG-003 â€” ExposiÃ§Ã£o de chaves API | [[04-Arquitetura/ADRs.md\|ADR-010]] |
| RISK-PROJ-002 â€” Complexidade integraÃ§Ã£o | [[04-Arquitetura/ADRs.md\|ADR-007]] |

> Ver [[03-Comportamento/Riscos.md|Riscos]] e [[04-Arquitetura/ADRs.md|ADRs]].

---

## 5. ADRs vs Arquitetura

| ADR | Tema | Documento Relacionado |
|-----|------|----------------------|
| ADR-001 | Obsidian como MemÃ³ria | [[05-Dados/Memoria-Obsidian.md]] |
| ADR-002 | Hermes como Orquestrador | [[04-Arquitetura/Arquitetura.md]], [[04-Arquitetura/Componentes.md]] |
| ADR-003 | Whisper para TranscriÃ§Ã£o | [[04-Arquitetura/Componentes.md#C05---transcriber]], [[04-Arquitetura/Arquitetura.md]] |
| ADR-004 | Qdrant para Busca | [[05-Dados/Banco-de-Dados.md]] |
| ADR-005 | n8n para AutomaÃ§Ã£o | [[04-Arquitetura/Integracoes.md]], [[04-Arquitetura/Operacao.md]] |
| ADR-006 | CLI como Interface PrimÃ¡ria | [[04-Arquitetura/Operacao.md]], [[04-Arquitetura/Componentes.md#C01---cli-interface-hermes]] |
| ADR-007 | Ports & Adapters (Hexagonal) | [[04-Arquitetura/Arquitetura.md]], [[04-Arquitetura/Componentes.md]] |
| ADR-008 | Python como Linguagem | [[04-Arquitetura/Convencoes-Codigo.md]], [[04-Arquitetura/Arquitetura.md#10-stack-tecnolÃ³gica-final]] |
| ADR-009 | Daemon + CLI | [[04-Arquitetura/Operacao.md]] |
| ADR-010 | Config Centralizada | [[04-Arquitetura/Configuracao.md]] |
| ADR-011 | Event Bus | [[04-Arquitetura/Arquitetura.md]], [[04-Arquitetura/Componentes.md#C036---eventbus]] |
| ADR-012 | Named Pipe (IPC) | [[04-Arquitetura/Operacao.md]] |
| ADR-013 | DI via Composition Root | [[04-Arquitetura/Estrutura-Projeto.md]], [[04-Arquitetura/Convencoes-Codigo.md#8-injeÃ§Ã£o-de-dependÃªncia]] |
| ADR-014 | AbstraÃ§Ã£o de Transporte | [[04-Arquitetura/Operacao.md#9-expansÃ£o-futura-acesso-remoto-via-tcp]] |
| ADR-015 | Desafio de Ãudio Remoto | [[04-Arquitetura/Operacao.md#95-nota-sobre-Ã¡udio-remoto]] |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

