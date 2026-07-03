---
title: "MVP"
description: "Escopo do MVP: criterios, funcionalidades, estimativa e entregaveis"
status: "concluido"
---

# MVP

> **Escopo mÃ­nimo viÃ¡vel para a primeira entrega do sistema.**
> O MVP deve entregar valor real (reduÃ§Ã£o de tempo burocrÃ¡tico) com o mÃ­nimo de complexidade.

---

## CritÃ©rios para InclusÃ£o no MVP

1. **Valor percebido:** Resolve uma dor real do dia a dia.
2. **Viabilidade tÃ©cnica:** Pode ser implementado em tempo razoÃ¡vel.
3. **IndependÃªncia:** NÃ£o depende de funcionalidades ainda nÃ£o implementadas.
4. **Testabilidade:** Pode ser testado e validado rapidamente.

---

## Escopo do MVP

> As funcionalidades listadas sÃ£o detalhadas em [[02-Requisitos/Requisitos-Funcionais.md]] e priorizadas no [[06-Planejamento/Backlog.md]].

### O Que Entra

| # | Funcionalidade | RFs | Agente | DependÃªncias |
|---|---------------|-----|--------|:------------:|
| 1 | **CLI BÃ¡sica** â€” Comandos essenciais (iniciar sessÃ£o, gravar Ã¡udio, transcrever, registrar) | RF-ACOMP-001, RF-ACOMP-002, RF-UI-001, RF-UI-002, RF-UI-003 | â€” | â€” |
| 2 | **GravaÃ§Ã£o de Ãudio** â€” Iniciar/parar com confirmaÃ§Ã£o e indicador visual | RF-AUDIO-001 a 005 | â€” | Hardware Ã¡udio |
| 3 | **TranscriÃ§Ã£o e Resumo** â€” Transcrever Ã¡udio e extrair pontos-chave | RF-TRANS-001 a 004 | A01 â€” TranscriÃ§Ã£o | Whisper (API) |
| 4 | **Registro no Obsidian** â€” Salvar conhecimento estruturado com aprovaÃ§Ã£o | RF-MEM-001 a 004 | A02 â€” MemÃ³ria | Obsidian vault |
| 5 | **SugestÃ£o de Fechamento de OS** â€” Gerar resumo tÃ©cnico para Movidesk | RF-OS-001, RF-OS-002, RF-OS-003 | A03 â€” DocumentaÃ§Ã£o | Movidesk API |
| 6 | **SugestÃ£o de E-mail (Compra/Comunicado)** â€” Gerar minutas para aprovaÃ§Ã£o | RF-EMAIL-001 a 003 | A04 â€” ComunicaÃ§Ã£o | â€” |
| 7 | **Painel de AprovaÃ§Ãµes** â€” Revisar e aprovar/rejeitar aÃ§Ãµes pendentes | RF-SEG-001, RF-SEG-004, RF-UI-003 | â€” | â€” |
| 8 | **Log de Auditoria** â€” Registro de todas as aÃ§Ãµes | RF-SEG-003 | â€” | PostgreSQL |
| 9 | **Banco Vetorial (Qdrant)** â€” IndexaÃ§Ã£o e busca semÃ¢ntica bÃ¡sica | RF-CONSULTA-002, RF-IA-001 | A05 â€” Consulta | Qdrant |
| 10 | **IntegraÃ§Ã£o com Movidesk** â€” Consultar e atualizar chamados | RF-INT-001, RF-OS-005 | â€” | [[04-Arquitetura/Movidesk-API.md\|Movidesk API]] |

### O Que NÃƒO Entra no MVP

| Funcionalidade | Motivo |
|----------------|--------|
| IntegraÃ§Ã£o com n8n | Complexidade adicional; automaÃ§Ãµes podem ser implementadas diretamente no Hermes no MVP |
| Interface Web | CLI Ã© suficiente para o usuÃ¡rio tÃ©cnico; web adiciona complexidade |
| MÃºltiplos LLM providers | Um provider (ex.: Claude) Ã© suficiente; fallback pode vir depois |
| Backup automÃ¡tico do Obsidian | Pode ser manual via git no inÃ­cio |
| Interface para TÃ©cnico Parceiro | Escopo de uso individual |
| Dashboard de mÃ©tricas | Pode vir depois com dados reais |
| Suporte offline completo | MVP depende de internet para LLM; funcionalidades locais continuam |
| PersonalizaÃ§Ã£o de templates de e-mail | Templates fixos no MVP, customizaÃ§Ã£o depois |
| Upload de fotos/vÃ­deos | MVP foca em Ã¡udio e texto; mÃ­dia visual depois |

---

## Arquitetura Simplificada do MVP

```mermaid
flowchart TD
    CLI[CLI Interface] --> HERMES[Hermes Core]
    HERMES --> WH[Whisper API]
    HERMES --> LLM[LLM API]
    HERMES --> OBS[Obsidian Vault]
    HERMES --> MOV[Movidesk API]
    HERMES --> QD[Qdrant]
    HERMES --> PG[(PostgreSQL)]
```

### Componentes do MVP vs PÃ³s-MVP

| Componente | MVP | PÃ³s-MVP |
|------------|:---:|:-------:|
| CLI Interface | âœ… | âœ… |
| Core Engine | âœ… | âœ… |
| Audio Recorder | âœ… | âœ… |
| Transcriber (Whisper API) | âœ… (API) | âœ… + Local |
| LLM Client | âœ… (1 provider) | âœ… (mÃºltiplos) |
| Memory Manager (Obsidian) | âœ… | âœ… |
| Movidesk Client | âœ… | âœ… |
| Email Service | âœ… (SMTP direto) | âœ… + n8n |
| Vector Store (Qdrant) | âœ… (bÃ¡sico) | âœ… + refinamento |
| PostgreSQL | âœ… (essencial) | âœ… + manutenÃ§Ã£o |
| Redis | âŒ (opcional) | âœ… |
| n8n Integration | âŒ | âœ… |
| Banco Vetorial avanÃ§ado | âŒ | âœ… |
| Interface Web | âŒ | âœ… |

---

## Estimativa de EsforÃ§o do MVP

| Funcionalidade | Estimativa | Depende de |
|----------------|:----------:|:----------:|
| 1 â€” CLI BÃ¡sica | 5 dias | â€” |
| 2 â€” GravaÃ§Ã£o de Ãudio | 3 dias | CLI |
| 3 â€” TranscriÃ§Ã£o e Resumo | 5 dias | GravaÃ§Ã£o, LLM |
| 4 â€” Registro no Obsidian | 4 dias | TranscriÃ§Ã£o |
| 5 â€” SugestÃ£o Fechamento OS | 3 dias | TranscriÃ§Ã£o, LLM |
| 6 â€” SugestÃ£o E-mail | 2 dias | LLM |
| 7 â€” Painel de AprovaÃ§Ãµes | 3 dias | CLI |
| 8 â€” Log de Auditoria | 2 dias | â€” |
| 9 â€” Banco Vetorial | 4 dias | Obsidian |
| 10 â€” IntegraÃ§Ã£o Movidesk | 3 dias | â€” |
| **Total (estimativa)** | **~34 dias Ãºteis** | ~7 semanas |

> **Nota:** Estimativas consideram desenvolvimento em tempo parcial. Refinar com POC de cada tecnologia.

---

## CritÃ©rios de AceitaÃ§Ã£o do MVP

| CritÃ©rio | MÃ©trica |
|----------|---------|
| Fluxo completo funcional | Conseguir: iniciar sessÃ£o â†’ gravar Ã¡udio â†’ transcrever â†’ registrar no Obsidian â†’ sugerir fechamento de OS |
| ReduÃ§Ã£o de tempo em burocracia | ReduÃ§Ã£o de pelo menos 30% no tempo de fechamento de OS |
| Nenhuma aÃ§Ã£o automÃ¡tica | Zero aÃ§Ãµes executadas sem aprovaÃ§Ã£o do usuÃ¡rio |
| Estabilidade | Sistema nÃ£o crasha durante uso normal |

---

## EntregÃ¡veis do MVP

1. CÃ³digo-fonte funcional do Hermes (core + CLI)
2. Vault do Obsidian estruturado com modelos
3. DocumentaÃ§Ã£o de uso do sistema
4. Script de setup (instalaÃ§Ã£o de dependÃªncias, configuraÃ§Ã£o)

---

**Premissas:**
- O MVP serÃ¡ iterativo: funcionalidades podem ser entregues em ondas dentro do MVP.
- O usuÃ¡rio participarÃ¡ ativamente da validaÃ§Ã£o de cada funcionalidade.

**Riscos:**
- DependÃªncia de API do Movidesk pode atrasar a funcionalidade de fechamento de OS.
- Qualidade da transcriÃ§Ã£o pode nÃ£o atender Ã s expectativas iniciais.

**DÃºvidas em aberto:**
- Deve ser criada uma POC (prova de conceito) para validar a integraÃ§Ã£o com Movidesk antes de iniciar o MVP?
- A estimativa de 34 dias Ã© realista para desenvolvimento em paralelo com o trabalho?

**PrÃ³ximos passos:**
- Detalhar Backlog priorizado.
- Criar Roadmap.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

