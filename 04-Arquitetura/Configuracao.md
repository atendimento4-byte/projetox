---
title: "Sistema de Configuracao"
description: "Configuracao YAML centralizada com JSON Schema e perfis"
status: "concluido"
---

# Sistema de ConfiguraÃ§Ã£o

> **Sistema de configuraÃ§Ã£o centralizada do Hermes: formato, schema, resoluÃ§Ã£o de secrets e perfis.**

---

## 1. Filosofia

> A decisÃ£o de usar configuraÃ§Ã£o centralizada estÃ¡ documentada na [[04-Arquitetura/ADRs.md|ADR-010]].

- **Um arquivo para governar todos:** `~/.hermes/config.yaml`
- **LegÃ­vel e editÃ¡vel manualmente:** YAML com comentÃ¡rios
- **Validado automaticamente:** JSON Schema na carga
- **Secrets fora do arquivo:** `${VARIAVEL}` resolvido de ambiente ou Windows Credential Manager
- **Hotkeys customizÃ¡veis:** Todas as teclas configurÃ¡veis no mesmo arquivo

---

## 2. LocalizaÃ§Ã£o do Arquivo

| Sistema | Caminho |
|---------|---------|
| **Windows** | `%USERPROFILE%\.hermes\config.yaml` |
| **Linux (futuro)** | `~/.hermes/config.yaml` |
| **Sobrescrita via env** | `HERMES_CONFIG=/path/to/config.yaml` |

### DiretÃ³rio de Dados

O daemon tambÃ©m cria `~/.hermes/` com estrutura:

```
~/.hermes/
â”œâ”€â”€ config.yaml                  # ConfiguraÃ§Ã£o principal
â”œâ”€â”€ config.schema.yaml          # Schema de validaÃ§Ã£o
â”œâ”€â”€ logs/
â”‚   â”œâ”€â”€ hermes.json             # Logs estruturados (NDJSON)
â”‚   â””â”€â”€ hermesd.log            # Logs do daemon (texto)
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ sessions/               # Estado de sessÃµes (recuperaÃ§Ã£o)
â”‚   â””â”€â”€ audio/                  # GravaÃ§Ãµes temporÃ¡rias
â””â”€â”€ backups/
    â””â”€â”€ obsidian/               # Backups do vault
```

---

## 3. Schema do Config.yaml

```yaml
# =============================================================================
# Hermes â€” ConfiguraÃ§Ã£o Principal
# =============================================================================
# LocalizaÃ§Ã£o padrÃ£o: ~/.hermes/config.yaml
# Sobrescrita via: HERMES_CONFIG=/path/to/config.yaml
# Secrets via: ${NOME_DA_VARIAVEL} (ambiente ou Windows Credential Manager)
# =============================================================================

# â”€â”€ Geral â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
hermes:
  # NÃ­vel de log: debug, info, warn, error
  log_level: info

  # DiretÃ³rio de dados do Hermes (logs, backups, estado)
  data_dir: ~/.hermes

# â”€â”€ Daemon â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  daemon:
    # Porta lÃ³gica para IPC (nÃ£o Ã© porta TCP â€” identificador do Named Pipe)
    pipe_name: hermes

    # Timeout para resposta do CLI (segundos)
    request_timeout: 30

# â”€â”€ Obsidian â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  obsidian:
    # Caminho absoluto para o vault do Obsidian
    vault_path: "C:/Users/v2admin/Documents/Obisidian/ProjetoX"

    # Backup automÃ¡tico do vault (ativar/desativar)
    auto_backup: true

    # DiretÃ³rio para backups
    backup_path: ~/.hermes/backups/obsidian

# â”€â”€ Ãudio â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  audio:
    # Dispositivo de entrada (null = padrÃ£o do sistema)
    device: null

    # Taxa de amostragem (Hz): 16000, 44100, 48000
    sample_rate: 16000

    # Canais: 1 (mono) ou 2 (stÃ©reo)
    channels: 1

    # Formato de gravaÃ§Ã£o: wav, mp3
    format: wav

    # Dias de retenÃ§Ã£o de gravaÃ§Ãµes (0 = nunca apagar)
    retention_days: 90

    # Filtro de ruÃ­do ambiente
    noise_filter: true

# â”€â”€ TranscriÃ§Ã£o â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  transcription:
    # Provider: whisper_api | whisper_local
    provider: whisper_api

    # Modelo Whisper: turbo, large, medium, small, base, tiny
    model: turbo

    # Idioma (auto-detect se vazio)
    language: pt

    # Timeout da transcriÃ§Ã£o (segundos)
    timeout: 60

# â”€â”€ LLM (Modelo de Linguagem) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  llm:
    # Provider: anthropic | openai | google
    provider: anthropic

    # Modelo especÃ­fico do provider
    # Anthropic: claude-sonnet-4-20250514, claude-haiku-3-20240307
    # OpenAI: gpt-4o, gpt-4o-mini
    # Google: gemini-1.5-pro, gemini-1.5-flash
    model: claude-sonnet-4-20250514

    # Chave da API (referÃªncia a variÃ¡vel de ambiente)
    api_key: ${ANTHROPIC_API_KEY}

    # MÃ¡ximo de tokens na resposta
    max_tokens: 4096

    # Temperatura (0.0 = determinÃ­stico, 1.0 = criativo)
    temperature: 0.3

    # Cache de respostas (segundos, 0 = desligado)
    cache_ttl: 3600

# â”€â”€ Movidesk â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  movidesk:
    # URL base da API
    base_url: "https://api.movidesk.com/public/v1"

    # Token de autenticaÃ§Ã£o
    token: ${MOVIDESK_TOKEN}

    # Rate limit mÃ¡ximo (requisiÃ§Ãµes por segundo)
    rate_limit: 10

# â”€â”€ E-mail â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  email:
    # Provider: smtp | gmail | outlook
    provider: smtp

    # Remetente padrÃ£o
    from_name: "Supervisor TÃ©cnico"
    from_email: "tecnico@empresa.com"

    # SMTP (usado se provider = smtp)
    smtp:
      host: smtp.gmail.com
      port: 587
      use_tls: true
      user: ${EMAIL_USER}
      password: ${EMAIL_APP_PASSWORD}

# â”€â”€ Banco Vetorial â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  vector_store:
    # Provider: qdrant | chroma (futuro)
    provider: qdrant

    # ConexÃ£o Qdrant
    host: localhost
    port: 6333
    collection_name: notas_obsidian

    # Tamanho do embedding (1536 = ada-002, 768 = miniLM, etc)
    embedding_size: 1536

# â”€â”€ PostgreSQL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  postgresql:
    host: localhost
    port: 5432
    database: hermes
    user: hermes
    password: ${PG_PASSWORD}

# â”€â”€ Redis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  redis:
    host: localhost
    port: 6379
    db: 0

# â”€â”€ Atalhos de Teclado (Hotkeys) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Formato: https://github.com/boppreh/keyboard#keyboard.hotkey
# Modificadores: ctrl, alt, shift, win
# Teclas: a-z, 0-9, f1-f24, space, enter, esc, tab, etc.
  keys:
    # SessÃ£o
    iniciar_sessao:    ctrl+shift+n
    finalizar_sessao:  ctrl+shift+w
    status:            ctrl+shift+s

    # Ãudio
    gravar:            ctrl+g
    parar_gravar:      ctrl+shift+g
    pausar_gravar:     ctrl+shift+p

    # TranscriÃ§Ã£o
    transcrever:       ctrl+t
    resumir:           ctrl+r

    # Conhecimento
    salvar_conhecimento: ctrl+d

    # OS e E-mail
    fechar_os:         ctrl+o
    email_compra:      ctrl+e
    email_comunicado:  ctrl+shift+e

    # AprovaÃ§Ãµes
    listar_pendentes:  ctrl+p
    aprovar_tudo:      ctrl+a
    abrir_painel:      ctrl+shift+a

    # Busca
    buscar:            ctrl+f

    # Geral
    ajuda:             ctrl+h
    sair:              ctrl+c
```

---

## 4. JSON Schema (config.schema.yaml)

O schema valida o config.yaml antes de ser carregado pelo sistema.

```yaml
# config.schema.yaml
type: object
required: [hermes]
properties:
  hermes:
    type: object
    required: [daemon, obsidian, audio, transcription, llm]
    properties:
      log_level:
        type: string
        enum: [debug, info, warn, error]
      data_dir:
        type: string

      daemon:
        type: object
        properties:
          pipe_name: { type: string }
          request_timeout: { type: integer, minimum: 5 }

      obsidian:
        type: object
        required: [vault_path]
        properties:
          vault_path: { type: string }
          auto_backup: { type: boolean }
          backup_path: { type: string }

      audio:
        type: object
        properties:
          device: { type: ["null", "string", "integer"] }
          sample_rate: { type: integer, enum: [8000, 16000, 44100, 48000] }
          channels: { type: integer, enum: [1, 2] }
          format: { type: string, enum: [wav, mp3] }
          retention_days: { type: integer, minimum: 0 }
          noise_filter: { type: boolean }

      transcription:
        type: object
        properties:
          provider: { type: string, enum: [whisper_api, whisper_local] }
          model: { type: string }
          language: { type: string }
          timeout: { type: integer }

      llm:
        type: object
        required: [api_key]
        properties:
          provider: { type: string, enum: [anthropic, openai, google] }
          model: { type: string }
          api_key: { type: string, pattern: "^\\$\\{.+\\}$" }
          max_tokens: { type: integer, minimum: 1 }
          temperature: { type: number, minimum: 0, maximum: 2 }
          cache_ttl: { type: integer, minimum: 0 }

      movidesk:
        properties:
          base_url: { type: string }
          token: { type: string, pattern: "^\\$\\{.+\\}$" }
          rate_limit: { type: integer }

      email:
        properties:
          provider: { type: string, enum: [smtp, gmail, outlook] }
          from_name: { type: string }
          from_email: { type: string, format: email }
          smtp:
            type: object
            properties:
              host: { type: string }
              port: { type: integer }
              use_tls: { type: boolean }
              user: { type: string }
              password: { type: string }

      vector_store:
        properties:
          provider: { type: string, enum: [qdrant] }
          host: { type: string }
          port: { type: integer }
          collection_name: { type: string }
          embedding_size: { type: integer }

      postgresql:
        properties:
          host: { type: string }
          port: { type: integer }
          database: { type: string }
          user: { type: string }
          password: { type: string }

      redis:
        properties:
          host: { type: string }
          port: { type: integer }
          db: { type: integer }

      keys:
        type: object
        additionalProperties:
          type: string
```

---

## 5. ResoluÃ§Ã£o de Secrets

O Hermes suporta referÃªncias a variÃ¡veis de ambiente no formato `${NOME}` no config.yaml.

### Ordem de ResoluÃ§Ã£o

```
1. Verificar se o valor corresponde ao padrÃ£o ${NOME}
2. Tentar ler da variÃ¡vel de ambiente NOME
3. Se nÃ£o encontrar: tentar Windows Credential Manager (credential: NOME)
4. Se nÃ£o encontrar em nenhum lugar: erro de validaÃ§Ã£o
```

### Windows Credential Manager

Para maior seguranÃ§a, secrets podem ser armazenados no Credential Manager do Windows:

```powershell
# Adicionar secret
cmdkey /add:ANTHROPIC_API_KEY /user:hermes /pass:"sk-ant-..."

# Listar secrets
cmdkey /list
```

O Hermes busca no Credential Manager quando a variÃ¡vel de ambiente nÃ£o existe.

### Arquivo .env (fallback)

Um arquivo `~/.hermes/.env` pode ser usado como fallback (com `chmod 600` ou permissÃµes restritas).

---

## 6. Carregamento (Ordem de PrecedÃªncia)

```
1. Valores padrÃ£o (hardcoded no cÃ³digo)
2. config.yaml (~/.hermes/config.yaml)
3. HERMES_CONFIG (variÃ¡vel de ambiente apontando para config alternativo)
4. ResoluÃ§Ã£o de ${VARIAVEL}
```

**Priority:** valores mais especÃ­ficos sobrescrevem os mais genÃ©ricos.

---

## 7. Perfis de ConfiguraÃ§Ã£o (Multi-profile)

O Hermes suporta perfis para diferentes contextos de uso:

```bash
# Usar config padrÃ£o
hermes iniciar --chamado 12345

# Usar perfil "homolog" (testes)
hermes --profile homolog iniciar --chamado 12345
```

**Estrutura de perfis:**
```
~/.hermes/
â”œâ”€â”€ config.yaml              # Config principal (produÃ§Ã£o)
â”œâ”€â”€ config.homolog.yaml      # Perfil: homologaÃ§Ã£o
â”œâ”€â”€ config.test.yaml         # Perfil: testes (mocks, sem envio real)
â””â”€â”€ config.dev.yaml          # Perfil: desenvolvimento (verbose, debug)
```

Cada perfil sobrescreve apenas os campos que diferem do config principal.

> Ver [[04-Arquitetura/Seguranca.md|SeguranÃ§a]] para prÃ¡ticas de proteÃ§Ã£o de secrets.

---

## 8. Interface via CLI

O Hermes expÃµe comandos para gerenciar a configuraÃ§Ã£o:

```bash
# Abrir config no editor padrÃ£o
hermes config edit

# Exibir config atual (com secrets mascarados)
hermes config show

# Validar config.yaml
hermes config validate

# Exportar config para template
hermes config init
```

---

**Premissas:**
- O usuÃ¡rio edita o config.yaml manualmente (nÃ£o hÃ¡ wizard de configuraÃ§Ã£o).
- Secrets sÃ£o gerenciados fora do config.yaml (ambiente ou Credential Manager).

**Riscos:**
- Erro de sintaxe YAML pode travar o sistema na inicializaÃ§Ã£o (mitigado por schema validation + `hermes config validate`).
- UsuÃ¡rio pode esquecer de configurar uma integraÃ§Ã£o e sÃ³ descobrir no uso.

**PrÃ³ximos passos:**
- Criar [[04-Arquitetura/Operacao.md]] â€” ciclo de vida do sistema.
- Preparar config.yaml inicial para o MVP.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

