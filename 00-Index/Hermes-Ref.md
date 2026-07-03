---
title: "Hermes — Referencia Rapida"
description: "Arquitetura, arquivos, comandos e fluxo do Hermes externo + OpenCode"
status: "vigente"
---

# Hermes — Referencia Rapida

> Documentacao pratica do sistema Hermes (Nous Research) + OpenCode + Obsidian.

---

## Arquitetura

```
                     Voce
                       │
         ┌─────────────┼─────────────┐
         │                           │
         ▼                           ▼
   ┌──────────┐              ┌──────────────┐
   │  Hermes  │              │   OpenCode   │
   │ (externo)│◄──prompts──►│(implementa)  │
   └────┬─────┘              └──────────────┘
        │
        │ le/escreve via usuario
        ▼
   ┌──────────┐
   │ Obsidian │ ← memoria permanente
   │  vault   │
   └──────────┘
```

---

## Arquivos do Sistema

| Arquivo | Local | Funcao |
|---------|-------|--------|
| `HERMES.md` | 00-Index/ | Constituicao: identidade, regras, workflow, task template |
| `Hermes-Skills.md` | 00-Index/ | 12 templates de prompt para o Hermes externo |
| `Bootstrap.md` | 00-Index/ | Roteiro de primeira execucao |
| `opencode.json` | vault root / ProjetoX | Config minima (apenas builder subagent) |
| `start-opencode.cmd` | ProjetoX/ | Atalho para abrir OpenCode no vault |
| `Tasks/README.md` | 06-Planejamento/ | Ciclo de vida da task + 10 estados |
| `Logs/README.md` | 00-Index/ | Protocolo de handover entre sessoes |

---

## As 12 Skills do Hermes

| # | Skill | Prompt em | Quando usar |
|---|-------|-----------|-------------|
| 1 | Context Loader | Hermes-Skills.md | Inicio de toda sessao |
| 2 | Task Manager | Hermes-Skills.md | Selecionar/criar tarefa |
| 3 | Reviewer | Hermes-Skills.md | Revisar output do OpenCode |
| 4 | Documentation Sync | Hermes-Skills.md | Apos revisao aprovada |
| 5 | Architecture Reviewer | Hermes-Skills.md | Mudancas estruturais |
| 6 | ADR Manager | Hermes-Skills.md | Registrar decisao |
| 7 | Memory Manager | Hermes-Skills.md | Registrar conhecimento |
| 8 | Research Manager | Hermes-Skills.md | Duvidas tecnicas |
| 9 | OpenCode Executor | Hermes-Skills.md | Gerar prompt p/ OpenCode |
| 10 | Git Manager | Hermes-Skills.md | Commits e PRs |
| 11 | Testing Manager | Hermes-Skills.md | Verificar cobertura |
| 12 | Quality Checker | Hermes-Skills.md | Checklist final |

---

## Estados da Tarefa

```
NEW → ANALYZING → PLANNING → READY → IN_PROGRESS
→ REVIEW → TESTING → DOCUMENTING → DONE → ARCHIVED
```

---

## Regras do Hermes

| Regra | Descricao |
|-------|-----------|
| **Nunca implementa** | Nem uma linha de codigo |
| **1 task por vez** | Nunca enviar varias ao OpenCode |
| **Memoria no vault** | Obsidian como fonte primaria, nao contexto LLM |
| **Revisao obrigatoria** | 7 criterios antes de aprovar |
| **Docs sempre atualizados** | Apos cada ciclo |
| **Handover** | Log salvo ao final de cada sessao |
| **Governance** | Acoes criticas exigem aprovacao humana |

---

## Comandos do Usuario

### Hermes (navegador)
Cole o template da skill relevante de [[00-Index/Hermes-Skills.md]].

### OpenCode (terminal)
```cmd
start-opencode
```
E cole o prompt gerado pelo Hermes (via Skill 9 — OpenCode Executor).

---

> [[00-Index/Hermes-Skills.md|Skills (prompts)]]
> [[00-Index/HERMES.md|Constituicao]]
> [[00-Index/Bootstrap.md|Primeira execucao]]
> [[00-Index/SDD-Index.md|Voltar ao indice]]