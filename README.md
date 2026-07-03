# ProjetoX

> Assistente inteligente para otimizar fluxo de atendimentos técnicos.

[![CI](https://github.com/atendimento4-byte/projetox/actions/workflows/ci.yml/badge.svg)](https://github.com/atendimento4-byte/projetox/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000)](https://docs.astral.sh/ruff)

## Sobre

O **ProjetoX** reduz a carga burocrática de atendimentos técnicos automatizando:
- Gravação de áudio com confirmação explícita
- Transcrição via Whisper API
- Extração de pontos-chave via LLM (Anthropic Claude ou OpenAI)
- Registro estruturado no Obsidian
- Geração de resumos e ordens de serviço
- Fila de aprovações e log de auditoria

## Quick Start

```bash
# 1. Ambiente
uv venv --python 3.12
uv pip install -e ".[dev]"

# 2. Iniciar daemon (mantém estado entre comandos)
python -m projetox.daemon

# 3. Usar CLI
projetox --help
```

## Comandos

```bash
# Acompanhamento
projetox acompanhamento iniciar <chamado> <cliente>    # Iniciar sessão
projetox acompanhamento finalizar                       # Finalizar sessão
projetox acompanhamento status                          # Status da sessão

# Gravação de Áudio
projetox acompanhamento gravar iniciar                  # Iniciar gravação
projetox acompanhamento gravar pausar                   # Pausar
projetox acompanhamento gravar retomar                  # Retomar
projetox acompanhamento gravar parar                    # Parar

# Transcrição e IA
projetox transcrever                                    # Transcrever áudio
projetox resumir                                        # Gerar resumo estruturado
projetox revisar                                        # Revisar/editar antes de salvar

# Memória
projetox salvar --resumo '{...}'                        # Salvar no Obsidian

# Controle
projetox pendentes                                      # Aprovações pendentes
projetox auditoria                                      # Log de auditoria
```

## Arquitetura

```
src/projetox/
├── acompanhamento/     # Domínio de sessões (DDD)
├── apresentacao/cli/   # Interface Typer (7 comandos)
├── aprovacao/          # Fila de aprovações
├── audio/              # Gravação sounddevice (Ports & Adapters)
├── auditoria/          # Log de auditoria
├── compartilhado/      # Erros, modelos, cache, IPC
├── daemon/             # Servidor IPC (Named Pipe/TCP)
├── llm/                # LLM (Anthropic, OpenAI)
├── memoria/            # Integração Obsidian
└── transcricao/        # Whisper API + validação
```

**ADR:** [15 decisões de arquitetura](https://github.com/atendimento4-byte/projetox/blob/main/04-Arquitetura/ADRs.md)

## Infraestrutura (Docker)

```bash
docker compose up -d    # PostgreSQL + Qdrant
```

| Serviço | Porta | Tecnologia |
|---------|:-----:|:-----------|
| PostgreSQL | 5432 | Banco relacional |
| Qdrant | 6333 | Banco vetorial |
| Daemon | 8790 | IPC via TCP/Named Pipe |

## Desenvolvimento

```bash
# Testes
uv run pytest tests/ -v

# Lint
uv run ruff check src/

# Type check
uv run mypy src/

# Daemon
python -m projetox.daemon
```

## Stack

- **Python 3.12+** · Typer · Rich · SQLAlchemy 2.0 (async)
- **Whisper API** · **Anthropic Claude** · **OpenAI GPT**
- **sounddevice** · **soundfile** · **structlog**
- **PostgreSQL** · **Redis** · **Qdrant** · **Obsidian**
- **Docker Compose** · **GitHub Actions** (CI)
- **pytest** · **ruff** · **mypy**

## Licença

MIT
