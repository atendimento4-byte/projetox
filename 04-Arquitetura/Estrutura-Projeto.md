---
title: "Estrutura do Projeto"
description: "Arvore de diretorios, 5 bounded contexts, regras de dependencia"
status: "novo"
---

# Estrutura do Projeto

> **Ãrvore completa de diretÃ³rios, responsabilidades de cada pasta e regras de dependÃªncia entre camadas.**

---

## 1. Filosofia

A estrutura do projeto segue os princÃ­pios de:

- **Domain-Driven Design** â€” cÃ³digo organizado por bounded contexts, cada um com seu prÃ³prio domÃ­nio e casos de uso
- **Arquitetura Hexagonal (Ports & Adapters)** â€” domÃ­nio no centro, infraestrutura nas bordas
- **Alta coesÃ£o e baixo acoplamento** â€” cada contexto sabe o mÃ­nimo dos outros
- **Responsabilidade Ãºnica** â€” cada diretÃ³rio tem um propÃ³sito claro

---

## 2. Ãrvore Completa

```
hermes/
â”‚
â”œâ”€â”€ src/                              # CÃ³digo fonte principal
â”‚   â”œâ”€â”€ hermes/                       # Package principal (CLI thin client)
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ __main__.py               # python -m hermes
â”‚   â”‚   â”œâ”€â”€ _app.py                   # Composition Root (DI container)
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ compartilhado/            # CÃ³digo compartilhado entre contexts
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ base_entidade.py      # Classe base para entidades
â”‚   â”‚   â”‚   â”œâ”€â”€ base_objeto_valor.py  # Classe base para VOs
â”‚   â”‚   â”‚   â”œâ”€â”€ base_agregado.py      # Classe base para aggregates
â”‚   â”‚   â”‚   â”œâ”€â”€ evento_dominio.py     # Domain Event base
â”‚   â”‚   â”‚   â”œâ”€â”€ erros/               # Hierarquia de erros
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ base.py           # ErroAplicacao
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ resultado.py      # Resultado[T, Erro]
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ erros_dominio.py
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ erros_infra.py
â”‚   â”‚   â”‚   â”œâ”€â”€ logging/             # ConfiguraÃ§Ã£o de logging
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ config.py
â”‚   â”‚   â”‚   â””â”€â”€ util/                # UtilitÃ¡rios gerais
â”‚   â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚       â”œâ”€â”€ identificadores.py
â”‚   â”‚   â”‚       â””â”€â”€ data_hora.py
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ contexto/                 # Bounded Contexts do sistema
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ acompanhamento/      # Contexto: Acompanhamento de Chamados
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ di.py             # MÃ³dulo de DI do contexto
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/          # Camada de domÃ­nio
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ entidades/
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ chamado.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ objetos_valor/
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ ...vo.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ eventos/
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ ...py
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ servicos/     # Domain services
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ ...py
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ repositorios/ # Interfaces (Ports)
â”‚   â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚       â””â”€â”€ repositorio_chamado.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/        # Camada de aplicaÃ§Ã£o
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ portas/       # Interfaces de entrada
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ ...porta.py
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ casos_uso/    # Use cases
â”‚   â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ iniciar_chamado.py
â”‚   â”‚   â”‚   â”‚   â”‚       â””â”€â”€ finalizar_chamado.py
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/       # ImplementaÃ§Ã£o (Adapters)
â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚       â””â”€â”€ persistencia/ # RepositÃ³rios concretos
â”‚   â”‚   â”‚   â”‚           â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚           â””â”€â”€ repositorio_chamado_postgres.py
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ audio/               # Contexto: GravaÃ§Ã£o e TranscriÃ§Ã£o
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ di.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ entidades/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ objetos_valor/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ eventos/
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ repositorios/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ portas/
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ casos_uso/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/
â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ gravador/     # Captura de Ã¡udio
â”‚   â”‚   â”‚   â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚       â”‚   â””â”€â”€ ...py
â”‚   â”‚   â”‚   â”‚       â””â”€â”€ transcritor/  # Whisper
â”‚   â”‚   â”‚   â”‚           â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚           â””â”€â”€ ...py
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ memoria/             # Contexto: MemÃ³ria (Obsidian + Qdrant)
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ di.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ entidades/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ objetos_valor/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ eventos/
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ repositorios/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ portas/
â”‚   â”‚   â”‚   â”‚   â”‚   â””â”€â”€ casos_uso/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/
â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ vault/        # Obsidian filesystem
â”‚   â”‚   â”‚   â”‚       â”œâ”€â”€ banco_vetorial/ # Qdrant
â”‚   â”‚   â”‚   â”‚       â””â”€â”€ .../
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â”œâ”€â”€ comunicacao/         # Contexto: E-mail e ComunicaÃ§Ãµes
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ di.py
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/
â”‚   â”‚   â”‚   â”‚       â””â”€â”€ email/
â”‚   â”‚   â”‚   â”‚
â”‚   â”‚   â”‚   â””â”€â”€ integracao/          # Contexto: IntegraÃ§Ãµes externas
â”‚   â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚       â”œâ”€â”€ di.py
â”‚   â”‚   â”‚       â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚       â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚       â””â”€â”€ integracao/
â”‚   â”‚   â”‚           â”œâ”€â”€ movidesk/
â”‚   â”‚   â”‚           â””â”€â”€ n8n/
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ agentes/                  # Agentes de IA (cross-context)
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ base_agente.py        # Classe base
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_transcricao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_memoria.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_documentacao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_comunicacao.py
â”‚   â”‚   â”‚   â””â”€â”€ agente_consulta.py
â”‚   â”‚   â”‚
â”‚   â”‚   â””â”€â”€ infra/                    # Infraestrutura cross-context
â”‚   â”‚       â”œâ”€â”€ __init__.py
â”‚   â”‚       â”œâ”€â”€ cli/                  # Interface de linha de comando
â”‚   â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚       â”‚   â”œâ”€â”€ app.py            # App Typer (entry point)
â”‚   â”‚       â”‚   â”œâ”€â”€ cliente_ipc.py    # Cliente Named Pipe
â”‚   â”‚       â”‚   â”œâ”€â”€ exibicao.py       # Helpers Rich
â”‚   â”‚       â”‚   â”œâ”€â”€ comandos/
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ sessao.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ audio.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ transcricao.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ conhecimento.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ os.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ email.py
â”‚   â”‚       â”‚   â”‚   â”œâ”€â”€ aprovacao.py
â”‚   â”‚       â”‚   â”‚   â””â”€â”€ config.py
â”‚   â”‚       â”‚   â””â”€â”€ atalhos.py        # Hotkeys
â”‚   â”‚       â”œâ”€â”€ servico/              # Daemon Windows Service
â”‚   â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚       â”‚   â”œâ”€â”€ servidor.py       # IPC Server
â”‚   â”‚       â”‚   â”œâ”€â”€ ipc.py            # Protocolo Named Pipe
â”‚   â”‚       â”‚   â””â”€â”€ servico_windows.py# Windows Service wrapper
â”‚   â”‚       â”œâ”€â”€ persistencia/         # Bancos de dados cross-context
â”‚   â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚       â”‚   â”œâ”€â”€ postgres/
â”‚   â”‚       â”‚   â”œâ”€â”€ redis/
â”‚   â”‚       â”‚   â””â”€â”€ qdrant/
â”‚   â”‚       â”œâ”€â”€ llm/                  # LLM providers
â”‚   â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚       â”‚   â”œâ”€â”€ cliente.py        # Cliente abstrato
â”‚   â”‚       â”‚   â””â”€â”€ provedores/
â”‚   â”‚       â””â”€â”€ barramento/           # Event Bus interno
â”‚   â”‚           â”œâ”€â”€ __init__.py
â”‚   â”‚           â”œâ”€â”€ barramento.py
â”‚   â”‚           â””â”€â”€ .../
â”‚   â”‚
â”‚   â””â”€â”€ hermesd/                      # Daemon service (entry point separado)
â”‚       â”œâ”€â”€ __init__.py
â”‚       â””â”€â”€ __main__.py
â”‚
â”œâ”€â”€ testes/                           # Testes organizados por camada
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ unitario/                     # Testes unitÃ¡rios (70%)
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â””â”€â”€ contexto/
â”‚   â”‚       â”œâ”€â”€ acompanhamento/
â”‚   â”‚       â”œâ”€â”€ audio/
â”‚   â”‚       â”œâ”€â”€ memoria/
â”‚   â”‚       â”œâ”€â”€ comunicacao/
â”‚   â”‚       â””â”€â”€ integracao/
â”‚   â”œâ”€â”€ integracao/                   # Testes de integraÃ§Ã£o (20%)
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ persistencia/
â”‚   â”‚   â”œâ”€â”€ ipc/
â”‚   â”‚   â””â”€â”€ adaptadores/
â”‚   â””â”€â”€ e2e/                          # Testes end-to-end (10%)
â”‚       â”œâ”€â”€ __init__.py
â”‚       â””â”€â”€ fluxos/
â”‚
â”œâ”€â”€ scripts/                          # Scripts de automaÃ§Ã£o
â”‚   â”œâ”€â”€ setup.ps1                     # ConfiguraÃ§Ã£o do ambiente
â”‚   â”œâ”€â”€ lint.ps1                      # Executa lint + typecheck
â”‚   â”œâ”€â”€ teste.ps1                     # Executa testes
â”‚   â””â”€â”€ build.ps1                     # Build do executÃ¡vel
â”‚
â”œâ”€â”€ docker/                           # ContÃªineres
â”‚   â”œâ”€â”€ docker-compose.yml
â”‚   â”œâ”€â”€ docker-compose.override.yml
â”‚   â””â”€â”€ Dockerfile
â”‚
â”œâ”€â”€ docs/                             # DocumentaÃ§Ã£o no repositÃ³rio
â”‚   â””â”€â”€ adr/                          # ADRs exportados (consulte vault)
â”‚
â”œâ”€â”€ config/                           # Arquivos de configuraÃ§Ã£o
â”‚   â”œâ”€â”€ exemplo.yaml
â”‚   â”œâ”€â”€ desenvolvimento.yaml
â”‚   â””â”€â”€ producao.yaml
â”‚
â”œâ”€â”€ pyproject.toml                    # ConfiguraÃ§Ã£o do projeto
â””â”€â”€ README.md                         # VisÃ£o geral do projeto
```

---

## 3. Responsabilidades por DiretÃ³rio

| DiretÃ³rio | Responsabilidade |
|-----------|-----------------|
| `src/hermes/_app.py` | Composition Root. Registra todos os mÃ³dulos de DI. Configura logging. Inicia o daemon ou CLI. |
| `src/hermes/compartilhado/` | CÃ³digo que qualquer contexto pode usar. NUNCA depende de contexto. Sem lÃ³gica de negÃ³cio. |
| `src/hermes/contexto/*/dominio/` | Regras de negÃ³cio puras. Sem dependÃªncias externas. Zero imports de infra. |
| `src/hermes/contexto/*/aplicacao/` | Casos de uso. Orquestra domÃ­nio + portas. Depende apenas de interfaces. |
| `src/hermes/contexto/*/integracao/` | ImplementaÃ§Ãµes concretas das portas. Depende de SQLAlchemy, httpx, etc. |
| `src/hermes/infra/cli/` | Thin client. Comunica com daemon via Named Pipe. Zero lÃ³gica de negÃ³cio. |
| `src/hermes/infra/servico/` | Daemon. Servidor IPC + ciclo de vida. |
| `src/hermes/infra/persistencia/` | ImplementaÃ§Ãµes de banco de dados concretas. |
| `src/hermes/agentes/` | Agentes de IA. Orquestram mÃºltiplos contexts. Dependem de casos de uso. |
| `testes/` | Espelha a estrutura de `src/hermes/`. Testes por camada. |
| `scripts/` | AutomaÃ§Ã£o local (setup, lint, test, build). |
| `docker/` | Infraestrutura de contÃªineres para desenvolvimento e produÃ§Ã£o. |
| `docs/` | ADRs exportados para referÃªncia rÃ¡pida. Vault Obsidian Ã© a fonte primÃ¡ria. |

---

## 4. Regras de DependÃªncia

```
CLI (thin client)  â†  Daemon (servidor IPC)
                            â”‚
                            â–¼
                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                   â”‚  Casos de Uso  â”‚
                   â”‚  (aplicacao/)  â”‚
                   â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚ depende de interfaces
                           â–¼
                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                   â”‚   Interfaces   â”‚
                   â”‚  (dominio/*/)  â”‚
                   â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚ implementado por
                           â–¼
                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                   â”‚  Adaptadores   â”‚
                   â”‚ (integracao/)  â”‚
                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Regra fundamental:** O domÃ­nio nÃ£o sabe que a infraestrutura existe. A infraestrutura sabe do domÃ­nio.

| De/Para | Depende |
|---------|---------|
| `dominio/` â†’ outro `dominio/` | âŒ Apenas via eventos ou IDs |
| `dominio/` â†’ `infra/` | âŒ ViolaÃ§Ã£o de DDD |
| `dominio/` â†’ `compartilhado/` | âœ… âœ… |
| `aplicacao/` â†’ `dominio/` | âœ… âœ… |
| `aplicacao/` â†’ `integracao/` | âŒ Apenas via interfaces (portas) |
| `integracao/` â†’ `dominio/` | âœ… âœ… (implementa interfaces) |
| `integracao/` â†’ `infra/` | âœ… âœ… |
| `agentes/` â†’ `aplicacao/` | âœ… âœ… |
| `infra/cli/` â†’ `infra/servico/` | âœ… âœ… (via Named Pipe) |
| `infra/cli/` â†’ `dominio/` | âŒ CLI Ã© thin client |

---

## 5. Checklist para Novo Contexto

Ao criar um novo bounded context, verificar:

- [ ] DiretÃ³rio `contexto/<nome>/` criado com `__init__.py`
- [ ] `di.py` com funÃ§Ãµes de registro de dependÃªncias
- [ ] `dominio/`: entidades, VOs, eventos, serviÃ§os, repositÃ³rios (interfaces)
- [ ] `aplicacao/`: portas (interfaces de entrada), casos de uso
- [ ] `integracao/`: implementaÃ§Ãµes dos repositÃ³rios e adaptadores
- [ ] O contexto comunica-se com outros APENAS via eventos de domÃ­nio ou interfaces compartilhadas
- [ ] Testes unitÃ¡rios criados em `testes/unitario/contexto/<nome>/`
- [ ] Testes de integraÃ§Ã£o criados em `testes/integracao/`
- [ ] MÃ³dulo de DI registrado no Composition Root (`_app.py`)

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

