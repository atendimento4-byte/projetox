---
title: "Integracoes"
description: "8 integracoes: Movidesk, Obsidian, E-mail, LLM, n8n, Whisper, Qdrant"
status: "concluido"
---

# IntegraÃ§Ãµes

> **Nota:** Os placeholders neste documento referentes Ã  API do Movidesk devem ser preenchidos com dados reais da conta antes do inÃ­cio da implementaÃ§Ã£o.

> **APIs externas, serviÃ§os terceiros, protocolos de integraÃ§Ã£o e configuraÃ§Ã£o.**
>
> DecisÃµes sobre cada integraÃ§Ã£o estÃ£o documentadas nas [[04-Arquitetura/ADRs.md|ADRs]]: ADR-003 (Whisper), ADR-004 (Qdrant), ADR-005 (n8n).
>
> A referÃªncia completa da API estÃ¡ em [[04-Arquitetura/Movidesk-API.md]].

---

## INT-001 â€” Movidesk API

**Tipo:** REST API
**Finalidade:** Consultar e atualizar chamados/OS
**DocumentaÃ§Ã£o oficial:** https://api.movidesk.com/public/v1

### MÃ©todos Utilizados

| OperaÃ§Ã£o | MÃ©todo | Endpoint | DescriÃ§Ã£o |
|----------|--------|----------|-----------|
| Consultar chamado Ãºnico | `GET` | `/tickets?id={id}` | ObtÃ©m ticket por ID ou protocolo |
| Listar chamados | `GET` | `/tickets?$select=...` | Lista com filtros OData |
| Listar chamados antigos | `GET` | `/tickets/past?$select=...` | Tickets com lastUpdate > 90 dias |
| Criar chamado | `POST` | `/tickets` | Cria novo ticket |
| Atualizar chamado | `PATCH` | `/tickets?id={id}` | Altera campos (parcial) |
| Upload de anexo | `POST` | `/ticketFileUpload?id={id}&actionId={id}` | Multipart form-data |
| Obter HTML das aÃ§Ãµes | `GET` | `/tickets/htmldescription?id={id}` | DescriÃ§Ã£o formatada |

> **Nota:** NÃ£o existe endpoint separado para interaÃ§Ãµes. AÃ§Ãµes sÃ£o manipuladas dentro do prÃ³prio ticket via `PATCH /tickets` com o campo `actions[]`.

### AutenticaÃ§Ã£o
- **Tipo:** Token de API (passado como query param `?token=`)
- **GeraÃ§Ã£o:** ConfiguraÃ§Ãµes â†’ Conta â†’ ParÃ¢metros â†’ Ambiente â†’ "Gerar nova chave"
- **Armazenamento:** Windows Credential Manager (nunca em cÃ³digo ou arquivo)
- **Header:** `Content-Type: application/json` obrigatÃ³rio em POST/PATCH

### Rate Limits
- **10 requisiÃ§Ãµes/minuto** (limite padrÃ£o, contratual para aumento)
- Bloqueio progressivo por requisiÃ§Ãµes com erro:
  - 3 erros â†’ bloqueio de **60s** (cÃ³digo `429 Too Many Failed Requests`)
  - +3 erros â†’ bloqueio de **120s**
  - +3 erros â†’ bloqueio de **300s**
- O header `retry-after` informa o tempo restante de bloqueio

### Tratamento de Erros
| CÃ³digo | AÃ§Ã£o |
|--------|------|
| 401 | Token invÃ¡lido â†’ notificar usuÃ¡rio |
| 429 | Rate limit â†’ ler `retry-after` e aguardar |
| 5xx | Servidor indisponÃ­vel â†’ retry 3x com backoff |

### Failover
- Se API indisponÃ­vel, sistema opera em modo offline:
  - Dados do chamado sÃ£o registrados localmente
  - SincronizaÃ§Ã£o automÃ¡tica quando API retornar
  - UsuÃ¡rio notificado sobre operaÃ§Ã£o offline

---

## INT-002 â€” Obsidian (Vault Local)

**Tipo:** Acesso a sistema de arquivos (.md)
**Finalidade:** Leitura e escrita de notas de conhecimento

### Acesso

| MÃ©todo | DescriÃ§Ã£o |
|--------|-----------|
| **PrimÃ¡rio** | Acesso direto ao filesystem (ler/escrever arquivos .md) |
| **Alternativo** | Obsidian Local REST API (via plugin) para operaÃ§Ãµes avanÃ§adas |

### LocalizaÃ§Ã£o
- **Caminho base:** `C:\Users\...\Documents\Obisidian\ProjetoX\` (vault do projeto)
- **Estrutura de pastas:** Definida em [[05-Dados/Memoria-Obsidian.md]]

### OperaÃ§Ãµes

| OperaÃ§Ã£o | ImplementaÃ§Ã£o |
|----------|---------------|
| Criar nota | `New-Item` / `fs.writeFile` no caminho adequado |
| Atualizar nota | Read â†’ edit â†’ write |
| Ler nota | Read file |
| Listar notas | File scan por pasta |
| Pesquisar conteÃºdo | Grep/ripgrep + busca semÃ¢ntica (Qdrant) |
| Criar links | Inserir `[[link]]` no conteÃºdo da nota |

### ConcorrÃªncia
- Usar locks de arquivo para evitar escrita simultÃ¢nea
- OperaÃ§Ãµes atÃ´micas (escrever em temp â†’ renomear)

### Backup
- Backup automÃ¡tico configurado (git ou cÃ³pia periÃ³dica)
- Versionamento via git do vault

---

## INT-003 â€” ServiÃ§o de E-mail

**Tipo:** SMTP ou API REST
**Finalidade:** Envio de e-mails (solicitaÃ§Ã£o de compra, comunicados)

### OpÃ§Ãµes

| Provedor | MÃ©todo | ConfiguraÃ§Ã£o |
|----------|--------|--------------|
| Gmail | Gmail API ou SMTP | OAuth2 ou App Password |
| Outlook | Graph API ou SMTP | OAuth2 |
| SMTP GenÃ©rico | SMTP | Servidor, porta, usuÃ¡rio, senha |

### ConfiguraÃ§Ã£o
- Armazenada em variÃ¡veis de ambiente ou Windows Credential Manager
- Permitir mÃºltiplas contas (ex.: pessoal + corporativa)

### Funcionalidades
- Enviar e-mail com corpo HTML e texto plano
- Anexar arquivos (documento OS, fotos)
- Salvar rascunho (nas pastas do provedor ou local)
- Templates customizÃ¡veis

### Tratamento de Erros
| Erro | AÃ§Ã£o |
|------|------|
| Falha de autenticaÃ§Ã£o | Notificar usuÃ¡rio |
| DestinatÃ¡rio invÃ¡lido | Notificar e solicitar correÃ§Ã£o |
| Anexo muito grande | Comprimir ou dividir |

---

## INT-004 â€” LLM Provider

**Tipo:** API REST
**Finalidade:** GeraÃ§Ã£o de resumos, sugestÃµes, respostas

> Ver [[04-Arquitetura/Seguranca.md|SeguranÃ§a]] para prÃ¡ticas de proteÃ§Ã£o de chaves de API.

### Provedores Suportados

| Provedor | Modelos | API |
|----------|---------|-----|
| Anthropic | Claude 3.5 Sonnet, Haiku, Opus | `POST /v1/messages` |
| OpenAI | GPT-4, GPT-4o, GPT-4o-mini | `POST /v1/chat/completions` |
| Google | Gemini 1.5 Pro, Flash | `POST /v1/models/{model}:generateContent` |
| Local (futuro) | Llama 3, Mistral via Ollama | API compatÃ­vel com OpenAI |

### AbstraÃ§Ã£o
- **Port:** `ILLM` â€” interface Ãºnica para qualquer provedor
- **Strategy Pattern:** Provider selecionÃ¡vel por config ou por tipo de tarefa
- Fallback automÃ¡tico entre provedores

### Gerenciamento de Custos
- Log de tokens usados por atendimento
- Sugerir modelo mais barato para tarefas simples (resumo vs anÃ¡lise)

### Tratamento de Erros
`429` (rate limit) â†’ retry com backoff + trocar de modelo/provedor se persistir
`400` (contexto muito longo) â†’ truncar e reenviar
`5xx` â†’ tentar provedor alternativo (fallback)

---

## INT-005 â€” n8n (Workflow Automation)

**Tipo:** Webhook REST + Polling
**Finalidade:** AutomaÃ§Ã£o de fluxos complexos

### ConfiguraÃ§Ã£o
- **ExecuÃ§Ã£o:** Docker local (`localhost:5678`)
- **AutenticaÃ§Ã£o:** Chave de API ou usuÃ¡rio/senha

### Workflows Previstos

| Workflow | DescriÃ§Ã£o | Gatilho |
|----------|-----------|---------|
| `email-compra` | Enviar e-mail de solicitaÃ§Ã£o de compra | Hermes via webhook |
| `email-comunicado` | Enviar e-mail de comunicado | Hermes via webhook |
| `movidesk-atualizar` | Atualizar chamado no Movidesk | Hermes via webhook |
| `movidesk-consultar` | Buscar dados de chamado | Hermes via webhook |
| `obsidian-backup` | Backup automÃ¡tico do vault | Agendado (diÃ¡rio) |

### IntegraÃ§Ã£o com Hermes
- Hermes dispara workflows via webhook HTTP
- Hermes pode aguardar resultado (sÃ­ncrono) ou apenas registrar (assÃ­ncrono)

---

## INT-006 â€” Whisper (TranscriÃ§Ã£o)

**Tipo:** Modelo local ou API REST
**Finalidade:** TranscriÃ§Ã£o de Ã¡udio para texto

### OpÃ§Ãµes

| OpÃ§Ã£o | DescriÃ§Ã£o | PrÃ³s | Contras |
|-------|-----------|------|---------|
| **Local (whisper.cpp)** | ExecuÃ§Ã£o local do modelo | Privacidade, sem custo | Requer hardware compatÃ­vel (GPU ideal) |
| **API OpenAI Whisper** | API paga | PrecisÃ£o alta, sem overhead local | Custo por minuto, dependÃªncia internet |

### DecisÃ£o
- **MVP:** API OpenAI Whisper (mais rÃ¡pida de implementar)
- **PÃ³s-MVP:** Implementar fallback local (whisper.cpp) para cenÃ¡rios offline

### Formatos de Ãudio Suportados
.wav, .mp3, .m4a, .ogg

### ParÃ¢metros de ConfiguraÃ§Ã£o
- Idioma: portuguÃªs (auto-detect disponÃ­vel)
- Modelo: turbo (balance speed/accuracy) ou large (precisÃ£o mÃ¡xima)
- Temperatura: 0 (determinÃ­stico)

---

## INT-007 â€” Qdrant (Banco Vetorial)

**Tipo:** Servidor REST/gRPC
**Finalidade:** Armazenamento e consulta de embeddings

### ConfiguraÃ§Ã£o
- **ExecuÃ§Ã£o:** Docker local
- **Porta:** 6333 (REST), 6334 (gRPC)
- **AutenticaÃ§Ã£o:** Desabilitada (rede local) ou chave de API

### Collections

| Collection | ConteÃºdo | Tamanho do Vetor | MÃ©trica |
|------------|----------|-----------------|---------|
| `notas_obsidian` | Embeddings de notas do vault | 1536 (Ada-002) | Cosine |
| `atendimentos` | Embeddings de resumos de atendimento | 1536 | Cosine |

### SincronizaÃ§Ã£o com Obsidian
- Monitorar alteraÃ§Ãµes no vault (watcher)
- Re-indexar notas modificadas
- SincronizaÃ§Ã£o pode ser automÃ¡tica ou sob demanda

---

## INT-008 â€” Sistema de Ãudio (Hardware)

**Tipo:** Dispositivo de Ã¡udio local
**Finalidade:** Captura de Ã¡udio do microfone

### Requisitos
- Microfone padrÃ£o do sistema (integrado ou headset)
- Acesso Ã  API de Ã¡udio do sistema operacional

### ConfiguraÃ§Ã£o
- SeleÃ§Ã£o de dispositivo de entrada (microfone)
- ConfiguraÃ§Ã£o de qualidade: taxa de amostragem (16kHz-48kHz), canais (mono)

### Formato de SaÃ­da
- WAV (formato bruto para Whisper)
- MP3 (compactado para armazenamento)

---

## Matriz de IntegraÃ§Ãµes

| ID | IntegraÃ§Ã£o | Tipo | CrÃ­tica para MVP | DependÃªncia |
|----|------------|------|:----------------:|:-----------:|
| INT-001 | Movidesk API | REST | Sim | Internet |
| INT-002 | Obsidian Vault | Filesystem | Sim | â€” |
| INT-003 | E-mail | SMTP/API | Sim | Internet |
| INT-004 | LLM Provider | REST | Sim | Internet |
| INT-005 | n8n | Docker/Webhook | NÃ£o (pÃ³s-MVP) | Docker |
| INT-006 | Whisper | Local/API | Sim | â€” (local) |
| INT-007 | Qdrant | Docker/REST | Sim | Docker |
| INT-008 | Ãudio | Hardware | Sim | â€” |

---

**Premissas:**
- Todas as integraÃ§Ãµes serÃ£o implementadas como Adapters (Ports & Adapters).
- O arquivo de configuraÃ§Ã£o centralizarÃ¡ credenciais, endpoints e parÃ¢metros.

**Riscos:**
- INT-001 (Movidesk): API pode ter limitaÃ§Ãµes nÃ£o documentadas.
- INT-005 (n8n): Adiciona complexidade de deploy (Docker).
- INT-007 (Qdrant): Requer Docker e memÃ³ria adicional.

**DÃºvidas em aberto:**
- O n8n Ã© necessÃ¡rio no MVP ou podemos implementar automaÃ§Ãµes diretamente no Hermes?
- Precisamos de integraÃ§Ã£o com alguma outra ferramenta nÃ£o listada? (CRM, ERP, WhatsApp?)

**PrÃ³ximos passos:**
- Especificar SeguranÃ§a e Privacidade.
- Detalhar Agentes.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

