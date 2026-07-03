---
id: TASK-001
status: READY
criada: 2026-07-03
tipo: infra
prioridade: P0
depende: —
---

# TASK-001: Setup do repositorio git e estrutura de pastas

## Contexto
Projeto em estagio inicial. Backlog define B-001 como item P0 bloqueante.
Repositorio git iniciado em `C:\Users\v2admin\Documents\Obisidian\ProjetoX`.
Remote configurado para `github.com/atendimento4-byte/projetox.git`.

## Objetivo
Configurar repositorio git, estrutura Python basica, e fazer primeiro commit.

## Arquivos Afetados
- `pyproject.toml` (novo)
- `.gitignore` (ja criado)
- `src/__init__.py` (novo)
- `README.md` (link para SDD-Index)

## Criterios de Aceitacao
- [ ] Git remote configurado e funcional
- [ ] pyproject.toml basico com nome, versao, descricao
- [ ] Estrutura src/ com __init__.py
- [ ] .gitignore funcional
- [ ] README.md referenciando documentacao
- [ ] Primeiro commit realizado na branch main

## Prompt para OpenCode
Execute os comandos para finalizar o setup do repositorio:
1. Criar pyproject.toml com nome "projetox", python >=3.11
2. Criar src/projetox/__init__.py
3. Criar README.md apontando para 00-Index/SDD-Index.md
4. git add .
5. git commit -m "feat: initial project setup with documentation and source structure"
6. git branch -m master main (renomear branch)
7. git remote add origin https://github.com/atendimento4-byte/projetox.git

## Revisao
- [ ] Segue arquitetura
- [ ] Segue ADRs
- [ ] Nao quebrou features existentes
- [ ] Documentacao atualizada
- [ ] Tarefa concluida em:
