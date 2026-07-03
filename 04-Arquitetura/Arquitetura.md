---
title: "Arquitetura Geral"
description: "Arquitetura hexagonal (Ports & Adapters)"
status: "concluido"
---

# Arquitetura Geral

> **VisÃ£o arquitetural completa do sistema: estilo, processos, concorrÃªncia, startup, erros e logging.**

---

## 1. Estilo Arquitetural

O sistema adota **Arquitetura Hexagonal (Ports & Adapters)** com **Orquestrador Central (Hermes)** e **Event Bus interno**.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         INTERFACE DO USUÃRIO                              â”‚
â”‚               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”           â”‚
â”‚               â”‚   hermes (CLI)       â”‚  â”‚  hermes tui (TUI)  â”‚           â”‚
â”‚               â”‚  Typer + Rich        â”‚  â”‚  Textual           â”‚           â”‚
â”‚               â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜           â”‚
â”‚                        â”‚ IPC (Named Pipe)        â”‚ IPC                    â”‚
â”‚                        â–¼                          â–¼                       â”‚
â”‚               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”               â”‚
â”‚               â”‚         hermesd (Daemon)                  â”‚               â”‚
â”‚               â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚               â”‚
â”‚               â”‚  â”‚          IPC Server                â”‚  â”‚               â”‚
â”‚               â”‚  â”‚   (Named Pipe: \\.\pipe\hermes)     â”‚  â”‚               â”‚
â”‚               â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚               â”‚
â”‚               â”‚                 â”‚                         â”‚               â”‚
â”‚               â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚               â”‚
â”‚               â”‚  â”‚         DI Container               â”‚  â”‚               â”‚
â”‚               â”‚  â”‚   (composition root)               â”‚  â”‚               â”‚
â”‚               â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚               â”‚
â”‚               â”‚                 â”‚                         â”‚               â”‚
â”‚               â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚               â”‚
â”‚               â”‚  â”‚            CORE (DOMAIN)            â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Session    â”‚ â”‚ Workflow       â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Manager    â”‚ â”‚ Engine         â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Approval   â”‚ â”‚ Context        â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Manager    â”‚ â”‚ Manager        â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Audit      â”‚ â”‚ Event Bus      â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â”‚ Logger     â”‚ â”‚ (pub/sub)      â”‚ â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚  â”‚               â”‚
â”‚               â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚               â”‚
â”‚               â”‚                 â”‚                         â”‚               â”‚
â”‚               â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚               â”‚
â”‚               â”‚  â”‚         PORTS (INTERFACES)          â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  [IAudio] [ITranscriber] [ILLM]     â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  [IMemory] [IMovidesk] [IEmail]     â”‚  â”‚               â”‚
â”‚               â”‚  â”‚  [IVectorStore] [ICache] [IDB]      â”‚  â”‚               â”‚
â”‚               â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚               â”‚
â”‚               â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜               â”‚
â”‚                                 â”‚                                        â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚                         ADAPTERS (INFRA)                            â”‚â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚â”‚
â”‚  â”‚  â”‚ Audio    â”‚ â”‚ Whisper  â”‚ â”‚ LLM      â”‚ â”‚ Obsidian â”‚ â”‚ Movidesk â”‚  â”‚â”‚
â”‚  â”‚  â”‚ Recorder â”‚ â”‚ API/Localâ”‚ â”‚ Anthropicâ”‚ â”‚ Adapter  â”‚ â”‚ API      â”‚  â”‚â”‚
â”‚  â”‚  â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤ â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤  â”‚â”‚
â”‚  â”‚  â”‚ SMTP     â”‚ â”‚ Qdrant   â”‚ â”‚ Redis    â”‚ â”‚ PostgreSQLâ”‚ â”‚          â”‚  â”‚â”‚
â”‚  â”‚  â”‚ Email    â”‚ â”‚ Adapter  â”‚ â”‚ Cache    â”‚ â”‚ Database â”‚ â”‚          â”‚  â”‚â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 2. Arquitetura de Processos

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                          COMPUTADOR DO USUÃRIO                          â”‚
â”‚                                                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                                       â”‚
â”‚  â”‚   hermesd (Daemon Process)   â”‚  â† Processo principal                 â”‚
â”‚  â”‚                              â”‚     (Windows Service)                  â”‚
â”‚  â”‚  PID: 1234                   â”‚                                       â”‚
â”‚  â”‚  MemÃ³ria: ~80MB             â”‚                                       â”‚
â”‚  â”‚  Threads: 5+3 (pool)        â”‚                                       â”‚
â”‚  â”‚                              â”‚                                       â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚                                       â”‚
â”‚  â”‚  â”‚  asyncio Event Loop    â”‚  â”‚                                       â”‚
â”‚  â”‚  â”‚  â”œâ”€ IPC Server Task    â”‚  â”‚  â† Escuta comandos do CLI            â”‚
â”‚  â”‚  â”‚  â”œâ”€ Hotkey Task        â”‚  â”‚  â† Monitora teclas globais            â”‚
â”‚  â”‚  â”‚  â”œâ”€ Event Bus Task     â”‚  â”‚  â† Distribui eventos                 â”‚
â”‚  â”‚  â”‚  â”œâ”€ Audio Monitor Task â”‚  â”‚  â† Buffer de Ã¡udio                   â”‚
â”‚  â”‚  â”‚  â””â”€ Pending Check Task â”‚  â”‚  â† Verifica pendÃªncias periÃ³dicamenteâ”‚
â”‚  â”‚  â”‚                        â”‚  â”‚                                       â”‚
â”‚  â”‚  â”‚  ThreadPool (4 workers)â”‚  â”‚  â† I/O bloqueante                     â”‚
â”‚  â”‚  â”‚  â”œâ”€ Whisper Local      â”‚  â”‚                                       â”‚
â”‚  â”‚  â”‚  â”œâ”€ LLM API Calls      â”‚  â”‚                                       â”‚
â”‚  â”‚  â”‚  â””â”€ File Operations    â”‚  â”‚                                       â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚                                       â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                                       â”‚
â”‚                 â”‚                                                        â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                                       â”‚
â”‚  â”‚   hermes (CLI Process)       â”‚  â† Processo temporÃ¡rio                â”‚
â”‚  â”‚                              â”‚     (inicia, executa, termina)         â”‚
â”‚  â”‚  PID: 5678                   â”‚                                       â”‚
â”‚  â”‚  DuraÃ§Ã£o: ~500ms             â”‚                                       â”‚
â”‚  â”‚  MemÃ³ria: ~15MB             â”‚                                       â”‚
â”‚  â”‚                              â”‚                                       â”‚
â”‚  â”‚  1. LÃª config.yaml           â”‚                                       â”‚
â”‚  â”‚  2. Conecta ao Named Pipe    â”‚                                       â”‚
â”‚  â”‚  3. Envia comando JSON       â”‚                                       â”‚
â”‚  â”‚  4. Aguarda resposta         â”‚                                       â”‚
â”‚  â”‚  5. Exibe resultado (Rich)   â”‚                                       â”‚
â”‚  â”‚  6. Termina                  â”‚                                       â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                                       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Protocolo IPC (JSON sobre Named Pipe)

```
Request:  {"id": 1, "method": "session.start", "params": {"ticket": "12345"}}
Response: {"id": 1, "result": {"session_id": "SES-001", "status": "active"}}

Event:    {"event": "session.started", "data": {"session_id": "SES-001"}}

Error:    {"id": 1, "error": {"code": -32000, "message": "Session already active"}}
```

---

## 3. MÃ¡quina de Estados

### SessÃ£o de Acompanhamento

```
     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â”‚  created  â”‚
     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜
          â”‚ iniciar()
          â–¼
     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â”‚  active   â”‚â—€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜                    â”‚
          â”‚ gravar()                  â”‚
     â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”   pausar()    â”Œâ”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”
     â”‚ recordingâ”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶â”‚   paused   â”‚
     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜â—€â”€â”€retomar()â”€â”€â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
          â”‚                         â”‚
          â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚ parar()
                 â–¼
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â”‚ completed â”‚
          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**TransiÃ§Ãµes e regras:**
| Estado | AÃ§Ã£o | PrÃ³ximo estado | ValidaÃ§Ã£o |
|--------|------|---------------|-----------|
| `created` | `iniciar()` | `active` | NÃ£o pode haver outra sessÃ£o ativa |
| `active` | `gravar()` | `recording` | Microfone disponÃ­vel |
| `recording` | `pausar()` | `paused` | â€” |
| `paused` | `retomar()` | `recording` | â€” |
| `recording` | `parar()` | `completed` | Ãudio salvo |
| `active` | `finalizar()` | `completed` | â€” |
| `*` | `cancelar()` | `cancelled` | â€” |

### AÃ§Ã£o Pendente (PendingAction)

```
  created â”€â”€â–¶ pending â”€â”€â–¶ approved â”€â”€â–¶ executing â”€â”€â–¶ done
                           â”‚
                           â”œâ”€â”€ rejected â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶ done
                           â”‚
                           â””â”€â”€ snoozed â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶ pending (reativada)
```

**AÃ§Ãµes que geram pendÃªncias:**
| AÃ§Ã£o | Prioridade padrÃ£o | TTL |
|------|:-----------------:|:---:|
| Registrar conhecimento no Obsidian | MÃ©dia | 24h |
| Fechar OS (status) | Alta | 4h |
| Enviar e-mail de compra | Alta | 4h |
| Enviar e-mail de comunicado | MÃ©dia | 8h |

---

## 4. Modelo de ConcorrÃªncia

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                       asyncio Event Loop                             â”‚
â”‚                                                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚  Task 1: IPC Server                                             â”‚â”‚
â”‚  â”‚  Escuta Named Pipe, recebe requisiÃ§Ãµes JSON,                    â”‚â”‚
â”‚  â”‚  roteia para o handler adequado, retorna resposta               â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â”‚                                                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚  Task 2: Hotkey Listener                                        â”‚â”‚
â”‚  â”‚  Registra hotkeys globais (keyboard library),                   â”‚â”‚
â”‚  â”‚  converte tecla em comando, publica no Event Bus                â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â”‚                                                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚  Task 3: Event Bus Dispatcher                                   â”‚â”‚
â”‚  â”‚  Distribui eventos para subscribers registrados                 â”‚â”‚
â”‚  â”‚  Executa callbacks de forma assÃ­ncrona                          â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â”‚                                                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚  Task 4: Pending Action Monitor                                 â”‚â”‚
â”‚  â”‚  A cada 5min, verifica aÃ§Ãµes pendentes prÃ³ximas do TTL          â”‚â”‚
â”‚  â”‚  Publica evento approval.expiring se necessÃ¡rio                 â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â”‚                                                                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”â”‚
â”‚  â”‚  ThreadPoolExecutor (max_workers=4)                              â”‚â”‚
â”‚  â”‚                                                                  â”‚â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â” â”‚â”‚
â”‚  â”‚  â”‚ Whisper Localâ”‚ â”‚ LLM API Call â”‚ â”‚ Obsidian     â”‚ â”‚ File   â”‚ â”‚â”‚
â”‚  â”‚  â”‚ (CPU-bound)  â”‚ â”‚ (I/O-bound)  â”‚ â”‚ Write (I/O)  â”‚ â”‚ I/O    â”‚ â”‚â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Regras de concorrÃªncia:**
- **AudioRecorder**: thread separada (nÃ£o pode ter latÃªncia), comunicaÃ§Ã£o via asyncio.Queue
- **Event Bus**: callbacks executados em asyncio Tasks (nÃ£o bloqueiam o publisher)
- **BD/Redis**: asyncio com drivers nativos (asyncpg, redis-py async)
- **Arquivos**: ThreadPool para evitar bloqueio do event loop
- **Locks**: asyncio.Lock para sessÃ£o (apenas 1 comando de sessÃ£o por vez)

---

## 5. Startup Sequence

```
1. Carregar config.yaml
2. Validar contra config.schema.yaml
3. Resolver ${VAR} (ambiente / Credential Manager)
4. Inicializar Logger (console + arquivo JSON)
5. Criar diretÃ³rios de dados (~/.hermes/data, ~/.hermes/logs)
6. Inicializar EventBus
7. Conectar Redis (se configurado)
8. Conectar PostgreSQL (rodar migrations se necessÃ¡rio)
9. Conectar Qdrant (verificar collections)
10. Criar DI Container (composiÃ§Ã£o)
11. Recuperar sessÃµes pendentes (estava gravando quando caiu?)
12. Inicializar AudioRecorder (abrir microfone)
13. Iniciar IPC Server (Named Pipe)
14. Registrar Hotkeys Globais
15. Publicar evento: system.started
16. Iniciar event loop (asyncio.run())

Tempo estimado: < 3 segundos
```

---

## 6. Shutdown Sequence

```
1. Sinal de parada (Ctrl+C / SIGTERM / Service Stop)
2. Pausar IPC Server (novos comandos rejeitados)
3. Publicar evento: system.shutting_down
4. Se sessÃ£o gravando: parar gravaÃ§Ã£o, salvar Ã¡udio parcial
5. Salvar estado pendente (para recuperaÃ§Ã£o na prÃ³xima inicializaÃ§Ã£o)
6. Aguardar tasks em andamento (timeout: 5s)
7. Fechar conexÃµes (Redis, PostgreSQL, Qdrant)
8. Fechar arquivos de log
9. Terminar

Tempo estimado: < 2 segundos
```

---

## 7. Hierarquia de Erros e Tratamento

```
HermesError (base)
â”œâ”€â”€ ConfigError
â”‚   â”œâ”€â”€ ConfigNotFoundError        (~/.hermes/config.yaml nÃ£o existe)
â”‚   â””â”€â”€ ConfigValidationError      (schema invÃ¡lido, campo obrigatÃ³rio faltando)
â”œâ”€â”€ SessionError
â”‚   â”œâ”€â”€ SessionNotFoundError       (session_id nÃ£o existe)
â”‚   â”œâ”€â”€ SessionStateError          (aÃ§Ã£o invÃ¡lida para o estado atual)
â”‚   â””â”€â”€ SessionAlreadyActiveError  (tentou iniciar com sessÃ£o ativa)
â”œâ”€â”€ AudioError
â”‚   â”œâ”€â”€ RecordingError             (falha ao gravar)
â”‚   â”œâ”€â”€ DeviceNotFoundError        (microfone nÃ£o encontrado)
â”‚   â””â”€â”€ DeviceBusyError            (microfone em uso por outro app)
â”œâ”€â”€ TranscriptionError
â”‚   â”œâ”€â”€ WhisperAPIError            (API retornou erro)
â”‚   â”œâ”€â”€ WhisperLocalError          (whisper.cpp falhou)
â”‚   â””â”€â”€ AudioCorruptedError       (Ã¡udio invÃ¡lido ou corrompido)
â”œâ”€â”€ LLMError
â”‚   â”œâ”€â”€ LLMAPIError                (LLM API retornou erro HTTP)
â”‚   â”œâ”€â”€ LLMRateLimitError          (rate limit atingido)
â”‚   â””â”€â”€ LLMContextLengthError      (contexto excedeu limite de tokens)
â”œâ”€â”€ MemoryError
â”‚   â”œâ”€â”€ ObsidianWriteError         (falha ao escrever nota)
â”‚   â”œâ”€â”€ ObsidianReadError          (falha ao ler nota)
â”‚   â””â”€â”€ NoteNotFoundError          (nota requisitada nÃ£o existe)
â”œâ”€â”€ IntegrationError
â”‚   â”œâ”€â”€ MovideskError
â”‚   â”‚   â”œâ”€â”€ MovideskAuthError      (token invÃ¡lido/expirado)
â”‚   â”‚   â”œâ”€â”€ MovideskTimeoutError   (timeout de rede)
â”‚   â”‚   â””â”€â”€ MovideskNotFoundError  (chamado nÃ£o encontrado)
â”‚   â”œâ”€â”€ EmailError
â”‚   â”‚   â”œâ”€â”€ EmailAuthError         (credenciais invÃ¡lidas)
â”‚   â”‚   â””â”€â”€ EmailSendError         (falha ao enviar)
â”‚   â””â”€â”€ VectorStoreError
â”‚       â”œâ”€â”€ QdrantConnectionError  (Qdrant offline)
â”‚       â””â”€â”€ EmbeddingError         (falha ao gerar embedding)
â”œâ”€â”€ ApprovalError
â”‚   â”œâ”€â”€ ActionNotFoundError        (aÃ§Ã£o de aprovaÃ§Ã£o nÃ£o encontrada)
â”‚   â””â”€â”€ ActionExpiredError         (aÃ§Ã£o expirou sem decisÃ£o)
â””â”€â”€ IPCError
    â”œâ”€â”€ PipeConnectionError        (falha ao conectar ao daemon)
    â”œâ”€â”€ PipeTimeoutError           (daemon nÃ£o respondeu)
    â””â”€â”€ DaemonNotRunningError      (daemon nÃ£o estÃ¡ rodando)
```

### PolÃ­ticas de Retry

| OperaÃ§Ã£o | Tentativas | Backoff | Timeout |
|----------|:----------:|---------|:-------:|
| LLM API | 3 | Exponencial (1s, 2s, 4s) | 30s |
| Whisper API | 2 | Exponencial (2s, 4s) | 60s |
| Movidesk API | 3 | Exponencial (1s, 2s, 4s) | 15s |
| Qdrant | 3 | Exponencial (500ms, 1s, 2s) | 5s |
| Redis | 2 | Exponencial (500ms, 1s) | 3s |
| Obsidian write | 1 | â€” (falha notifica usuÃ¡rio) | 2s |
| Email send | 2 | Exponencial (1s, 3s) | 10s |

---

## 8. Logging Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         Logger (estruturado)                        â”‚
â”‚                                                                     â”‚
â”‚  Handler 1: Console (Rich)                                          â”‚
â”‚  - NÃ­vel: INFO+                                                     â”‚
â”‚  - Formato: colorido, human-readable                                â”‚
â”‚  - Exemplo:                                                         â”‚
â”‚    [14:30:00] âœ… SessÃ£o #SES-001 iniciada (Chamado: 12345)         â”‚
â”‚    [14:30:05] âº GravaÃ§Ã£o iniciada                                   â”‚
â”‚                                                                     â”‚
â”‚  Handler 2: Arquivo JSON (~/.hermes/logs/hermes.json)               â”‚
â”‚  - NÃ­vel: DEBUG+                                                    â”‚
â”‚  - Formato: JSON por linha (NDJSON)                                 â”‚
â”‚  - Exemplo:                                                         â”‚
â”‚    {"t":"2026-07-02T14:30:00.123Z","l":"INFO",                      â”‚
â”‚     "m":"session.started","s":"SES-001",                            â”‚
â”‚     "d":{"ticket":"12345"},"c":"corr-abc"}                          â”‚
â”‚                                                                     â”‚
â”‚  Handler 3: Auditoria (PostgreSQL)                                  â”‚
â”‚  - NÃ­vel: AUDIT (nÃ­vel custom)                                      â”‚
â”‚  - Eventos crÃ­ticos: gravaÃ§Ã£o, envio de email, fechamento OS        â”‚
â”‚  - Append-only (imutÃ¡vel)                                           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Campos do JSON:**
| Campo | DescriÃ§Ã£o |
|-------|-----------|
| `t` | Timestamp ISO 8601 |
| `l` | Level (DEBUG, INFO, WARN, ERROR, AUDIT) |
| `m` | Mensagem / nome do evento |
| `s` | Session ID (se aplicÃ¡vel) |
| `d` | Dados estruturados do evento |
| `c` | Correlation ID (rastreio de chain de eventos) |
| `e` | Error trace (se houver) |

---

## 9. PadrÃµes Arquiteturais

> Ver [[04-Arquitetura/ADRs.md|ADRs]] para a fundamentaÃ§Ã£o de cada padrÃ£o.

| PadrÃ£o | Onde | AplicaÃ§Ã£o |
|--------|------|-----------|
| **[[04-Arquitetura/ADRs.md\|Ports & Adapters]]** | Toda a periferia do Core | `core/ports/` define interfaces; `adapters/` implementa |
| **Event Bus (pub/sub)** | ComunicaÃ§Ã£o entre mÃ³dulos | `core/event_bus.py` â€” mÃ³dulos publicam e subscrevem |
| **Composition Root** | InicializaÃ§Ã£o | `container.py` â€” ponto Ãºnico de wiring de dependÃªncias |
| **Repository** | Acesso a BD/Redis | Abstrai PostgreSQL, Redis, Qdrant atrÃ¡s de interfaces |
| **Strategy** | LLM providers | Container escolhe implementaÃ§Ã£o baseada na config |
| **State Machine** | SessÃµes e aÃ§Ãµes | `core/session.py` â€” estados e transiÃ§Ãµes formais |
| **Saga / Workflow** | Fluxos de atendimento | `core/workflow.py` â€” sequÃªncia de passos com rollback |
| **CQRS** | Leitura/escrita no Obsidian | Escrita via MemoryAdapter; leitura via VectorStore + filesystem |

---

## 10. Stack TecnolÃ³gica Final

| Camada | Tecnologia | VersÃ£o | FunÃ§Ã£o |
|--------|------------|:------:|--------|
| **Linguagem** | Python | 3.12+ | Desenvolvimento do core |
| **CLI Framework** | Typer + Rich | â€” | Interface de linha de comando |
| **TUI (futuro)** | Textual | â€” | Dashboard interativo (pÃ³s-MVP) |
| **Daemon** | pywin32 (Windows Service) | â€” | ServiÃ§o de background |
| **Config** | PyYAML + JSON Schema | â€” | ConfiguraÃ§Ã£o centralizada |
| **Event Bus** | asyncio (pub/sub interno) | â€” | ComunicaÃ§Ã£o entre mÃ³dulos |
| **IPC** | Named Pipes (win32pipe) | â€” | ComunicaÃ§Ã£o CLI â†” Daemon |
| **Hotkeys** | keyboard (Python lib) | â€” | Atalhos globais |
| **Ãudio** | sounddevice | â€” | Captura de Ã¡udio |
| **TranscriÃ§Ã£o** | openai-whisper (API/Local) | â€” | Ãudio â†’ texto |
| **LLM** | anthropic / openai SDK | â€” | GeraÃ§Ã£o e anÃ¡lise |
| **Banco Relacional** | PostgreSQL + asyncpg | â€” | Dados estruturados |
| **Cache / Estado** | Redis + redis-py async | â€” | SessÃµes e cache |
| **Banco Vetorial** | Qdrant + qdrant-client | â€” | Busca semÃ¢ntica |
| **Obsidian** | Acesso filesystem (.md) | â€” | MemÃ³ria persistente |
| **E-mail** | aiosmtplib / API Gmail | â€” | Envio de e-mails |
| **AutomaÃ§Ã£o (futuro)** | n8n (Docker) | â€” | Workflows de integraÃ§Ã£o |
| **API Web (futuro)** | FastAPI | â€” | Endpoints REST |
| **Testes** | pytest + pytest-asyncio | â€” | Testes automatizados |

> As decisÃµes sobre cada tecnologia estÃ£o documentadas nas [[04-Arquitetura/ADRs.md|ADRs]].

---

## 11. Diagrama de Pacotes (CÃ³digo)

```
hermes/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ hermes/                     # Package principal
â”‚   â”‚   â”œâ”€â”€ __main__.py             # Ponto de entrada (CLI ou daemon)
â”‚   â”‚   â”œâ”€â”€ _app.py                 # Composition Root + DI container
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ compartilhado/          # CÃ³digo compartilhado (zero dep. externa)
â”‚   â”‚   â”‚   â”œâ”€â”€ base_entidade.py
â”‚   â”‚   â”‚   â”œâ”€â”€ base_objeto_valor.py
â”‚   â”‚   â”‚   â”œâ”€â”€ base_agregado.py
â”‚   â”‚   â”‚   â”œâ”€â”€ evento_dominio.py
â”‚   â”‚   â”‚   â”œâ”€â”€ gerenciador_sessao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ motor_fluxo_trabalho.py
â”‚   â”‚   â”‚   â”œâ”€â”€ gerenciador_aprovacao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ registrador_auditoria.py
â”‚   â”‚   â”‚   â”œâ”€â”€ gerenciador_contexto.py
â”‚   â”‚   â”‚   â”œâ”€â”€ barramento_eventos/
â”‚   â”‚   â”‚   â”œâ”€â”€ erros/              # Resultado[T,E] + hierarquia
â”‚   â”‚   â”‚   â”œâ”€â”€ logging/
â”‚   â”‚   â”‚   â””â”€â”€ util/
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ contexto/               # Bounded Contexts
â”‚   â”‚   â”‚   â”œâ”€â”€ acompanhamento/     # Acompanhamento de chamados
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/        # Entidades, VOs, eventos, repositÃ³rios
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/      # Casos de uso
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/     # Adaptadores (Postgres)
â”‚   â”‚   â”‚   â”œâ”€â”€ audio/              # GravaÃ§Ã£o e transcriÃ§Ã£o
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/     # Gravador, transcritor (Whisper)
â”‚   â”‚   â”‚   â”œâ”€â”€ memoria/            # Obsidian + Qdrant
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/     # Vault, banco_vetorial
â”‚   â”‚   â”‚   â”œâ”€â”€ comunicacao/        # E-mail e comunicaÃ§Ãµes
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚   â”‚   â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ integracao/     # SMTP, templates
â”‚   â”‚   â”‚   â””â”€â”€ integracao/         # IntegraÃ§Ãµes externas
â”‚   â”‚   â”‚       â”œâ”€â”€ dominio/
â”‚   â”‚   â”‚       â”œâ”€â”€ aplicacao/
â”‚   â”‚   â”‚       â””â”€â”€ integracao/     # Movidesk, n8n
â”‚   â”‚   â”‚
â”‚   â”‚   â”œâ”€â”€ agentes/                # Agentes de IA (cross-context)
â”‚   â”‚   â”‚   â”œâ”€â”€ base_agente.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_transcricao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_memoria.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_documentacao.py
â”‚   â”‚   â”‚   â”œâ”€â”€ agente_comunicacao.py
â”‚   â”‚   â”‚   â””â”€â”€ agente_consulta.py
â”‚   â”‚   â”‚
â”‚   â”‚   â””â”€â”€ infra/                  # Infraestrutura cross-context
â”‚   â”‚       â”œâ”€â”€ cli/                # Typer + Rich
â”‚   â”‚       â”‚   â”œâ”€â”€ app.py
â”‚   â”‚       â”‚   â”œâ”€â”€ comandos/
â”‚   â”‚       â”‚   â”œâ”€â”€ exibicao.py
â”‚   â”‚       â”‚   â””â”€â”€ cliente_ipc.py
â”‚   â”‚       â”œâ”€â”€ servico/            # Daemon Windows Service
â”‚   â”‚       â”‚   â”œâ”€â”€ servidor.py     # Named Pipe server
â”‚   â”‚       â”‚   â”œâ”€â”€ ipc.py          # Protocolo IPC
â”‚   â”‚       â”‚   â””â”€â”€ servico_windows.py
â”‚   â”‚       â”œâ”€â”€ persistencia/       # Bancos de dados
â”‚   â”‚       â”‚   â”œâ”€â”€ postgres/
â”‚   â”‚       â”‚   â”œâ”€â”€ redis/
â”‚   â”‚       â”‚   â””â”€â”€ qdrant/
â”‚   â”‚       â””â”€â”€ llm/                # LLM providers
â”‚   â”‚           â”œâ”€â”€ cliente.py
â”‚   â”‚           â””â”€â”€ provedores/
â”‚   â”‚
â”‚   â””â”€â”€ hermesd/                    # Entry point do daemon
â”‚       â””â”€â”€ __main__.py
â”‚
â”œâ”€â”€ testes/
â”‚   â”œâ”€â”€ unitario/
â”‚   â”‚   â””â”€â”€ contexto/
â”‚   â”œâ”€â”€ integracao/
â”‚   â”‚   â”œâ”€â”€ persistencia/
â”‚   â”‚   â””â”€â”€ ipc/
â”‚   â””â”€â”€ e2e/
â”‚       â””â”€â”€ fluxos/
â”‚
â”œâ”€â”€ scripts/                        # AutomaÃ§Ã£o local
â”‚   â”œâ”€â”€ setup.ps1
â”‚   â”œâ”€â”€ lint.ps1
â”‚   â””â”€â”€ teste.ps1
â”‚
â”œâ”€â”€ docker/                         # ContÃªineres
â”‚   â”œâ”€â”€ docker-compose.yml
â”‚   â”œâ”€â”€ docker-compose.override.yml
â”‚   â””â”€â”€ Dockerfile
â”‚
â”œâ”€â”€ config/                         # ConfiguraÃ§Ãµes
â”‚   â”œâ”€â”€ exemplo.yaml
â”‚   â”œâ”€â”€ desenvolvimento.yaml
â”‚   â””â”€â”€ producao.yaml
â”‚
â””â”€â”€ pyproject.toml
```

---

**Premissas:**
- A arquitetura serÃ¡ implementada incrementalmente (MVP â†’ pÃ³s-MVP).
- O daemon Ã© o processo principal; o CLI Ã© thin client.

**Riscos:**
- Complexidade do Named Pipe pode exigir mais cÃ³digo que o estimado.
- Windows Service tem peculiaridades de instalaÃ§Ã£o e permissÃµes.

**PrÃ³ximos passos:**
- Detalhar Sistema de ConfiguraÃ§Ã£o ([[04-Arquitetura/Configuracao.md]]).
- Detalhar OperaÃ§Ã£o e Ciclo de Vida ([[04-Arquitetura/Operacao.md]]).
- Atualizar Componentes com implementaÃ§Ã£o concreta.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

