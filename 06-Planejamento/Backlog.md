---
title: "Backlog"
description: "Sprint 0 + 6 Epics MVP + 4 Epics Pos-MVP priorizados"
status: "concluido"
---

# Backlog

> **Lista priorizada de funcionalidades, melhorias e correÃ§Ãµes.**
>
> Este backlog implementa os [[02-Requisitos/Requisitos-Funcionais.md|Requisitos Funcionais]] e define o escopo do [[06-Planejamento/MVP.md|MVP]].
> Organizado por categorias e ordenado por prioridade dentro do MVP e pÃ³s-MVP.

---

## ConvenÃ§Ãµes

| Prioridade | Significado |
|:----------:|-------------|
| **P0** | Bloqueante â€” essencial para o MVP funcionar |
| **P1** | Importante â€” deve estar no MVP se possÃ­vel |
| **P2** | DesejÃ¡vel â€” pode ficar para pÃ³s-MVP |
| **P3** | Futuro â€” feature avanÃ§ada / melhoria |

---

## Sprint 0 â€” FundaÃ§Ã£o (Setup)

| ID | Item | Prioridade | EsforÃ§o | Depende de |
|----|------|:----------:|:-------:|:----------:|
| B-001 | Setup do projeto (repositÃ³rio git, estrutura de pastas) | P0 | 1 dia | â€” |
| B-002 | Setup do ambiente de desenvolvimento (Python/Node, dependÃªncias) | P0 | 1 dia | B-001 |
| B-003 | ConfiguraÃ§Ã£o do Obsidian vault (pastas, modelos) | P0 | 1 dia | â€” |
| B-004 | Setup do Qdrant (Docker) | P0 | 1 dia | â€” |
| B-005 | Setup do PostgreSQL (Docker ou local) | P0 | 1 dia | â€” |
| B-006 | DefiniÃ§Ã£o da estrutura de dados (tabelas PostgreSQL) | P0 | 2 dias | B-005 |
| B-007 | CI bÃ¡sico (lint, testes, build) | P2 | 1 dia | B-001 |

---

## MVP â€” Funcionalidades Core

### Ã‰pico 1: Acompanhamento e Ãudio

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-008 | CLI: estrutura de comandos (Click/Typer) | P0 | 3 dias | RF-UI-001 |
| B-009 | CLI: comando `iniciar` â€” nova sessÃ£o de acompanhamento | P0 | 2 dias | RF-ACOMP-001 |
| B-010 | CLI: comando `finalizar` â€” encerrar sessÃ£o | P0 | 1 dia | RF-ACOMP-002 |
| B-011 | GravaÃ§Ã£o: comando `gravar` â€” iniciar/parar gravaÃ§Ã£o | P0 | 2 dias | RF-AUDIO-001, 002 |
| B-012 | GravaÃ§Ã£o: confirmaÃ§Ã£o obrigatÃ³ria antes de iniciar | P0 | 1 dia | RF-SEG-002 |
| B-013 | GravaÃ§Ã£o: indicador visual de gravaÃ§Ã£o ativa | P0 | 1 dia | RF-AUDIO-003 |
| B-014 | GravaÃ§Ã£o: salvar Ã¡udio associado Ã  sessÃ£o | P0 | 1 dia | RF-AUDIO-004 |
| B-015 | CLI: hotkey para iniciar/parar gravaÃ§Ã£o | P1 | 2 dias | RF-UI-002 |
| B-016 | CLI: comando `pausar` / `retomar` gravaÃ§Ã£o | P2 | 1 dia | RF-AUDIO-005 |
| B-017 | CLI: comando `status` â€” exibir estado atual da sessÃ£o | P1 | 1 dia | RF-UI-004 |

### Ã‰pico 2: TranscriÃ§Ã£o e IA

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-018 | IntegraÃ§Ã£o com Whisper API | P0 | 2 dias | RF-TRANS-001 |
| B-019 | CLI: comando `transcrever` â€” transcrever Ã¡udio gravado | P0 | 1 dia | RF-TRANS-001 |
| B-020 | IntegraÃ§Ã£o com LLM (Claude/GPT) para extraÃ§Ã£o de pontos-chave | P0 | 3 dias | RF-TRANS-002 |
| B-021 | GeraÃ§Ã£o de resumo estruturado do atendimento | P0 | 2 dias | RF-TRANS-003 |
| B-022 | CLI: comando `resumir` â€” gerar e exibir resumo | P0 | 1 dia | RF-TRANS-003 |
| B-023 | RevisÃ£o e ediÃ§Ã£o manual do resumo antes de usar | P1 | 2 dias | RF-TRANS-004 |
| B-024 | TranscriÃ§Ã£o parcial (Ã¡udio ainda gravando) | P2 | 3 dias | RF-TRANS-001 |
| B-025 | Tratamento de erros na transcriÃ§Ã£o (falha, ruÃ­do) | P1 | 1 dia | â€” |
| B-026 | Cache de respostas do LLM (evitar reprocessar) | P2 | 2 dias | â€” |

### Ã‰pico 3: MemÃ³ria (Obsidian)

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-027 | IntegraÃ§Ã£o com vault do Obsidian (filesystem) | P0 | 2 dias | RF-MEM-001 |
| B-028 | CLI: comando `salvar` â€” registrar conhecimento no Obsidian | P0 | 2 dias | RF-MEM-001 |
| B-029 | AnÃ¡lise e identificaÃ§Ã£o de entidades (cliente, equipamento, soluÃ§Ã£o) | P0 | 3 dias | RF-MEM-002 |
| B-030 | CriaÃ§Ã£o de notas com estrutura correta (frontmatter + conteÃºdo) | P0 | 2 dias | RF-MEM-002 |
| B-031 | CriaÃ§Ã£o de links entre notas ([[link]]) | P0 | 1 dia | RF-MEM-003 |
| B-032 | DetecÃ§Ã£o de entidades existentes vs novas | P0 | 2 dias | RF-MEM-004 |
| B-033 | ExibiÃ§Ã£o de prÃ©via das alteraÃ§Ãµes propostas | P0 | 1 dia | RF-MEM-001 |
| B-034 | AprovaÃ§Ã£o/ediÃ§Ã£o/rejeiÃ§Ã£o antes de escrever | P0 | 2 dias | RF-SEG-001 |
| B-035 | AtualizaÃ§Ã£o de notas existentes (ex.: adicionar ao histÃ³rico) | P1 | 2 dias | RF-MEM-004 |
| B-036 | Templates de nota (criar modelos base) | P1 | 1 dia | â€” |

### Ã‰pico 4: DocumentaÃ§Ã£o e OS

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-037 | IntegraÃ§Ã£o com API do Movidesk (consultar chamado) | P0 | 3 dias | RF-INT-001 |
| B-038 | CLI: comando `fechar` â€” sugerir fechamento de OS | P0 | 2 dias | RF-OS-001 |
| B-039 | GeraÃ§Ã£o de resumo tÃ©cnico para OS via LLM | P0 | 2 dias | RF-OS-001 |
| B-040 | DefiniÃ§Ã£o de status (Resolvido vs Retorno da OS) | P0 | 1 dia | RF-OS-002, 003 |
| B-041 | PrÃ©via do fechamento para revisÃ£o | P0 | 1 dia | RF-OS-001 |
| B-042 | Envio do fechamento para o Movidesk (apÃ³s aprovaÃ§Ã£o) | P0 | 2 dias | RF-OS-005 |
| B-043 | CLI: comando `email-compra` â€” gerar solicitaÃ§Ã£o de compra | P0 | 2 dias | RF-EMAIL-001 |
| B-044 | CLI: comando `email-comunicado` â€” gerar comunicado | P0 | 2 dias | RF-EMAIL-002 |
| B-045 | Envio de e-mail via SMTP (apÃ³s aprovaÃ§Ã£o) | P1 | 2 dias | RF-EMAIL-004 |
| B-046 | Salvamento de rascunho de e-mail | P2 | 1 dia | RF-EMAIL-003 |
| B-047 | Anexos em e-mail (documento OS) | P2 | 2 dias | â€” |

### Ã‰pico 5: AprovaÃ§Ãµes e Controle

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-048 | GestÃ£o de aÃ§Ãµes pendentes (fila de aprovaÃ§Ãµes) | P0 | 2 dias | RF-SEG-004 |
| B-049 | CLI: comando `pendentes` â€” listar aÃ§Ãµes aguardando aprovaÃ§Ã£o | P0 | 1 dia | RF-UI-003 |
| B-050 | CLI: comandos `aprovar`, `editar`, `rejeitar`, `adiar` | P0 | 2 dias | RF-SEG-001 |
| B-051 | Log de auditoria (todas as aÃ§Ãµes) | P0 | 2 dias | RF-SEG-003 |
| B-052 | Feedback visual para cada ação executada | P1 | 1 dia | — |
| **B-083** | **CLI: `pendentes criar` — follow-up manual com responsável e prazo** | **P1** | **2 dias** | **—** |
| B-084 | Cron job de lembrete: notificar pendentes vencendo/vencidos | P2 | 1 dia | B-083 |

### Ã‰pico 6: Busca e Consulta

| ID | Item | Prioridade | EsforÃ§o | RF |
|----|------|:----------:|:-------:|:--:|
| B-053 | IndexaÃ§Ã£o do Obsidian no Qdrant (embeddings) | P0 | 3 dias | RF-CONSULTA-002 |
| B-054 | CLI: comando `buscar` â€” busca semÃ¢ntica na base | P0 | 2 dias | RF-CONSULTA-002 |
| B-055 | CLI: sugestÃ£o automÃ¡tica durante atendimento | P1 | 3 dias | RF-IA-001 |
| B-056 | CLI: comando `historico` â€” consultar histÃ³rico do cliente | P1 | 2 dias | RF-CONSULTA-001 |
| B-057 | Resposta a perguntas em linguagem natural | P2 | 4 dias | RF-IA-003 |
| B-058 | Ranqueamento de resultados por relevÃ¢ncia | P2 | 2 dias | â€” |

---

## PÃ³s-MVP

### Ã‰pico 7: Melhorias e Estabilidade

| ID | Item | Prioridade | EsforÃ§o |
|----|------|:----------:|:-------:|
| B-059 | Implementar Redis para cache e estado | P2 | 3 dias |
| B-060 | Fallback para Whisper local (whisper.cpp) | P2 | 5 dias |
| B-061 | MÃºltiplos provedores de LLM (fallback automÃ¡tico) | P2 | 3 dias |
| B-062 | Testes automatizados (unitÃ¡rios + integraÃ§Ã£o) | P1 | ContÃ­nuo |
| B-063 | Melhorias de performance (otimizar consultas, cache) | P2 | 3 dias |
| B-064 | Backup automÃ¡tico do vault do Obsidian | P2 | 2 dias |
| B-065 | Criptografia de gravaÃ§Ãµes e dados sensÃ­veis | P2 | 3 dias |

### Ã‰pico 8: AutomaÃ§Ã£o com n8n

| ID | Item | Prioridade | EsforÃ§o |
|----|------|:----------:|:-------:|
| B-066 | Setup do n8n (Docker) | P2 | 1 dia |
| B-067 | Workflow: envio de e-mail via n8n | P2 | 2 dias |
| B-068 | Workflow: atualizaÃ§Ã£o do Movidesk via n8n | P2 | 2 dias |
| B-069 | Workflow: backup do Obsidian | P3 | 1 dia |
| B-070 | Webhook de integraÃ§Ã£o Hermes â†’ n8n | P2 | 2 dias |

### Ã‰pico 9: Interface Web

| ID | Item | Prioridade | EsforÃ§o |
|----|------|:----------:|:-------:|
| B-071 | API REST do Hermes (FastAPI / Express) | P2 | 5 dias |
| B-072 | Web App bÃ¡sico (dashboard de acompanhamento) | P3 | 10 dias |
| B-073 | NotificaÃ§Ãµes em tempo real (WebSocket) | P3 | 5 dias |
| B-074 | Upload de fotos/vÃ­deos via interface | P3 | 3 dias |

### Ã‰pico 10: Features AvanÃ§adas

| ID | Item | Prioridade | EsforÃ§o |
|----|------|:----------:|:-------:|
| B-075 | SugestÃ£o proativa de soluÃ§Ãµes durante atendimento | P2 | 5 dias |
| B-076 | Grafo de conhecimento visual (relacionamentos) | P3 | 5 dias |
| B-077 | Dashboard de mÃ©tricas (tempo economizado, atendimentos) | P3 | 5 dias |
| B-078 | Suporte a mÃºltiplos usuÃ¡rios | P3 | 10 dias |
| B-079 | App mobile para tÃ©cnico parceiro (registrar fotos, assinar OS) | P3 | 15 dias |
| B-080 | IntegraÃ§Ã£o com WhatsApp | P3 | 8 dias |
| B-081 | IntegraÃ§Ã£o com calendÃ¡rio (agendamento de retornos) | P3 | 5 dias |
| B-082 | ExportaÃ§Ã£o de dados (relatÃ³rios, planilhas) | P3 | 3 dias |

---

## Resumo do Backlog

| Categoria | P0 | P1 | P2 | P3 | Total |
|-----------|:--:|:--:|:--:|:--:|:-----:|
| Sprint 0 â€” FundaÃ§Ã£o | 6 | â€” | 1 | â€” | 7 |
| Ã‰pico 1 â€” Acompanhamento | 6 | 2 | 2 | â€” | 10 |
| Ã‰pico 2 â€” TranscriÃ§Ã£o | 5 | 2 | 2 | â€” | 9 |
| Ã‰pico 3 â€” MemÃ³ria | 7 | 2 | â€” | â€” | 9 |
| Ã‰pico 4 â€” DocumentaÃ§Ã£o | 7 | 1 | 3 | â€” | 11 |
| Ã‰pico 5 â€” AprovaÃ§Ãµes | 4 | 1 | 2 | â€” | 7 |
| Ã‰pico 6 â€” Busca | 2 | 2 | 2 | â€” | 6 |
| PÃ³s-MVP | â€” | 1 | 12 | 16 | 29 |
| **Total** | **37** | **11** | **22** | **16** | **86** |

---

**Premissas:**
- Itens P0 sÃ£o obrigatÃ³rios para o MVP.
- Itens P1 sÃ£o desejÃ¡veis no MVP, dependendo do tempo disponÃ­vel.
- O backlog serÃ¡ refinado continuamente com feedback de uso.

**Riscos:**
- Estimativas de esforÃ§o sÃ£o aproximadas e podem variar.
- Novos itens podem surgir durante o desenvolvimento.

**DÃºvidas em aberto:**
- A ordem exata dos itens P0 deve ser refinada com base nas dependÃªncias tÃ©cnicas.
- Algum item P0 pode ser simplificado para reduzir escopo do MVP?

**PrÃ³ximos passos:**
- Criar Roadmap com timeline estimada.
- Definir prÃ³ximas iteraÃ§Ãµes.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

