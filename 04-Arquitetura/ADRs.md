---
title: "Decisoes de Arquitetura (ADRs)"
description: "15 decisoes de arquitetura (ADR-001 a ADR-015)"
status: "concluido"
---

# DecisÃµes de Arquitetura (ADRs)

> **Registro de decisÃµes arquiteturais com contexto, opÃ§Ãµes consideradas e justificativas.**
> Formato baseado em Architecture Decision Records (ADRs).

---

## ADR-001 â€” Uso do Obsidian como MemÃ³ria Persistente

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa armazenar conhecimento de forma organizada, pesquisÃ¡vel e com relacionamentos entre informaÃ§Ãµes. O usuÃ¡rio jÃ¡ demonstrou interesse em usar o Obsidian como repositÃ³rio de conhecimento. |
| **OpÃ§Ã£o escolhida** | Obsidian como memÃ³ria principal do sistema |
| **Alternativas** | 1. Banco relacional puro (PostgreSQL) â€” sem capacidade nativa de linking e visualizaÃ§Ã£o. 2. Wiki tradicional (Confluence, Notion) â€” dependente de web, sem controle local. 3. Sistema de arquivos simples â€” sem estrutura de metadados e links. |
| **Vantagens** | - Estrutura de notas interligadas via [[links]] nativa<br>- Armazenamento local (seguranÃ§a e privacidade)<br>- FÃ¡cil visualizaÃ§Ã£o e ediÃ§Ã£o manual pelo usuÃ¡rio<br>- Suporte a plugins e integraÃ§Ãµes<br>- IndependÃªncia de vendor (arquivos .md padrÃ£o) |
| **Desvantagens** | - Sem controle de concorrÃªncia embutido<br>- Necessidade de mecanismo de backup externo<br>- API de integraÃ§Ã£o limitada (necessÃ¡rio plugin ou acesso direto ao filesystem) |
| **Justificativa** | O Obsidian atende perfeitamente ao requisito de memÃ³ria organizada com relacionamentos. O usuÃ¡rio jÃ¡ o conhece e quer utilizÃ¡-lo. A natureza local dos arquivos estÃ¡ alinhada com os requisitos de privacidade e seguranÃ§a. |
| **Impactos** | - Arquitetura deve tratar concorrÃªncia de escrita no vault<br>- Implementar mecanismo de backup automÃ¡tico |

---

## ADR-002 â€” Orquestrador Hermes

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa de um componente central que coordene os fluxos entre mÃ³dulos (transcriÃ§Ã£o, IA, memÃ³ria, integraÃ§Ãµes), gerencie estado e controle de permissÃµes. |
| **OpÃ§Ã£o escolhida** | Hermes como orquestrador dedicado |
| **Alternativas** | 1. Agente LLM puro (sem orquestrador) â€” perde determinismo e controle. 2. n8n como orquestrador principal â€” bom para automaÃ§Ãµes, mas limitado para lÃ³gica de estado e decisÃ£o complexa. 3. Microservices sem orquestrador â€” complexidade desnecessÃ¡ria para uso individual. |
| **Vantagens** | - Controle centralizado de fluxos e estado<br>- Facilidade para implementar aprovaÃ§Ã£o do usuÃ¡rio em cada etapa<br>- SeparaÃ§Ã£o entre orquestraÃ§Ã£o e execuÃ§Ã£o<br>- Flexibilidade para mudar componentes sem afetar o todo |
| **Desvantagens** | - Ponto Ãºnico de falha (mitigÃ¡vel com resiliÃªncia local)<br>- Complexidade adicional vs abordagem monolÃ­tica simples |
| **Justificativa** | Para um sistema com mÃºltiplas integraÃ§Ãµes e o requisito crÃ­tico de "nenhuma aÃ§Ã£o sem aprovaÃ§Ã£o", um orquestrador dedicado oferece o controle necessÃ¡rio sem acoplar os mÃ³dulos. |
| **Impactos** | - Hermes precisa ser implementado como mÃ³dulo central<br>- Fluxos de aprovaÃ§Ã£o sÃ£o gerenciados pelo orquestrador |

---

## ADR-003 â€” Whisper para TranscriÃ§Ã£o

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa transcrever Ã¡udio de atendimentos para texto, com extraÃ§Ã£o de pontos-chave. |
| **OpÃ§Ã£o escolhida** | Whisper (OpenAI) â€” preferencialmente local (whisper.cpp) |
| **Alternativas** | 1. Google Speech-to-Text â€” dependente de nuvem, custo por minuto. 2. Azure Speech â€” mesmo problema. 3. Modelo local alternativo (Wav2Vec2) â€” menor precisÃ£o. |
| **Vantagens** | - Alta precisÃ£o em mÃºltiplos idiomas<br>- OpÃ§Ã£o de execuÃ§Ã£o local (whisper.cpp) sem custo de API<br>- Open source e ativo na comunidade |
| **Desvantagens** | - ExecuÃ§Ã£o local requer GPU ou Ã© mais lenta em CPU<br>- Modelo grande (~3GB para versÃ£o local completa) |
| **Justificativa** | Whisper oferece o melhor equilÃ­brio entre precisÃ£o, custo (pode ser local) e privacidade (Ã¡udio nÃ£o sai da mÃ¡quina). |
| **Impactos** | - Avaliar trade-off entre precisÃ£o (modelo grande) vs velocidade (modelo pequeno/turbo)<br>- Se usar local, garantir que hardware suporta |

---

## ADR-004 â€” Banco Vetorial para Busca SemÃ¢ntica

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa pesquisar na base de conhecimento por similaridade semÃ¢ntica, nÃ£o apenas por palavras-chave. |
| **OpÃ§Ã£o escolhida** | Qdrant (preferencialmente local/Docker) |
| **Alternativas** | 1. Chroma â€” mais leve, mas menos maduro. 2. PostgreSQL + pgvector â€” bom se jÃ¡ usar PG, mas pode impactar performance. 3. FAISS (Facebook) â€” apenas indexaÃ§Ã£o, sem servidor. |
| **Vantagens** | - Performance superior em busca vetorial<br>- Suporte a filtros (cliente, data, tipo)<br>- Pode rodar localmente via Docker<br>- API REST para integraÃ§Ã£o |
| **Desvantagens** | - Requer Docker ou servidor dedicado<br>- Consumo adicional de memÃ³ria |
| **Justificativa** | Qdrant oferece o melhor equilÃ­brio entre performance, maturidade e facilidade de execuÃ§Ã£o local. |
| **Impactos** | - NecessÃ¡rio gerenciar embeddings do conteÃºdo do Obsidian<br>- SincronizaÃ§Ã£o entre Obsidian e Qdrant |

---

## ADR-005 â€” AutomaÃ§Ã£o com n8n

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa integrar mÃºltiplos serviÃ§os (e-mail, Movidesk, outros) em fluxos de automaÃ§Ã£o. |
| **OpÃ§Ã£o escolhida** | n8n como motor de automaÃ§Ã£o auxiliar |
| **Alternativas** | 1. Desenvolver automaÃ§Ãµes manualmente em cÃ³digo â€” mais flexÃ­vel, mas maior esforÃ§o. 2. Zapier/Make â€” dependente de nuvem e custo recorrente. 3. Scripts Python/Node simples â€” sem interface visual. |
| **Vantagens** | - Interface visual para fluxos<br>- AutomaÃ§Ã£o low-code<br>- Pode rodar localmente<br>- Ampla gama de integraÃ§Ãµes prontas (e-mail, HTTP, etc.) |
| **Desvantagens** | - Curva de aprendizado do n8n<br>- Pode ser excessivo para fluxos simples |
| **Justificativa** | n8n complementa o Hermes: Hermes orquestra a lÃ³gica de negÃ³cio (decisÃµes, aprovaÃ§Ãµes, estado), n8n executa automaÃ§Ãµes de integraÃ§Ã£o (enviar e-mail, atualizar Movidesk). |
| **Impactos** | - Hermes + n8n devem ter interfaces bem definidas<br>- n8n gerencia conexÃµes com serviÃ§os externos |

---

## ADR-006 â€” Interface do UsuÃ¡rio: Terminal (CLI) como PrimÃ¡ria

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa de uma interface para o usuÃ¡rio interagir durante os atendimentos. O usuÃ¡rio trabalha majoritariamente em ambiente tÃ©cnico (terminal, ferramentas de acesso remoto). |
| **OpÃ§Ã£o escolhida** | CLI como interface primÃ¡ria, com possibilidade de interface web complementar |
| **Alternativas** | 1. Web app â€” maior complexidade inicial, mas mais acessÃ­vel. 2. Desktop app (Electron/Tauri) â€” maior esforÃ§o de desenvolvimento. 3. Interface de voz â€” interessante, mas nÃ£o substitui uma interface visual. |
| **Vantagens** | - Desenvolvimento rÃ¡pido<br>- Baixo consumo de recursos<br>- Ideal para usuÃ¡rio tÃ©cnico<br>- FÃ¡cil integraÃ§Ã£o com hotkeys e automaÃ§Ãµes |
| **Desvantagens** | - Curva de aprendizado para interaÃ§Ã£o textual<br>- Limitado para exibiÃ§Ã£o de mÃ­dia (fotos, vÃ­deos)<br>- Menos intuitivo que interface grÃ¡fica |
| **Justificativa** | Para um MVP focado em produtividade e agilidade, CLI permite desenvolvimento mais rÃ¡pido e integraÃ§Ã£o direta com o fluxo de trabalho do usuÃ¡rio tÃ©cnico. Interface web pode ser adicionada posteriormente. |
| **Impactos** | - Desenvolvimento inicial focado em CLI<br>- Comandos intuitivos e auto-documentados<br>- Suporte a argumentos e modo interativo |

---

## ADR-007 â€” Arquitetura Modular com Ports & Adapters

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa ser flexÃ­vel para trocar componentes (ex.: trocar Whisper por outro transcriÃ§Ã£o, Qdrant por Chroma, LLM provider) sem impacto nos demais mÃ³dulos. |
| **OpÃ§Ã£o escolhida** | Arquitetura hexagonal (Ports & Adapters) no core do Hermes |
| **Alternativas** | 1. MonÃ³lito acoplado â€” mais rÃ¡pido de desenvolver, mas difÃ­cil de modificar. 2. Microservices â€” complexidade desnecessÃ¡ria. 3. Plugin-based â€” mais flexÃ­vel, mas mais complexo. |
| **Vantagens** | - Componentes intercambiÃ¡veis<br>- Testabilidade (mocks nos adapters)<br>- SeparaÃ§Ã£o clara entre domÃ­nio e infraestrutura<br>- Facilita adiÃ§Ã£o de novos providers |
| **Desvantagens** | - Mais cÃ³digo inicial (interfaces, adapters)<br>- Overhead de abstraÃ§Ã£o para sistemas simples |
| **Justificativa** | Dada a quantidade de integraÃ§Ãµes externas e a probabilidade de troca de componentes, ports & adapters oferece o melhor custo-benefÃ­cio entre flexibilidade e complexidade. |
| **Impactos** | - Cada integraÃ§Ã£o externa terÃ¡ uma interface (port) e uma implementaÃ§Ã£o (adapter)<br>- Core do Hermes nÃ£o depende de bibliotecas externas diretamente |

---

---

## ADR-008 â€” Python como Linguagem de ImplementaÃ§Ã£o

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema requer integraÃ§Ãµes com IA (LLMs, Whisper), processamento de Ã¡udio, CLI rica e banco vetorial. A escolha da linguagem impacta a produtividade do desenvolvimento, ecossistema disponÃ­vel e facilidade de manutenÃ§Ã£o. |
| **OpÃ§Ã£o escolhida** | Python 3.12+ |
| **Alternativas** | 1. Node.js (TypeScript) â€” melhor para I/O concorrente, mas ecossistema de IA menos maduro. Whisper sem binding nativo. 2. Go â€” excelente performance, mas ecossistema de IA e processamento de Ã¡udio muito limitado. 3. C# â€” Windows-first, mas ecossistema de IA inferior e comunidade menor. |
| **Vantagens** | - Ecossistema de IA maduro (LangChain, LlamaIndex, SDKs nativos)<br>- Whisper com suporte nativo (whisper.cpp bindings)<br>- Rich/Textual para CLI/TUI rica<br>- FastAPI para API futura<br>- Processamento de Ã¡udio robusto (sounddevice, PyAudio) |
| **Desvantagens** | - Tipagem opcional (mitigado com mypy + type hints rigorosos)<br>- DistribuiÃ§Ã£o via PyInstaller (executÃ¡vel maior)<br>- GIL pode limitar paralelismo (mitigado com asyncio + threads) |
| **Justificativa** | O domÃ­nio do problema (IA, Ã¡udio, NLP) Ã© onde Python tem o ecossistema mais maduro. A produtividade no desenvolvimento supera as desvantagens de distribuiÃ§Ã£o e tipagem. |
| **Impactos** | - Projeto usarÃ¡ pyproject.toml, mypy, ruff<br>- DistribuiÃ§Ã£o via PyInstaller ou Nuitka<br>- DependÃªncias: openai, anthropic, sounddevice, rich, typer, pyyaml |

---

## ADR-009 â€” Modo de OperaÃ§Ã£o: Daemon + CLI

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema precisa manter estado entre comandos (sessÃµes ativas, gravaÃ§Ãµes em andamento, fila de aprovaÃ§Ãµes). Uma CLI pura (one-shot) nÃ£o mantÃ©m estado entre execuÃ§Ãµes e nÃ£o pode gerenciar hotkeys globais nem notificaÃ§Ãµes. |
| **OpÃ§Ã£o escolhida** | Arquitetura bipartida: daemon (serviÃ§o Windows) + CLI |
| **Alternativas** | 1. CLI pura (one-shot) â€” cada comando Ã© um processo independente. Sem estado, sem hotkeys globais. 2. TUI pura (modo interativo) â€” estado mantido na sessÃ£o do terminal, mas sem hotkeys globais e sem acesso via scripts. 3. AplicaÃ§Ã£o desktop (Electron/Tauri) â€” complexidade excessiva para MVP. |
| **Vantagens** | - Estado persistente 24/7 (sessÃµes ativas sobrevivem a fechamento de terminal)<br>- Hotkeys globais funcionam mesmo sem terminal focado<br>- CLI pode ser usada em scripts e automaÃ§Ãµes<br>- Daemon gerencia concorrÃªncia e filas<br>- SeparaÃ§Ã£o clara entre interface e lÃ³gica |
| **Desvantagens** | - Complexidade adicional de IPC<br>- Gerenciamento de processo (Windows service)<br>- Duas superfÃ­cies de erro (CLI falha != daemon falha) |
| **Justificativa** | Estado persistente Ã© requisito fundamental (gravaÃ§Ã£o em andamento nÃ£o pode parar se o terminal fechar). Hotkeys globais sÃ£o essenciais para produtividade durante atendimentos. |
| **Impactos** | - ComunicaÃ§Ã£o via Named Pipes (IPC)<br>- Daemon registrado como Windows Service<br>- CLI Ã© thin client que encaminha comandos via IPC |

---

## ADR-010 â€” Sistema de ConfiguraÃ§Ã£o Centralizado

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema possui mÃºltiplos componentes configurÃ¡veis (integraÃ§Ãµes, hotkeys, Ã¡udio, LLM providers). O usuÃ¡rio precisa de um ponto Ãºnico e simples para configurar tudo. |
| **OpÃ§Ã£o escolhida** | Arquivo Ãºnico YAML em ~/.hermes/config.yaml + JSON Schema + variÃ¡veis de ambiente para secrets |
| **Alternativas** | 1. MÃºltiplos arquivos .env + JSON â€” fragmentado, difÃ­cil de gerenciar. 2. Banco de dados SQLite para config â€” overkill. 3. Interface de configuraÃ§Ã£o via CLI wizard â€” complexidade desnecessÃ¡ria. |
| **Vantagens** | - Arquivo Ãºnico, editÃ¡vel manualmente<br>- YAML Ã© legÃ­vel e suporta comentÃ¡rios<br>- JSON Schema valida a estrutura antes de carregar<br>- ${VAR} para secrets (sem expor no arquivo)<br>- Suporte a multi-profile (config.yaml, config.prod.yaml) |
| **Desvantagens** | - Erro de sintaxe YAML pode quebrar o sistema (mitigado com schema validation)<br>- UsuÃ¡rio precisa editar arquivo manualmente |
| **Justificativa** | Arquivo Ãºnico editÃ¡vel Ã© a abordagem mais simples e transparente para o usuÃ¡rio. YAML Ã© padrÃ£o em ferramentas DevOps e de IA. |
| **Impactos** | - Implementar loader com validaÃ§Ã£o de schema<br>- Secrets resolvidos via variÃ¡veis de ambiente (Windows Credential Manager)<br>- Hotkeys totalmente configurÃ¡veis no YAML |

---

## ADR-011 â€” ComunicaÃ§Ã£o entre MÃ³dulos via Event Bus

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O Hermes possui mÃºltiplos mÃ³dulos (SessionManager, WorkflowEngine, ApprovalManager, AuditLogger, adapters) que precisam se comunicar sem acoplamento direto. Eventos como "transcriÃ§Ã£o concluÃ­da" disparam aÃ§Ãµes em cascata (registrar no Obsidian, sugerir OS, notificar usuÃ¡rio). |
| **OpÃ§Ã£o escolhida** | Event Bus assÃ­ncrono pub/sub interno (in-process) |
| **Alternativas** | 1. Chamada direta entre mÃ³dulos â€” acoplamento forte, difÃ­cil de estender. 2. Filas externas (RabbitMQ, Redis Pub/Sub) â€” overkill para processo Ãºnico. 3. Callbacks/observers â€” mais complexo de gerenciar ciclo de vida. |
| **Vantagens** | - Baixo acoplamento (publisher nÃ£o conhece subscribers)<br>- FÃ¡cil adicionar novos listeners<br>- AssÃ­ncrono (nÃ£o bloqueia o publisher)<br>- Ideal para logging, auditoria, notificaÃ§Ãµes |
| **Desvantagens** | - DepuraÃ§Ã£o mais complexa (fluxo indireto)<br>- Risco de dead event (ninguÃ©m escuta) ou event avalanche (muitos eventos seguidos) |
| **Justificativa** | O fluxo de um atendimento gera mÃºltiplos eventos em cadeia. O Event Bus permite que cada mÃ³dulo reaja apenas aos eventos que lhe interessam, sem acoplamento. |
| **Impactos** | - Core conterÃ¡ EventBus com subscribe/publish<br>- Eventos tipados (dataclasses)<br>- Subscribers registrados na inicializaÃ§Ã£o (container DI) |

---

## ADR-012 â€” IPC via Named Pipes (CLI â†” Daemon)

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O CLI precisa se comunicar com o daemon para enviar comandos e receber respostas. A comunicaÃ§Ã£o precisa ser bidirecional, rÃ¡pida e funcionar no Windows sem depender de rede. |
| **OpÃ§Ã£o escolhida** | Named Pipes (Windows) com mensagens JSON |
| **Alternativas** | 1. TCP localhost (socket) â€” funciona, mas porta pode conflitar. 2. Arquivos de lock/pipe no filesystem â€” lento e frÃ¡gil. 3. stdin/stdout com subprocess â€” o CLI nÃ£o gerencia o daemon. |
| **Vantagens** | - Nativo do Windows (performÃ¡tico)<br>- Bidirecional (request/response + eventos)<br>- Sem risco de conflito de porta<br>- Apenas o usuÃ¡rio logado acessa (seguranÃ§a implÃ­cita) |
| **Desvantagens** | - Windows-only (se quiser Linux no futuro, precisa de adaptaÃ§Ã£o)<br>- ImplementaÃ§Ã£o um pouco mais verbosa que sockets |
| **Justificativa** | O sistema roda exclusivamente no Windows. Named Pipes Ã© o mecanismo IPC mais adequado: rÃ¡pido, seguro, sem configuraÃ§Ã£o de rede. |
| **Impactos** | - Daemon: servidor de Named Pipe (\\.\pipe\hermes)<br>- CLI: cliente Named Pipe<br>- Protocolo: JSON-RPC simplificado (mÃ©todo, params, resposta) |

---

## ADR-013 â€” InjeÃ§Ã£o de DependÃªncia via Composition Root

| Campo | Valor |
|-------|-------|
| **Status** | Aceito |
| **Data** | 02/07/2026 |
| **Contexto** | O sistema usa Ports & Adapters (ADR-007). As dependÃªncias precisam ser resolvidas em um ponto central, com escolha de implementaÃ§Ã£o baseada na configuraÃ§Ã£o. |
| **OpÃ§Ã£o escolhida** | Composition Root manual (funÃ§Ã£o container) sem framework de DI pesado |
| **Alternativas** | 1. Dependency Injector (Python lib) â€” adiciona dependÃªncia externa e complexidade. 2. Service locator â€” anti-pattern. 3. InjeÃ§Ã£o manual dispersa â€” difÃ­cil de rastrear. |
| **Vantagens** | - Zero dependÃªncias externas para DI<br>- ExplÃ­cito e rastreÃ¡vel<br>- FÃ¡cil de entender e debugar<br>- Escolha do adapter condicionada Ã  config |
| **Desvantagens** | - Mais verboso que um framework<br>- Container precisa ser atualizado manualmente quando novos adapters surgirem |
| **Justificativa** | Para um sistema de porte individual, um composition root manual Ã© mais simples e transparente que um framework de DI. A complexidade nÃ£o justifica a dependÃªncia. |
| **Impactos** | - Arquivo container.py com funÃ§Ã£o que instancia todos os objetos<br>- Config Ã© lida â†’ container Ã© montado â†’ sistema inicia<br>- FÃ¡cil trocar implementaÃ§Ãµes (ex.: MockTranscriber para testes) |

---

## ADR-014 â€” AbstraÃ§Ã£o de Transporte para ExpansÃ£o de Rede (Futuro)

| Campo | Valor |
|-------|-------|
| **Status** | Diferido (pÃ³s-MVP) |
| **Data** | 02/07/2026 |
| **Contexto** | O MVP utiliza Named Pipes (ADR-012) para comunicaÃ§Ã£o CLI â†” Daemon, restrito Ã  mÃ¡quina local. Futuramente, o usuÃ¡rio pode querer acessar o Hermes de outra mÃ¡quina via VPN, ou expor uma interface web. O Ã¡udio continuarÃ¡ sendo capturado apenas na mÃ¡quina do daemon (desafio tÃ©cnico conhecido). |
| **OpÃ§Ã£o escolhida** | Abstrair o transporte por trÃ¡s de uma interface `ITransport` que permita trocar Named Pipe por TCP socket sem alterar a lÃ³gica de negÃ³cio |
| **Alternativas** | 1. ComeÃ§ar com TCP desde o MVP â€” adiciona complexidade de rede, TLS e autenticaÃ§Ã£o sem benefÃ­cio imediato. 2. Manter Named Pipe e depois reescrever â€” retrabalho. |
| **Vantagens** | - MVP mais simples (Named Pipe)<br>- ExpansÃ£o futura sem refatoraÃ§Ã£o do core<br>- Suporte a mÃºltiplos transportes (Named Pipe, TCP, WebSocket)<br>- Tanto CLI quanto Web UI podem usar o mesmo backend |
| **Desvantagens** | - AbstraÃ§Ã£o adicional no cÃ³digo (interface + adapter)<br>- Complexidade marginal de design |
| **Justificativa** | A abstraÃ§Ã£o tem custo baixo (uma interface + dois adapters) e evita retrabalho futuro. O padrÃ£o jÃ¡ estÃ¡ alinhado com Ports & Adapters (ADR-007). |
| **Impactos** | - Criar `core/ports/i_transport.py` â€” interface Ãºnica para IPC<br>- Adapter `named_pipe.py` para o MVP<br>- Adapter `tcp_socket.py` para o futuro (com TLS + token de autenticaÃ§Ã£o)<br>- CLI escolhe o transporte via config.yaml |

## ADR-015 â€” Desafio de Ãudio Remoto (Diferido)

| Campo | Valor |
|-------|-------|
| **Status** | Diferido (pÃ³s-MVP) |
| **Data** | 02/07/2026 |
| **Contexto** | Se o Hermes for acessado remotamente (ADR-014), o Ã¡udio Ã© capturado no microfone da mÃ¡quina onde o daemon roda. Capturar Ã¡udio da mÃ¡quina remota que executa o CLI exigiria streaming de Ã¡udio pela rede, com latÃªncia, sincronizaÃ§Ã£o e consumo de banda. |
| **DecisÃ£o** | Adiar. No MVP e pÃ³s-MVP imediato, o Ã¡udio Ã© sempre capturado na mÃ¡quina do daemon. O desafio de Ã¡udio remoto serÃ¡ tratado como feature separada quando houver demanda concreta. |
| **Impactos** | - Documentado como desafio tÃ©cnico conhecido<br>- NÃ£o bloqueia a expansÃ£o de rede para comandos, status e aprovaÃ§Ãµes<br>- Quando necessÃ¡rio, avaliar WebRTC ou streaming de Ã¡udio via WebSocket |

| ADR | DecisÃ£o | Status |
|-----|---------|--------|
| 001 | Obsidian como memÃ³ria persistente | Aceito |
| 002 | Hermes como orquestrador central | Aceito |
| 003 | Whisper para transcriÃ§Ã£o (preferÃªncia local) | Aceito |
| 004 | Qdrant para banco vetorial | Aceito |
| 005 | n8n para automaÃ§Ã£o auxiliar | Aceito |
| 006 | CLI como interface primÃ¡ria | Aceito |
| 007 | Arquitetura hexagonal (Ports & Adapters) | Aceito |
| 008 | Python como linguagem de implementaÃ§Ã£o | Aceito |
| 009 | Modo de operaÃ§Ã£o Daemon + CLI | Aceito |
| 010 | ConfiguraÃ§Ã£o centralizada (YAML + Schema) | Aceito |
| 011 | Event Bus pub/sub interno | Aceito |
| 012 | IPC via Named Pipes (JSON) | Aceito |
| 013 | DI via Composition Root manual | Aceito |
| 014 | AbstraÃ§Ã£o de Transporte (Rede futura) | Diferido |
| 015 | Desafio de Ãudio Remoto | Diferido |

---

**Premissas:**
- ADRs podem ser revisitados e alterados conforme o projeto evolui.
- ADRs Aceitos sÃ£o decisÃµes fechadas; ADRs Propostos ainda podem mudar.

**Riscos:**
- DecisÃµes tomadas cedo podem precisar ser revistas se novas informaÃ§Ãµes surgirem.

**PrÃ³ximos passos:**
- Detalhar Arquitetura Geral com diagramas de processo.
- Especificar Componentes com implementaÃ§Ã£o concreta.
- Documentar sistema de ConfiguraÃ§Ã£o e OperaÃ§Ã£o.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

