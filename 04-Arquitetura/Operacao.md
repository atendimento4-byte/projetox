---
title: "Operacao do Sistema"
description: "Windows Service, IPC via Named Pipe, 40+ comandos CLI"
status: "concluido"
---

# OperaÃ§Ã£o do Sistema

> **Ciclo de vida, instalaÃ§Ã£o, execuÃ§Ã£o, IPC, Windows Service e hotkeys globais.**

---

## 1. VisÃ£o Geral

O Hermes opera em dois processos distintos:

> Este modelo de operaÃ§Ã£o (Daemon + CLI) Ã© definido na [[04-Arquitetura/ADRs.md|ADR-009]]. A comunicaÃ§Ã£o via Named Pipe Ã© definida na [[04-Arquitetura/ADRs.md|ADR-012]].

| Processo | Nome | DescriÃ§Ã£o |
|----------|------|-----------|
| **Daemon** | `hermesd` | ServiÃ§o de background. MantÃ©m estado, gerencia Ã¡udio, hotkeys e fila de aprovaÃ§Ãµes. |
| **CLI** | `hermes` | Interface de linha de comando. Envia comandos ao daemon e exibe resultados. |

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”         IPC (Named Pipe)         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   hermes CLI  â”‚ â”€â”€â”€â”€ JSON Request/Response â”€â”€â”€â”€â–¶ â”‚   hermesd     â”‚
â”‚   (efÃªmero)   â”‚ â—€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚   (daemon)    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. InstalaÃ§Ã£o

### 2.1 â€” PrÃ©-requisitos

| DependÃªncia | VersÃ£o | Motivo |
|-------------|:------:|--------|
| Python | 3.12+ | Runtime |
| PostgreSQL | 16+ | Dados estruturados |
| Redis | 7+ | Cache e estado |
| Qdrant | 1.10+ | Banco vetorial |
| Docker (opcional) | â€” | Para rodar Qdrant, Redis, PostgreSQL |
| Git | â€” | Versionamento do vault Obsidian |

### 2.2 â€” InstalaÃ§Ã£o via pip

```bash
# Instalar o Hermes
pip install hermes

# Verificar instalaÃ§Ã£o
hermes --version
```

### 2.3 â€” InstalaÃ§Ã£o via PyInstaller (standalone)

```bash
# Build do executÃ¡vel
pip install pyinstaller
pyinstaller --onefile --name hermes hermes/main.py

# Distribuir o .exe
```

### 2.4 â€” Setup Inicial

```bash
# 1. Criar config padrÃ£o
hermes config init
# â†’ Cria ~/.hermes/config.yaml com valores padrÃ£o

# 2. Editar configuraÃ§Ã£o
hermes config edit
# â†’ Abre o config.yaml no editor padrÃ£o

# 3. Validar configuraÃ§Ã£o
hermes config validate
# â†’ Verifica schema e conectividade

# 4. Instalar o daemon como serviÃ§o Windows
hermesd install
# â†’ Registra como Windows Service

# 5. Iniciar o daemon
hermesd start
```

---

## 3. Ciclo de Vida do Daemon (hermesd)

### 3.1 â€” Como ServiÃ§o Windows

```bash
# Instalar
hermesd install

# Iniciar
hermesd start

# Parar
hermesd stop

# Status
hermesd status

# Desinstalar
hermesd uninstall
```

### 3.2 â€” Como Processo (modo debug)

```bash
# Rodar em primeiro plano (para debug)
hermesd run

# Rodar em background (Linux/WSL)
hermesd run &
```

### 3.3 â€” Startup Sequence (detalhada)

```
Fase 1 â€” Carregamento de Config
  [1] Localizar config.yaml (HERMES_CONFIG ou ~/.hermes/config.yaml)
  [2] Validar contra config.schema.yaml
  [3] Resolver ${VARIAVEL} (ambiente â†’ Credential Manager â†’ .env)
  [4] Mesclar com defaults do cÃ³digo

Fase 2 â€” InicializaÃ§Ã£o de Infraestrutura
  [5] Inicializar Logger (console + arquivo JSON)
  [6] Criar diretÃ³rios: logs, data/sessions, data/audio, backups
  [7] Conectar Redis (timeout: 3s)
  [8] Conectar PostgreSQL (timeout: 5s, rodar migrations)
  [9] Conectar Qdrant (timeout: 3s, criar collection se nÃ£o existir)

Fase 3 â€” Core Services
  [10] Inicializar EventBus
  [11] Criar DI Container:
       - Registrar EventBus (singleton)
       - Registrar Cache (Redis)
       - Registrar Database (PostgreSQL)
       - Registrar AudioRecorder (sounddevice)
       - Registrar Transcriber (Whisper)
       - Registrar LLM (Claude/GPT/Gemini)
       - Registrar Memory (Obsidian filesystem)
       - Registrar Movidesk (API)
       - Registrar Email (SMTP)
       - Registrar VectorStore (Qdrant)
  [12] Registrar Subscribers no EventBus:
       - Logger â†’ escuta todos os eventos
       - AuditLogger â†’ escuta eventos crÃ­ticos
       - ApprovalManager â†’ escuta *.suggested
       - SessionManager â†’ escuta session.*
       - CLI.notify â†’ escuta approval.pending (via IPC)

Fase 4 â€” RecuperaÃ§Ã£o
  [13] Verificar sessÃµes pendentes no estado anterior
  [14] Se havia sessÃ£o gravando: marcar como interrompida, notificar usuÃ¡rio
  [15] Se havia aÃ§Ãµes pendentes: reativar no ApprovalManager

Fase 5 â€” InÃ­cio das OperaÃ§Ãµes
  [16] Iniciar AudioRecorder (abrir microfone, buffer de Ã¡udio)
  [17] Iniciar IPC Server (Named Pipe: \\.\pipe\hermes)
  [18] Registrar Hotkeys Globais (keyboard library)
  [19] Publicar evento: system.started
  [20] Iniciar event loop principal (asyncio.run())

Tempo estimado total: < 3 segundos
```

### 3.4 â€” Shutdown Sequence

```
Fase 1 â€” Sinal de Parada
  [1] Receber sinal: Ctrl+C / SIGTERM / Service Stop
  [2] Publicar evento: system.shutting_down

Fase 2 â€” Parada Ordenada
  [3] Parar IPC Server (novas conexÃµes recusadas com "daemon shutting down")
  [4] Unregister Hotkeys Globais
  [5] Se sessÃ£o gravando: parar gravaÃ§Ã£o, salvar Ã¡udio parcial
  [6] Salvar estado pendente no disco (para recuperaÃ§Ã£o)
  [7] Aguardar tasks em andamento (timeout: 5s)

Fase 3 â€” FinalizaÃ§Ã£o
  [8] Fechar conexÃµes: Redis, PostgreSQL, Qdrant
  [9] Fechar arquivos de Ã¡udio e log
  [10] Publicar evento: system.stopped
  [11] Terminar processo

Tempo estimado total: < 2 segundos
```

---

## 4. Protocolo IPC (CLI â†” Daemon)

### 4.1 â€” Transporte

**Named Pipe:** `\\.\pipe\hermes`

- **Tipo:** Byte stream bidirecional
- **Formato:** Mensagens JSON delimitadas por `\n`
- **Timeout:** 30 segundos (configurÃ¡vel)

### 4.2 â€” Formato das Mensagens

**Request (CLI â†’ Daemon):**
```json
{
  "id": 1,
  "method": "session.start",
  "params": {
    "ticket_id": "12345"
  }
}
```

**Response (Daemon â†’ CLI):**
```json
{
  "id": 1,
  "result": {
    "session_id": "SES-001",
    "status": "active",
    "client": "Empresa ABC"
  }
}
```

**Error (Daemon â†’ CLI):**
```json
{
  "id": 1,
  "error": {
    "code": -32000,
    "message": "JÃ¡ existe uma sessÃ£o ativa (SES-001)",
    "data": {
      "session_id": "SES-001"
    }
  }
}
```

**Event (Daemon â†’ CLI, sem request):**
```json
{
  "event": "approval.pending",
  "data": {
    "count": 3,
    "actions": ["Salvar conhecimento", "Fechar OS", "Email de compra"]
  }
}
```

### 4.3 â€” CÃ³digos de Erro IPC

| CÃ³digo | Significado |
|:------:|-------------|
| -32700 | Parse error (JSON invÃ¡lido) |
| -32600 | Invalid request (formato errado) |
| -32601 | Method not found (comando nÃ£o existe) |
| -32602 | Invalid params (parÃ¢metros invÃ¡lidos) |
| -32000 | Daemon error |
| -32001 | Daemon not ready |
| -32002 | Session not found |

### 4.4 â€” MÃ©todos DisponÃ­veis

**SessÃ£o:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `session.start` | `ticket_id`, `client_name` | Iniciar acompanhamento |
| `session.end` | â€” | Finalizar sessÃ£o atual |
| `session.status` | â€” | Status da sessÃ£o atual |
| `session.info` | `session_id` | Detalhes de uma sessÃ£o |

**Ãudio:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `audio.record.start` | â€” | Iniciar gravaÃ§Ã£o |
| `audio.record.stop` | â€” | Parar gravaÃ§Ã£o |
| `audio.record.pause` | â€” | Pausar gravaÃ§Ã£o |
| `audio.record.resume` | â€” | Retomar gravaÃ§Ã£o |

**TranscriÃ§Ã£o:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `transcribe` | â€” | Transcrever Ã¡udio gravado |
| `summarize` | â€” | Gerar resumo da transcriÃ§Ã£o |

**Conhecimento:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `knowledge.save` | â€” | Sugerir registro no Obsidian |
| `knowledge.search` | `query` | Buscar na base de conhecimento |

**OS:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `os.suggest` | â€” | Sugerir fechamento de OS |
| `os.close` | `data` | Fechar OS (apÃ³s aprovaÃ§Ã£o) |

**E-mail:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `email.compra` | `materiais` | Gerar e-mail de solicitaÃ§Ã£o de compra |
| `email.comunicado` | `tipo` | Gerar e-mail de comunicado |

**AprovaÃ§Ãµes:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `approval.list` | â€” | Listar aÃ§Ãµes pendentes |
| `approval.decide` | `action_id`, `decision` | Aprovar/rejeitar/editar aÃ§Ã£o |

**Sistema:**
| MÃ©todo | ParÃ¢metros | DescriÃ§Ã£o |
|--------|------------|-----------|
| `system.ping` | â€” | Verificar se daemon estÃ¡ ativo |
| `system.status` | â€” | Status geral do sistema |
| `system.logs` | `level`, `limit` | Ãšltimos logs |
| `system.restart` | â€” | Reiniciar daemon |

---

## 5. Hotkeys Globais

### 5.1 â€” Funcionamento

As hotkeys sÃ£o registradas pelo daemon usando a biblioteca `keyboard` (Python).

- **Funcionam mesmo quando o terminal nÃ£o estÃ¡ em foco**
- **Capturadas globalmente** (qualquer aplicaÃ§Ã£o)
- **Convertidas em comandos internos** â†’ publicadas no EventBus

**LimitaÃ§Ã£o no Windows:** Se o Hermes nÃ£o estiver rodando como Administrador, algumas teclas podem nÃ£o ser capturadas em aplicativos elevados (UAC).

### 5.2 â€” Hotkeys PadrÃ£o

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ AÃ§Ã£o                â”‚ Atalho               â”‚ Comando                  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Iniciar SessÃ£o      â”‚ Ctrl + Shift + N     â”‚ session.start            â”‚
â”‚ Finalizar SessÃ£o    â”‚ Ctrl + Shift + W     â”‚ session.end              â”‚
â”‚ Status              â”‚ Ctrl + Shift + S     â”‚ session.status           â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Gravar              â”‚ Ctrl + G             â”‚ audio.record.start       â”‚
â”‚ Parar GravaÃ§Ã£o      â”‚ Ctrl + Shift + G     â”‚ audio.record.stop        â”‚
â”‚ Pausar/Retomar      â”‚ Ctrl + Shift + P     â”‚ audio.record.pause/resumeâ”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Transcrever         â”‚ Ctrl + T             â”‚ transcribe               â”‚
â”‚ Resumir             â”‚ Ctrl + R             â”‚ summarize                â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Salvar Conhecimento â”‚ Ctrl + D             â”‚ knowledge.save           â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Fechar OS           â”‚ Ctrl + O             â”‚ os.suggest               â”‚
â”‚ Email Compra        â”‚ Ctrl + E             â”‚ email.compra             â”‚
â”‚ Email Comunicado    â”‚ Ctrl + Shift + E     â”‚ email.comunicado         â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Pendentes           â”‚ Ctrl + P             â”‚ approval.list            â”‚
â”‚ Aprovar Tudo        â”‚ Ctrl + A             â”‚ approval.approve_all     â”‚
â”‚ Painel AprovaÃ§Ãµes   â”‚ Ctrl + Shift + A     â”‚ TUI pendÃªncias           â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Buscar              â”‚ Ctrl + F             â”‚ knowledge.search         â”‚
â”‚ Ajuda               â”‚ Ctrl + H             â”‚ ajuda                    â”‚
â”‚ Sair                â”‚ Ctrl + C             â”‚ system.shutdown          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 5.3 â€” CustomizaÃ§Ã£o

Todas as hotkeys sÃ£o configurÃ¡veis no `config.yaml`:

```yaml
keys:
  gravar: ctrl+g
  transcrever: ctrl+t
  # ...
```

### 5.4 â€” Feedback Visual

Quando uma hotkey Ã© acionada:

| SituaÃ§Ã£o | Feedback |
|----------|----------|
| Comando executado | NotificaÃ§Ã£o Windows (toast) + log |
| Comando ignorado (sem sessÃ£o) | NotificaÃ§Ã£o "Nenhuma sessÃ£o ativa" |
| Erro | NotificaÃ§Ã£o "Erro: ..." |

---

## 6. Comandos CLI (hermes)

### 6.1 â€” SessÃ£o

```bash
hermes iniciar --chamado 12345
hermes iniciar --cliente "Empresa ABC" --avulso    # Sem chamado

hermes finalizar

hermes status
```

### 6.2 â€” Ãudio

```bash
hermes gravar          # Iniciar gravaÃ§Ã£o (com confirmaÃ§Ã£o)
hermes parar           # Parar gravaÃ§Ã£o
hermes pausar          # Pausar
hermes retomar         # Retomar
```

### 6.3 â€” TranscriÃ§Ã£o

```bash
hermes transcrever     # Transcrever Ã¡udio gravado
hermes resumir         # Gerar resumo estruturado
```

### 6.4 â€” Conhecimento

```bash
hermes salvar          # Sugerir registro no Obsidian
hermes buscar "senha padrÃ£o mikrotik"   # Buscar na base
```

### 6.5 â€” OS

```bash
hermes fechar          # Sugerir fechamento de OS
```

### 6.6 â€” E-mail

```bash
hermes email-compra "Cabo de rede CAT6 10m"
hermes email-comunicado --tipo interno
hermes email-comunicado --tipo externo
```

### 6.7 â€” AprovaÃ§Ãµes

```bash
hermes pendentes       # Listar aÃ§Ãµes pendentes
hermes aprovar --tudo  # Aprovar todas
hermes aprovar abc123  # Aprovar aÃ§Ã£o especÃ­fica
hermes rejeitar abc123 # Rejeitar
hermes editar abc123   # Editar antes de executar
```

### 6.8 â€” ConfiguraÃ§Ã£o

```bash
hermes config init     # Criar config.yaml padrÃ£o
hermes config edit     # Abrir no editor
hermes config show     # Exibir config (secrets mascarados)
hermes config validate # Validar config.yaml
```

### 6.9 â€” Daemon

```bash
hermesd install        # Instalar serviÃ§o Windows
hermesd uninstall      # Desinstalar
hermesd start          # Iniciar daemon
hermesd stop           # Parar daemon
hermesd restart        # Reiniciar
hermesd status         # Status do daemon
hermesd logs           # Ãšltimos logs
```

---

## 7. TUI (Modo Interativo)

> **PÃ³s-MVP.** Uma TUI (Terminal UI) baseada em Textual serÃ¡ disponibilizada como modo alternativo de interaÃ§Ã£o.

```bash
hermes tui    # â†’ Abre dashboard interativo
```

A TUI exibirÃ¡:
- Status da sessÃ£o atual (em tempo real)
- Indicador de gravaÃ§Ã£o
- PendÃªncias com opÃ§Ãµes de aÃ§Ã£o rÃ¡pida
- HistÃ³rico de eventos recentes
- Campo de busca

---

## 8. Monitoramento

### 8.1 â€” Health Check

```bash
hermesd status
# â†’ Daemon: RUNNING (PID: 1234, uptime: 2h 15m)
# â†’ SessÃ£o: ACTIVE (SES-001, cliente: Empresa ABC)
# â†’ GravaÃ§Ã£o: RECORDING (00:03:42)
# â†’ PendÃªncias: 3
# â†’ Redis: OK (0.2ms)
# â†’ PostgreSQL: OK (1.1ms)
# â†’ Qdrant: OK (0.8ms)
```

### 8.2 â€” Logs

```bash
# Ãšltimos logs do daemon
hermesd logs --level warn --limit 20

# Logs em tempo real
hermesd logs --follow

# Logs de uma sessÃ£o especÃ­fica
hermesd logs --session SES-001
```

---

## 9. ExpansÃ£o Futura: Acesso Remoto via TCP

> **ImplementaÃ§Ã£o pÃ³s-MVP.** O MVP usa Named Pipe (apenas local). Esta seÃ§Ã£o documenta o plano para acesso via rede.
>
> A estratÃ©gia de expansÃ£o para rede estÃ¡ documentada na [[04-Arquitetura/ADRs.md|ADR-014]].

### 9.1 â€” AbstraÃ§Ã£o de Transporte

O transporte IPC serÃ¡ abstraÃ­do por trÃ¡s da interface `ITransport`:

```python
# core/ports/i_transport.py
class ITransport(ABC):
    async def connect(self) -> None
    async def send_request(self, method: str, params: dict) -> dict
    async def disconnect(self) -> None
    async def on_event(self, handler: Callable) -> None
```

**ImplementaÃ§Ãµes:**
| Adapter | LocalizaÃ§Ã£o | Quando |
|---------|-------------|--------|
| `NamedPipeTransport` | `adapters/transport/named_pipe.py` | MVP (padrÃ£o) |
| `TcpTransport` | `adapters/transport/tcp_socket.py` | PÃ³s-MVP |

### 9.2 â€” CenÃ¡rio VPN

```
MÃ¡quina A (VPN: 10.0.0.1)          MÃ¡quina B (VPN: 10.0.0.2)
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  hermesd (daemon)    â”‚â—€â”€â”€TCPâ”€â”€â–¶â”‚  hermes CLI          â”‚
â”‚  0.0.0.0:8790        â”‚  TLS    â”‚  --server 10.0.0.1:8790
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚          â”‚                      â”‚
â”‚  â”‚ Ãudio capturadoâ”‚  â”‚          â”‚  Sem Ã¡udio local     â”‚
â”‚  â”‚ aqui (sempre)  â”‚  â”‚          â”‚  (desafio futuro)    â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚          â”‚                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**O que funciona remotamente:**
- âœ… Comandos de sessÃ£o (iniciar, finalizar, status)
- âœ… TranscriÃ§Ã£o e resumo
- âœ… Registro no Obsidian
- âœ… AprovaÃ§Ãµes
- âœ… GeraÃ§Ã£o de e-mail e fechamento de OS
- âœ… Busca na base de conhecimento

**O que NÃƒO funciona (desafio):**
- âŒ Captura de Ã¡udio da mÃ¡quina remota (microfone do CLI)
- âŒ Hotkeys globais (sÃ³ funcionam na mÃ¡quina do daemon)

### 9.3 â€” ConfiguraÃ§Ã£o Futura

```yaml
# config.yaml (futuro)
hermes:
  daemon:
    transport: named_pipe   # named_pipe | tcp
    tcp:
      host: 0.0.0.0
      port: 8790
      tls_enabled: true
      tls_cert: ~/.hermes/certs/server.crt
      tls_key: ~/.hermes/certs/server.key
    auth_token: ${HERMES_AUTH_TOKEN}  # para conexÃµes remotas
```

### 9.4 â€” ConsideraÃ§Ãµes de SeguranÃ§a

| Aspecto | Named Pipe | TCP |
|---------|------------|-----|
| AutenticaÃ§Ã£o | SO (usuÃ¡rio logado) | Token JWT |
| Criptografia | NÃ£o precisa | TLS obrigatÃ³rio |
| Firewall | N/A | Porta 8790 liberada na VPN |
| Acesso | Apenas local | IPs autorizados na VPN |

### 9.5 â€” Nota sobre Ãudio Remoto

O Ã¡udio Ã© capturado **sempre na mÃ¡quina do daemon**. Capturar Ã¡udio de uma mÃ¡quina remota e enviar para o daemon processar Ã© um **desafio tÃ©cnico conhecido** e serÃ¡ tratado separadamente, quando houver demanda concreta. PossÃ­veis abordagens futuras:

- Streaming de Ã¡udio via WebSocket
- Envio de arquivo de Ã¡udio como comando (ex.: `hermes transcrever --arquivo C:/temp/audio.wav`)
- WebRTC para captura remota

---

**Premissas:**
- O Hermes serÃ¡ instalado em ambiente Windows com Python 3.12+.
- O daemon roda como Windows Service para garantir disponibilidade 24/7.

**Riscos:**
- Hotkeys globais podem conflitar com outros aplicativos (mitigado por customizaÃ§Ã£o).
- Windows Service tem peculiaridades de permissÃ£o (instalaÃ§Ã£o requer Admin).

**PrÃ³ximos passos:**
- Atualizar [[04-Arquitetura/Componentes.md]] com implementaÃ§Ã£o concreta de cada componente.
- Iniciar Sprint 0 (setup do projeto, estrutura de cÃ³digo).

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

