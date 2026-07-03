---
title: "Bootstrap — Primeira Execucao"
description: "Roteiro de como iniciar o Hermes (Nous Research) pela primeira vez"
status: "vigente"
---

# Bootstrap — Primeira Execucao

> Como iniciar o Hermes externo e o OpenCode pela primeira vez.

---

## Passo 1 — Abrir o Hermes

Acesse: **https://hermes-agent.nousresearch.com**

---

## Passo 2 — Primeiro Prompt

Cole o **Context Loader** (Skill 1 de [[00-Index/Hermes-Skills.md]]):

```
[CONTEXTO DO PROJETO]
Voce e o Hermes, orquestrador do projeto ProjetoX.

O ProjetoX e um assistente inteligente que otimiza o fluxo de trabalho
de atendimentos tecnicos, reduzindo carga burocratica e criando uma
base de conhecimento organizada no Obsidian.
... (texto completo em Hermes-Skills.md)
```

---

## Passo 3 — Abrir o OpenCode

Em outro terminal, execute:

```cmd
C:\Users\v2admin\Documents\ProjetoX\start-opencode.cmd
```

---

## Passo 4 — Ciclo de Trabalho

```
[VOCE]                     [HERMES]              [OPENCODE]
  │                          │                      │
  ├── Context Loader ──────► │                      │
  │                          ├── Le SDD-Index       │
  │                          ├── Le Arquitetura     │
  │                          ├── Le Roadmap         │
  │                          ├── Le ADRs            │
  │                          ├── Le Logs            │
  │◄── Resumo + prox task ──┤                      │
  │                          │                      │
  ├── Task Manager ─────────►│                      │
  │                          ├── Gera task + prompt │
  │◄── Prompt da tarefa ────┤                      │
  │                          │                      │
  ├── Cola prompt ─────────────────────────────────►│
  │                          │                      ├── Le vault
  │                          │                      ├── Implementa
  │                          │                      ├── Testa
  │                          │                      ├── Lint
  │                          │                      ├── Prepara output
  │◄── Output do OC ────────────────────────────────┤
  │                          │                      │
  ├── Reviewer + output ────►│                      │
  │                          ├── Revisa              │
  │◄── Aprovado/Rejeitado ──┤                      │
  │                          │                      │
  │  Se REJEITADO:                                  │
  │  ├── Correcao ─────────────────────────────────►│
  │  └── Volta ao Reviewer                          │
  │                          │                      │
  │  Se APROVADO:                                   │
  ├── Doc Sync ─────────────►│                      │
  │                          ├── Lista atualizacoes │
  │◄── Docs a atualizar ────┤                      │
  │                          │                      │
  └── Proximo ciclo ────────────────────────────────┘
```

## Comandos do Dia a Dia

| Situacao | Prompt Hermes |
|----------|--------------|
| Iniciar sessao | `[Context Loader]` (Skill 1) |
| Criar tarefa | `[Task Manager]` (Skill 2) |
| Revisar codigo | `[Reviewer]` (Skill 3) |
| Atualizar docs | `[Documentation Sync]` (Skill 4) |
| Decisao arquitetural | `[Architecture Reviewer]` (Skill 5) |
| Registrar ADR | `[ADR Manager]` (Skill 6) |
| Acessar vault | `[Hermes-Vault]` (Skill 13) |
| Commitar | `[Git Manager]` (Skill 10) |

---

> [[00-Index/Hermes-Skills.md|Skills completas (14 skills)]]
> [[00-Index/HERMES.md|Constituicao]]
> [[00-Index/SDD-Index.md|Voltar ao indice]]