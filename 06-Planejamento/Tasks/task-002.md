---
id: TASK-002
status: NEW
criada: 2026-07-03
tipo: infra
prioridade: P0
depende: TASK-001
---

# TASK-002: Setup ambiente Python e dependências

## Contexto
Sprint 0 — B-002 (Setup ambiente Python/dependências). O repositório está configurado (B-001 ✅), pyproject.toml básico existe, mas sem dependências declaradas. O ambiente de desenvolvimento precisa ser configurado para permitir o início da Onda 1 (CLI, gravação, etc.).

O projeto segue ADR-008 (Python) e ADR-013 (DI manual). As dependências estão listadas em [[04-Arquitetura/Convencoes-Codigo.md#10-dependencias-do-projeto]].

Python disponível:
- 3.14.3 (sistema — `python3`)
- 3.11.15 (via uv — `python`)
- uv 0.11.26 instalado

## Objetivo
Configurar ambiente virtual, instalar todas as dependências de produção e desenvolvimento, e verificar que o pacote `projetox` importa corretamente.

## Arquivos Afetados
- `pyproject.toml` (modificar — adicionar dependências)
- `.venv/` (novo — ambiente virtual)
- `src/projetox/__init__.py` (verificar)
- `src/projetox/compartilhado/` (novo — estrutura inicial)
- `src/projetox/compartilhado/erros/` (novo — Resultado pattern + hierarquia de erros)
- `ruff.toml` (novo — config do linter)
- `mypy.ini` (novo — config do type checker)

## Critérios de Aceitação
- [ ] Ambiente virtual criado com `uv venv` usando Python >=3.12 (ou 3.11 mantendo compatibilidade)
- [ ] `pyproject.toml` completo com todas as dependências de produção e desenvolvimento
- [ ] `ruff.toml` configurado conforme Convencoes-Codigo.md (linha 100, regras especificadas)
- [ ] `mypy.ini` configurado em modo strict
- [ ] `pip install -e .` funcional (pacote instalável em modo editable)
- [ ] `python -c "import projetox"` executa sem erro
- [ ] `ruff check src/` executa sem erros
- [ ] `mypy src/` executa sem erros (permissivo inicialmente — ajustar conforme código cresce)
- [ ] Estrutura `src/projetox/compartilhado/erros/` criada com `__init__.py` e classes base de erro (Resultado, hierarquia)
- [ ] `src/projetox/__init__.py` atualizado com versão e docstring do pacote
- [ ] Commit com mensagem padronizada

## Observações
- Usar `uv` para gerenciar o ambiente (`uv venv`, `uv pip install`)
- Python 3.12+ é preferível (ADR-008), mas 3.11 é aceitável se não houver 3.12 disponível localmente
- Dependências de produção detalhadas em Convencoes-Codigo.md seção 10.1
- Dependências de desenvolvimento seção 10.2
- Configuração de Ruff e mypy conforme seções 2 e 9 de Convencoes-Codigo.md
- Se `uv` não tiver Python 3.12 disponível localmente, baixar com `uv python install 3.12`

## Prompt para OpenCode
```
Execute o setup completo do ambiente Python para o projetox seguindo TASK-002.

1. Crie o ambiente virtual com `uv venv` (use Python 3.12 se disponível, senão 3.11)
2. Atualize `pyproject.toml` com todas as dependências de produção (typer, rich, pydantic, sqlalchemy, asyncpg, redis, anthropic, openai, httpx, structlog)
3. Adicione dependências de desenvolvimento (ruff, mypy, pytest, pytest-asyncio, pytest-cov, pytest-mock, factory-boy)
4. Crie `ruff.toml` com linha 100, regras: E, F, I, N, W, UP, B, SIM, ARG, COM, C4, T10, RUF, PL, PT, RET, TRY, EM, C90
5. Crie `mypy.ini` com modo strict
6. Instale o pacote em modo editable: `uv pip install -e ".[dev]"
7. Crie a estrutura `src/projetox/compartilhado/erros/` com:
   - `__init__.py` exportando Resultado e classes de erro
   - `resultado.py` com a classe Resultado[T, E] (sucesso/ok, falha/erro)
   - `hierarquia.py` com ErroAplicacao → ErroDominio, ErroAplicacaoServico, ErroInfraestrutura e subclasses
8. Atualize `src/projetox/__init__.py` com versão 0.1.0 e docstring
9. Execute `ruff check src/` e corrija se necessário
10. Execute `mypy src/` (pode ter erros de import — aceitável nesta fase)
11. git add . && git commit -m "feat: setup ambiente Python com dependencias, linter e estrutura de erros"
```

## Revisão
- [ ] Segue arquitetura
- [ ] Segue SOLID / Clean Code
- [ ] Segue ADRs (ADR-008, ADR-013)
- [ ] Não quebrou features existentes
- [ ] Testes criados e passando
- [ ] Documentação atualizada
- [ ] Tarefa concluída em:
