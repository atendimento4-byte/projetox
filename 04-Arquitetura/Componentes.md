---
title: "Componentes"
description: "13 componentes (C01-C13) com interfaces e implementacoes"
status: "concluido"
---

# Componentes

> **Detalhamento dos módulos e serviços do sistema.**
> Cada componente possui responsabilidade bem definida, interfaces (Ports), implementações (Adapters) e dependências.
>
> As decisões arquiteturais que fundamentam estes componentes estão nas [[04-Arquitetura/ADRs.md|ADRs]].

---

## C01 — CLI Interface (hermes)

**Responsabilidade:** Interface de linha de comando do usuário. Thin client que envia comandos ao daemon via IPC e exibe resultados.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/infra/cli/` |
| **Tecnologia** | Typer (framework CLI) + Rich (terminal rico) |
| **Tipo** | Processo efêmero (inicia, executa, termina) |
| **Input** | Argumentos de linha de comando + hotkeys (via daemon) |
| **Output** | Terminal formatado (Rich: tabelas, painéis, markdown, cores) |

**Arquitetura interna:**
```
hermes/infra/cli/
├── app.py              # App Typer (entry point)
├── ipc_client.py       # Cliente Named Pipe
├── display.py          # Helpers de exibição Rich
├── commands/
│   ├── session.py      # iniciar, finalizar, status
│   ├── audio.py        # gravar, parar, pausar, retomar
│   ├── transcription.py # transcrever, resumir
│   ├── knowledge.py    # salvar, buscar
│   ├── os.py           # fechar
│   ├── email.py        # email-compra, email-comunicado
│   ├── approval.py     # pendentes, aprovar, rejeitar, editar
│   └── config.py       # init, edit, show, validate
└── keybinds.py         # Leitura de hotkeys do config.yaml
```

**Fluxo de execução de um comando:**
1. Typer interpreta argumentos
2. Carrega config.yaml (apenas seção de conexão)
3. Conecta ao Named Pipe do daemon
4. Envia requisição JSON (method + params)
5. Aguarda resposta (timeout: 30s)
6. Exibe resultado com Rich (tabela, painel, markdown)
7. Desconecta e termina

**Interfaces:**
- `IPCClient` — conecta ao Named Pipe, envia/recebe JSON
- `Display` — formata saída (info, sucesso, erro, tabela, painel)

**Dependências:** Typer, Rich, PyYAML, win32pipe

---

## C02 — Daemon (hermesd)

**Responsabilidade:** Serviço de background. Mantém estado do sistema, gerencia sessões, áudio, hotkeys e orquestra todos os módulos.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/infra/servico/` |
| **Tecnologia** | Python asyncio + Windows Service (pywin32) |
| **Tipo** | Processo contínuo (Windows Service) |
| **Estado** | Mantém sessões ativas, fila de aprovações, contexto |
| **Input** | Comandos via IPC (Named Pipe) + eventos internos + hotkeys |
| **Output** | Respostas via IPC + logs + ações externas (e-mail, Movidesk, Obsidian) |

**Arquitetura interna:**
```
hermes/infra/servico/
├── service.py           # Wrapper Windows Service (pywin32)
├── servidor.py          # Servidor Named Pipe
└── hotkey_listener.py   # Monitor de hotkeys globais
```

**Subcomponentes gerenciados pelo Daemon:**
- C03 a C13 (todos os serviços)
- Tudo roda dentro do mesmo processo (asyncio event loop + thread pool)

**Ciclo de vida:** Ver [[04-Arquitetura/Operacao.md]] para detalhes de startup/shutdown.

**Dependências:** pywin32, keyboard, asyncio

---

## C03 — Core Engine

**Responsabilidade:** Lógica de negócio central. Orquestra fluxos, gerencia estado, coordena aprovações.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/compartilhado/` |
| **Tecnologia** | Python puro + asyncio |
| **Tipo** | Módulo core (zero dependências externas diretas) |
| **Padrão** | Ports & Adapters (domain puro) |

**Módulos internos:**

```
hermes/compartilhado/
├── gerenciador_sessao.py
├── motor_fluxo_trabalho.py
├── gerenciador_aprovacao.py
├── registrador_auditoria.py
├── gerenciador_contexto.py
└── barramento_eventos/
```

### C03.1 — SessionManager
**Arquivo:** `gerenciador_sessao.py`
**Responsabilidade:** Gerenciar sessões de acompanhamento.
- Máquina de estados: `created → active → recording → paused → completed`
- Valida transições de estado
- Persiste estado para recuperação de falhas
- Garante apenas 1 sessão ativa por vez

**Interface:**
```python
class ISessionManager:
    async def start(ticket_id: str) -> Session
    async def end() -> Session
    async def pause() -> Session
    async def resume() -> Session
    async def status() -> SessionStatus
    async def get(session_id: str) -> Session
```

### C03.2 — WorkflowEngine
**Arquivo:** `motor_fluxo_trabalho.py`
**Responsabilidade:** Executar fluxos de trabalho (workflows) com sequência de passos.
- Workflow: `acompanhar → gravar → transcrever → registrar → fechar`
- Cada passo pode ter rollback
- Suporta steps síncronos e assíncronos
- Publica eventos no EventBus a cada transição de passo

**Interface:**
```python
class IWorkflowEngine:
    async def execute(workflow_name: str, context: dict) -> WorkflowResult
    async def step_current() -> str
    async def rollback() -> None
```

### C03.3 — ApprovalManager
**Arquivo:** `gerenciador_aprovacao.py`
**Responsabilidade:** Gerenciar fila de ações pendentes de aprovação do usuário.
- Mantém fila ordenada por urgência
- Suporta: aprovar, rejeitar, editar, sonegar
- Ações expiram (TTL configurável)
- Publica evento `approval.pending` quando novas ações surgem

**Interface:**
```python
class IApprovalManager:
    async def add(action: PendingAction) -> None
    async def list() -> list[PendingAction]
    async def decide(action_id: str, decision: Decision) -> None
    async def count_pending() -> int
```

### C03.4 — AuditLogger
**Arquivo:** `registrador_auditoria.py`
**Responsabilidade:** Registro imutável de auditoria (append-only).
- Todas as ações críticas são registradas
- Hash chain (cada entrada contém hash da anterior)
- Dois destinos: PostgreSQL (persistente) + arquivo JSON (consulta rápida)

**Interface:**
```python
class IAuditLogger:
    async def log(event: AuditEvent) -> None
    async def query(filters: AuditFilter) -> list[AuditEvent]
```

### C03.5 — ContextManager
**Arquivo:** `gerenciador_contexto.py`
**Responsabilidade:** Manter contexto do atendimento atual (cliente, equipamento, problema).
- Contexto enriquecido durante o atendimento
- Usado pelos agentes de IA para gerar sugestões contextuais
- Persistido entre comandos do CLI

**Interface:**
```python
class IContextManager:
    async def set(key: str, value: Any) -> None
    async def get(key: str) -> Any
    async def snapshot() -> dict
    async def clear() -> None
```

### C03.6 — EventBus
**Arquivo:** `barramento_eventos/`
**Responsabilidade:** Barramento de eventos pub/sub assíncrono.
- Publishers: qualquer módulo que publica eventos
- Subscribers: módulos registrados que reagem a eventos
- Eventos tipados (dataclasses)
- Assíncrono (não bloqueia o publisher)

**Interface:**
```python
class IEventBus:
    async def publish(event: Event) -> None
    def subscribe(event_type: str, handler: Callable) -> None
    def unsubscribe(event_type: str, handler: Callable) -> None
```

**Eventos do sistema:**
| Evento | Publisher | Subscribers |
|--------|-----------|-------------|
| `session.started` | SessionManager | Logger, CLI (IPC) |
| `session.ended` | SessionManager | Logger, CLI |
| `audio.recording.started` | AudioRecorder | Logger, CLI, ContextManager |
| `audio.recording.stopped` | AudioRecorder | Logger, CLI, Transcriber |
| `transcription.completed` | Transcriber | Logger, MemoryAgent, DocAgent |
| `knowledge.suggested` | MemoryAgent | Logger, ApprovalManager |
| `knowledge.saved` | MemoryAgent | Logger, CLI |
| `os.suggested` | DocAgent | Logger, ApprovalManager |
| `os.closed` | DocAgent | Logger, CLI |
| `email.generated` | CommAgent | Logger, ApprovalManager |
| `email.sent` | CommAgent | Logger, CLI |
| `approval.pending` | ApprovalManager | Logger, CLI (IPC event) |
| `approval.decided` | ApprovalManager | Logger, CLI |
| `error.occurred` | Vários | Logger, CLI |

---

## C04 — Audio Recorder

**Responsabilidade:** Capturar áudio do microfone do sistema.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/audio/integracao/gravador/` |
| **Interface** | `IAudioRecorder` (Port em `core/ports/i_audio.py`) |
| **Tecnologia** | sounddevice (Python) |
| **Tipo** | Serviço contínuo (thread separada no daemon) |
| **Input** | Comandos: `start()`, `stop()`, `pause()`, `resume()` |
| **Output** | Arquivo WAV + eventos no EventBus |

**Port (IAudioRecorder):**
```python
class IAudioRecorder:
    async def start() -> None
    async def stop() -> RecorderResult
    async def pause() -> None
    async def resume() -> None
    def is_recording() -> bool
```

**Comportamento:**
- Usa thread separada para não introduzir latência
- Buffer circular (últimos 30s em memória) para captura retroativa
- Filtro de ruído básico (opcional, configurável)
- Salva em WAV (16kHz, mono, 16bit)
- Publica eventos: `audio.recording.started`, `audio.recording.stopped`

**Configuração:**
```python
AudioConfig:
    device: Optional[int] = None      # None = padrão do sistema
    sample_rate: int = 16000
    channels: int = 1
    format: str = "wav"
    noise_filter: bool = True
```

**Dependências:** sounddevice, numpy, scipy (para filtro)

---

## C05 — Transcriber

**Responsabilidade:** Transcrever áudio para texto utilizando Whisper.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/audio/integracao/transcritor/` |
| **Interface** | `ITranscriber` |
| **Implementações** | `whisper_api.py` (API OpenAI), `whisper_local.py` (whisper.cpp) |
| **Input** | Caminho do arquivo de áudio |
| **Output** | Texto transcrito + metadados (duração, confiança) |

**Port (ITranscriber):**
```python
class ITranscriber:
    async def transcribe(audio_path: str) -> TranscriptionResult
```

**TranscriptionResult:**
```python
class TranscriptionResult:
    text: str
    segments: list[Segment]  # timestamp, texto
    language: str
    duration: float
    confidence: float
```

**Whisper API Adapter:**
- Envia arquivo para OpenAI Whisper API
- Modelo: whisper-1 (padrão) ou configurável
- Idioma: pt (configurável)
- Retry: 2x com backoff exponencial

**Whisper Local Adapter (futuro):**
- Executa whisper.cpp via subprocess
- Modelos: turbo, large, medium (configurável)
- Thread pool para não bloquear event loop

---

## C06 — LLM Client

**Responsabilidade:** Interface com modelo de linguagem para geração de resumos, sugestões e respostas.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/infra/llm/` |
| **Interface** | `ILLM` |
| **Implementações** | `anthropic.py`, `openai.py`, `google.py` |
| **Padrão** | Strategy (selecionado via config) |
| **Input** | Prompt + contexto + parâmetros |
| **Output** | Resposta gerada |

**Port (ILLM):**
```python
class ILLM:
    async def generate(prompt: str, context: dict, params: LLMParams) -> str
    async def generate_stream(prompt: str, context: dict, params: LLMParams) -> AsyncIterator[str]
```

**Parâmetros:**
```python
class LLMParams:
    model: str
    max_tokens: int = 4096
    temperature: float = 0.3
    system_prompt: str | None = None
```

**Cache:**
- Respostas do LLM são cacheadas por hash do prompt (TTL configurável)
- Cache armazenado no Redis (se disponível) ou em memória

---

## C07 — Memory Manager (Obsidian)

**Responsabilidade:** Gerenciar o vault do Obsidian — criar, atualizar, ler e linkar notas Markdown.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/memoria/integracao/vault/` |
| **Interface** | `IMemory` |
| **Tecnologia** | Acesso direto ao filesystem (.md) |
| **Input** | Comandos de CRUD de notas |
| **Output** | Conteúdo de notas + confirmação |

**Port (IMemory):**
```python
class IMemory:
    async def create_note(path: str, content: str, frontmatter: dict) -> NoteRef
    async def update_note(path: str, content: str, frontmatter: dict) -> NoteRef
    async def get_note(path: str) -> Note | None
    async def find_by_tag(tag: str) -> list[NoteRef]
    async def find_by_link(target: str) -> list[NoteRef]
    async def get_note_links(path: str) -> list[str]
    async def exists(path: str) -> bool
```

**Regras de escrita:**
- Sempre escrever em arquivo temporário → renomear (operação atômica)
- Validar frontmatter antes de escrever
- Atualizar links existentes se necessário
- Lock de arquivo para evitar concorrência com edição manual

> A estrutura detalhada do vault está em [[05-Dados/Memoria-Obsidian.md]].

**Estrutura do vault:** Ver [[05-Dados/Memoria-Obsidian.md]]

---

## C08 — Movidesk Client

**Responsabilidade:** Integração com API do Movidesk para consultar e atualizar chamados.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/integracao/integracao/movidesk/` |
| **Interface** | `IMovidesk` |
| **Tecnologia** | HTTP REST (httpx async) |
| **Input** | Comandos de consulta/atualização |
| **Output** | Dados do chamado + confirmação |

> A referência completa da API está em [[04-Arquitetura/Movidesk-API.md]].

**Port (IMovidesk):**
```python
class IMovidesk:
    async def get_ticket(ticket_id: str) -> Ticket
    async def get_ticket_by_protocol(protocol: str) -> Ticket
    async def search_tickets(filters: ODataFilter) -> list[Ticket]
    async def create_ticket(data: TicketCreate) -> Ticket
    async def update_ticket(ticket_id: str, data: TicketUpdate) -> Ticket
    async def attach_file(ticket_id: str, action_id: str, file_path: str) -> None
    async def get_html_description(ticket_id: str, action_id: str) -> str
```

**Tratamento de erros:**
- Timeout: 15s
- Retry: 3x com backoff exponencial (1s, 2s, 4s)
- 401: token inválido → notificar usuário
- 429: rate limit → ler header `retry-after` e aguardar

---

## C09 — Email Service

**Responsabilidade:** Envio de e-mails via provedor configurado.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/comunicacao/integracao/email/` |
| **Interface** | `IEmail` |
| **Tecnologia** | aiosmtplib (async SMTP) |
| **Input** | Comandos: enviar, salvar rascunho |
| **Output** | Confirmação de envio |

**Port (IEmail):**
```python
class IEmail:
    async def send(message: EmailMessage) -> EmailResult
    async def save_draft(message: EmailMessage) -> None
```

---

## C10 — Vector Store (Qdrant)

**Responsabilidade:** Armazenar e consultar embeddings para busca semântica.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/contexto/memoria/integracao/banco_vetorial/` |
| **Interface** | `IVectorStore` |
| **Tecnologia** | Qdrant client (async) |
| **Input** | Texto para busca, documentos para indexar |
| **Output** | Resultados ordenados por similaridade |

**Port (IVectorStore):**
```python
class IVectorStore:
    async def search(query: str, filters: dict, limit: int) -> list[SearchResult]
    async def index(doc_id: str, text: str, metadata: dict) -> None
    async def remove(doc_id: str) -> None
    async def health() -> bool
```

---

## C11 — Cache / State Store (Redis)

**Responsabilidade:** Cache temporário e estado de sessões.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/infra/persistencia/redis/` |
| **Interface** | `ICache` |
| **Tecnologia** | redis-py (async) |
| **Input** | Chave-valor |
| **Output** | Valor |

**Port (ICache):**
```python
class ICache:
    async def get(key: str) -> str | None
    async def set(key: str, value: str, ttl: int) -> None
    async def delete(key: str) -> None
    async def exists(key: str) -> bool
    async def hget(hash: str, field: str) -> str | None
    async def hset(hash: str, field: str, value: str) -> None
```

---

## C12 — Database (PostgreSQL)

**Responsabilidade:** Dados estruturados do sistema.

| Atributo | Descrição |
|----------|-----------|
| **Localização** | `hermes/infra/persistencia/postgres/` |
| **Interface** | `IDatabase` |
| **Tecnologia** | asyncpg |
| **Input** | Queries |
| **Output** | Resultados |

**Port (IDatabase):**
```python
class IDatabase:
    async def execute(query: str, params: tuple) -> None
    async def fetch(query: str, params: tuple) -> list[dict]
    async def fetch_one(query: str, params: tuple) -> dict | None
    async def migrate() -> None
```

---

## C13 — Agentes de IA

**Responsabilidade:** Agentes especializados que utilizam o LLM para tarefas específicas.

| Agente | Localização | Função |
|--------|-------------|--------|
| **TranscriptionAgent** | `agentes/transcription_agent.py` | Extrair pontos-chave da transcrição |
| **MemoryAgent** | `agentes/memory_agent.py` | Classificar e estruturar conhecimento |
| **DocumentationAgent** | `agentes/documentation_agent.py` | Gerar resumo técnico para OS |
| **CommunicationAgent** | `agentes/communication_agent.py` | Redigir e-mails |
| **QueryAgent** | `agentes/query_agent.py` | Responder perguntas com base na base |

Cada agente estende a classe base `BaseAgent`:
```python
class BaseAgent(ABC):
    def __init__(self, llm: ILLM, event_bus: IEventBus)
    @abstractmethod
    async def execute(context: dict) -> AgentResult
    def subscribe_to_events(self, event_bus: IEventBus)  # opcional
```

**Detalhes:** Ver [[04-Arquitetura/Agentes.md]]

---

## Matriz de Componentes

| ID | Componente | Tecnologia | Execução | Porta |
|:--:|------------|------------|:--------:|:-----:|
| C01 | CLI Interface | Typer + Rich | CLI efêmero | — |
| C02 | Daemon | pywin32 + asyncio | Serviço Windows | — |
| C03 | Core Engine | Python puro | In-process (C02) | — |
| C04 | Audio Recorder | sounddevice | Thread em C02 | — |
| C05 | Transcriber | Whisper API/Local | In-process (C02) | — |
| C06 | LLM Client | HTTP (httpx) | In-process (C02) | — |
| C07 | Memory (Obsidian) | Filesystem | In-process (C02) | — |
| C08 | Movidesk Client | HTTP (httpx) | In-process (C02) | — |
| C09 | Email Service | SMTP (aiosmtplib) | In-process (C02) | — |
| C10 | Vector Store | Qdrant Client | Docker externo | 6333 |
| C11 | Cache | Redis Client | Docker externo | 6379 |
| C12 | Database | PostgreSQL Client | Docker externo | 5432 |
| C13 | AI Agents | LLM + templates | In-process (C02) | — |

---

**Premissas:**
- C01 a C09 rodam no mesmo processo (daemon).
- C10 a C12 rodam como serviços externos (Docker ou locais).
- Todos os adapters implementam interfaces definidas em `core/ports/`.

**Próximos passos:**
- Atualizar SDD-Index.md com novos documentos.
- Iniciar Sprint 0 (setup do projeto).

---
> [[00-Index/SDD-Index.md|Voltar ao índice]]

