---
title: "Guia de Setup"
description: "Pre-requisitos, Docker Compose, ambiente Python e configuracao"
status: "novo"
---

# Guia de Setup do Ambiente de Desenvolvimento

> **InstruÃ§Ãµes para configurar o ambiente de desenvolvimento do Hermes + Obsidian.**

---

## 1. PrÃ©-requisitos

| Ferramenta | VersÃ£o MÃ­nima | Obtido em | Motivo |
|------------|---------------|-----------|--------|
| **Python** | 3.12 | python.org | Linguagem principal ([[04-Arquitetura/ADRs.md\|ADR-002]]) |
| **Git** | 2.40 | git-scm.com | Controle de versÃ£o |
| **Docker** | 24.0 | docker.com | Postgres, Redis, Qdrant |
| **Docker Compose** | 2.20 | docker.com | OrquestraÃ§Ã£o local |
| **Node.js** | 18 | nodejs.org | Lua de apoio para Textual (futuro) |

## 2. RepositÃ³rio

```bash
git clone <url-do-repositorio> hermes
cd hermes

# (Opcional) Verificar assinatura dos commits
git log --show-signature
```

## 3. Ambiente Python

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Ativar (Linux/macOS)
source .venv/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependÃªncias do projeto
pip install -r requirements-dev.txt
```

## 4. ServiÃ§os com Docker Compose

```bash
# Iniciar todos os serviÃ§os de infraestrutura
docker compose up -d

# ServiÃ§os iniciados:
# - postgres:5432 â€” Banco relacional
# - redis:6379 â€” Cache e Event Bus
# - qdrant:6333 â€” Banco vetorial

# Verificar status
docker compose ps

# Parar serviÃ§os
docker compose down
```

> A estrutura do banco de dados Ã© detalhada em [[05-Dados/Banco-de-Dados.md]].

## 5. ConfiguraÃ§Ã£o Inicial

```bash
# Copiar configuraÃ§Ã£o de exemplo
cp config.example.yaml ~/.hermes/config.yaml

# Editar configuraÃ§Ã£o com seus dados
notepad ~/.hermes/config.yaml
```

Configure pelo menos:
- `credenciais.movidesk_token` â€” Token de API do Movidesk
- `credenciais.anthropic_api_key` â€” Chave da API Anthropic

> O formato completo da configuraÃ§Ã£o estÃ¡ em [[04-Arquitetura/Configuracao.md]].

## 6. VerificaÃ§Ã£o

```bash
# Verificar configuraÃ§Ã£o
hermes config validate

# Verificar conexÃ£o com serviÃ§os
hermes doctor

# Verificar versÃ£o
hermes --version
```

## 7. Executando pela Primeira Vez

```bash
# Iniciar daemon (modo debug)
hermes daemon start --debug

# Em outro terminal, testar comando simples
hermes ping

# Verificar logs
hermes logs --tail 20
```

## 8. PrÃ³ximos Passos

- Revisar [[01-Fundacao/Visao-Geral.md|VisÃ£o Geral do Sistema]]
- Explorar [[04-Arquitetura/Operacao.md|Comandos do Sistema]]
- Verificar [[06-Planejamento/MVP.md|Escopo do MVP]]

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

