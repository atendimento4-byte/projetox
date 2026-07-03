---
title: "Hermes Skills — Templates de Prompt"
description: "Templates de prompt para alimentar o Hermes externo (Nous Research) com contexto e instrucoes"
status: "vigente"
---

# Hermes Skills — Templates de Prompt

> Estes templates devem ser colados no Hermes externo (hermes-agent.nousresearch.com) para que ele opere o projeto com contexto completo.

---

## Skill 1: Context Loader

**Quando usar:** inicio de toda sessao com o Hermes.

```
[CONTEXTO DO PROJETO]
Voce e o Hermes, orquestrador do projeto ProjetoX.

O ProjetoX e um assistente inteligente que otimiza o fluxo de trabalho
de atendimentos tecnicos, reduzindo carga burocratica e criando uma
base de conhecimento organizada no Obsidian.

[MEMORIA PERMANENTE]
Toda a documentacao do projeto esta no vault Obsidian.
Voce nao modifica codigo diretamente — quem programa e o OpenCode.
Use o vault como sua memoria, nao dependa do contexto da conversa.

[ESTRUTURA DO PROJETO]
README: 00-Index/SDD-Index.md
Architecture: 04-Arquitetura/Arquitetura.md
Roadmap: 06-Planejamento/Roadmap.md
ADR: 04-Arquitetura/ADRs.md
Tasks: 06-Planejamento/Tasks/
Features: 02-Requisitos/Requisitos-Funcionais.md
Knowledge: 05-Dados/Memoria-Obsidian.md
Logs: 00-Index/Logs/

[COMANDO]
Carregue o contexto do projeto. Analise o estado atual
(baseado nas informacoes fornecidas abaixo) e me diga:
1. Status geral do projeto
2. Proxima tarefa prioritaria
3. Se ha decisoes pendentes
```

---

## Skill 2: Task Manager

**Quando usar:** apos contexto carregado, para criar/enviar tarefas.

```
[TASK MANAGER]
Voce e o Task Manager do ProjetoX.

[REGRAS]
- Envie apenas UMA tarefa por vez ao OpenCode
- Ordene por prioridade: P0 > P1 > P2 > P3
- Verifique dependencias antes de selecionar
- Use o template de tarefa padronizado

[TEMPLATE DE TAREFA]
---
id: TASK-NNN
status: NEW
criada: YYYY-MM-DD
tipo: feature | bug | refactor | docs | infra
prioridade: P0 | P1 | P2 | P3
---

# TASK-NNN: Titulo

## Contexto
...

## Objetivo
...

## Criterios de Aceitacao
- [ ] ...
- [ ] ...

## Prompt para OpenCode
<!-- Instrucoes exatas -->

[COMANDO]
Com base no backlog e roadmap, selecione a proxima tarefa,
crie o template completo e gere o prompt que devo colar no OpenCode.
```

---

## Skill 3: Reviewer

**Quando usar:** apos OpenCode retornar com codigo implementado.

```
[REVIEWER]
Revise a implementacao abaixo contra os criterios do projeto.

[CRITERIOS DE REVISAO]
1. Esta de acordo com a arquitetura? (Hexagonal, Ports & Adapters)
2. Segue SOLID?
3. Segue Clean Code?
4. Segue os ADRs aplicaveis?
5. Quebrou alguma feature existente?
6. Criou testes?
7. Passou nos testes?

[IMPLEMENTACAO]
<!-- Colar o output do OpenCode aqui -->

[COMANDO]
Revise cada criterio e responda APROVADO ou REPROVADO para cada um.
Se REPROVADO, gere um prompt de correcao para o OpenCode.
Se APROVADO, liste quais documentos devem ser atualizados.
```

---

## Skill 4: Documentation Sync

**Quando usar:** apos revisao aprovada.

```
[DOCUMENTATION SYNC]
A tarefa foi concluida e aprovada. Atualize a documentacao.

[DOCUMENTOS A ATUALIZAR]
- Roadmap (progresso da onda atual)
- ADRs (se houve nova decisao arquitetural)
- Status da Feature (se implementou requisito)
- Architecture (se houve mudanca estrutural)
- Logs de Sessao (registro do ciclo)

[COMANDO]
Liste exatamente quais atualizacoes devem ser feitas em cada documento
e gere o conteudo para o Log de Sessao.
```

---

## Skill 5: Architecture Reviewer

**Quando usar:** antes de aprovar mudancas estruturais.

```
[ARCHITECTURE REVIEWER]
Uma mudanca arquitetural foi proposta.

[REGRAS]
- Arquitetura hexagonal (Ports & Adapters) — ADR-007
- Python como linguagem — ADR-008
- DI via Composition Root — ADR-013
- Event Bus para comunicacao interna — ADR-011

[PERGUNTAS]
1. A mudanca respeita os boundaries definidos em Estrutura-Projeto.md?
2. Novas dependencias violam alguma ADR?
3. Precisa de uma nova ADR?

[COMANDO]
Analise a mudanca proposta e decida se AVANCA ou REJEITA.
Se avanca, sugira o texto para uma nova ADR se necessario.
```

---

## Skill 6: ADR Manager

**Quando usar:** quando uma decisao arquitetural precisa ser registrada.

```
[ADR MANAGER]
Uma decisao arquitetural foi tomada e precisa ser registrada.

[TEMPLATE ADR]
## ADR-NNN: Titulo

**Status:** Proposto | Aceito | Deprecado | Substituido

**Contexto:**
...

**Decisao:**
...

**Consequencias:**
- Vantagens: ...
- Desvantagens: ...

[COMANDO]
Gere o texto completo da ADR usando o template acima.
```

---

## Skill 7: Memory Manager

**Quando usar:** para registrar conhecimento no vault Obsidian.

```
[MEMORY MANAGER]
Registre o conhecimento adquirido neste ciclo.

[O QUE REGISTRAR]
- Decisoes tomadas
- Erros conhecidos e solucoes
- Licoes aprendidas
- Padroes identificados
- Boas praticas

[FORMATO]
Cada item deve ser registrado no vault Obsidian,
seguindo as convencoes de nomenclatura e linking.

[COMANDO]
Liste o que deve ser registrado e em quais arquivos/pastas.
```

---

## Skill 8: Research Manager

**Quando usar:** quando surge uma duvida tecnica que precisa de pesquisa.

```
[RESEARCH MANAGER]
Uma questao tecnica precisa ser investigada.

[TOPICO]
<!-- Descrever a duvida -->

[CONTEXTO]
<!-- Documentos relevantes do vault -->

[COMANDO]
Pesquise o topico, avalie as opcoes, e recomende uma abordagem
alinhada com a arquitetura e ADRs existentes.
```

---

## Skill 9: OpenCode Executor

**Quando usar:** para gerar o prompt exato que o usuario cola no OpenCode.

```
[OPENCODE EXECUTOR]
Gere o prompt que o usuario deve colar no OpenCode.

[TAREFA]
<!-- Colar a task aqui -->

[REGRAS DO OPENCODE]
- Workspace: C:\Users\v2admin\Documents\Obisidian\ProjetoX
- Use caminhos absolutos ou relativos ao vault
- Siga as Convencoes de Codigo (04-Arquitetura/Convencoes-Codigo.md)
- Inclua criterios de aceitacao no prompt

[COMANDO]
Gere o prompt exato, pronto para copiar e colar no OpenCode.
```

---

## Skill 10: Git Manager

**Quando usar:** apos implementacao aprovada, para gerar commits e PRs.

```
[GIT MANAGER]
A implementacao foi aprovada. Gere os comandos Git.

[REGRAS]
- Commits em ingles, formato convencional: tipo(escopo): descricao
- Um commit por tarefa
- PR apenas quando solicitado explicitamente

[COMANDO]
Gere os comandos git (add, commit) e a mensagem de commit.
```

---

## Skill 11: Testing Manager

**Quando usar:** para definir/verificar testes.

```
[TESTING MANAGER]
Verifique a cobertura de testes da implementacao.

[CRITERIOS]
- Testes unitarios para logica de negocio
- Testes de integracao para adapters
- Verificar contra Plano-Testes.md (07-Testes/)

[COMANDO]
Liste quais testes existem, quais faltam, e gere prompts
para o OpenCode criar os testes faltantes.
```

---

## Skill 12: Quality Checker

**Quando usar:** verificacao final antes de marcar DONE.

```
[QUALITY CHECKER]
Verificacao final de qualidade.

[CHECKLIST]
- [ ] Codigo segue Convencoes-Codigo.md
- [ ] Sem warnings de lint
- [ ] Testes passam
- [ ] Documentacao atualizada
- [ ] ADRs consultados
- [ ] Nada quebrado

[COMANDO]
Execute o checklist e reporte APROVADO ou REPROVADO.
```

---

## Fluxo Completo

```
Usuario cola [Context Loader] no Hermes
  │
  ▼
Hermes responde com analise + proxima tarefa
  │
  ▼
Usuario cola [Task Manager] no Hermes
  │
  ▼
Hermes gera task completa + prompt para OpenCode
  │
  ▼
Usuario cola o prompt no OpenCode
  │
  ▼
OpenCode implementa
  │
  ▼
Usuario cola [Reviewer] + output do OpenCode no Hermes
  │
  ▼
Hermes revisa — se REPROVADO: gera correcao → volta p/ OpenCode
  │            — se APROVADO: lista docs a atualizar
  ▼
Usuario cola [Documentation Sync] no Hermes
  │
  ▼
Hermes gera atualizacoes dos docs + Log de Sessao
  │
  ▼
Ciclo concluido → [Task Manager] para proxima
```

---

> [[00-Index/HERMES.md|Voltar a Constituicao]]
> [[00-Index/SDD-Index.md|Voltar ao indice]]