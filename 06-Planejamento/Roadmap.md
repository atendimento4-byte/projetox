---
title: "Roadmap"
description: "4 ondas (10 semanas) + Pos-MVP com marcos e timeline"
status: "concluido"
---

# Roadmap

> **Cronograma macro de entregas e marcos do projeto.**
>
> Este roadmap organiza as entregas do [[06-Planejamento/Backlog.md|Backlog]] e define os marcos do [[06-Planejamento/MVP.md|MVP]].
> O progresso Ã© acompanhado pelo [[06-Planejamento/Checklist-MVP.md|Checklist MVP]].

---

## VisÃ£o Geral

```mermaid
gantt
    title Roadmap Hermes + Obsidian
    dateFormat  YYYY-MM-DD
    
    section Sprint 0 - FundaÃ§Ã£o
    Setup repositÃ³rio/ambiente (B-001 a B-006) :2026-07-06, 5d
    CI bÃ¡sico (B-007)                         :2026-07-06, 5d
    
    section MVP - Onda 1 (Semanas 2-4)
    CLI estrutura/comandos (B-008 a B-010)    :crit, 2026-07-13, 10d
    GravaÃ§Ã£o de Ã¡udio (B-011 a B-014)         :2026-07-20, 5d
    Hotkeys + status (B-015 a B-017)          :2026-07-27, 3d
    
    section MVP - Onda 2 (Semanas 4-7)
    Whisper + LLM (B-018 a B-022)             :crit, 2026-07-27, 10d
    Registro Obsidian (B-027 a B-036)         :2026-08-03, 10d
    RevisÃ£o/tratamento erros (B-023 a B-026)  :2026-08-10, 5d
    
    section MVP - Onda 3 (Semanas 7-9)
    IntegraÃ§Ã£o Movidesk (B-037)               :crit, 2026-08-10, 5d
    Fechamento de OS (B-038 a B-042)          :2026-08-17, 10d
    GeraÃ§Ã£o de e-mail (B-043 a B-047)         :2026-08-17, 5d
    
    section MVP - Onda 4 (Semanas 9-11)
    AprovaÃ§Ãµes e controle (B-048 a B-052)     :2026-08-24, 5d
    Busca semÃ¢ntica (B-053 a B-058)           :2026-08-24, 10d
    Testes e validaÃ§Ã£o final                  :2026-09-01, 5d
    
    section PÃ³s-MVP (Epics 7-10)
    Epic 7 - Estabilidade (B-059 a B-065)     :2026-09-08, 15d
    Epic 8 - n8n (B-066 a B-070)              :2026-09-22, 10d
    Epic 9 - Web (B-071 a B-074)              :2026-10-06, 20d
    Epic 10 - AvanÃ§ado (B-075 a B-082)        :2026-10-20, 30d
```

> **Legenda:** `crit` = item no caminho crÃ­tico (atraso aqui desliza o projeto)

---

## Caminho CrÃ­tico

As entregas abaixo estÃ£o no caminho crÃ­tico â€” qualquer atraso desliza o cronograma:

```
B-008 (CLI estrutura)  â†’  B-011 (gravaÃ§Ã£o)  â†’  B-018 (Whisper)
                                                     â†“
B-037 (Movidesk API)   â†’  B-038 (fechamento OS)   B-020 (LLM)
                                                     â†“
                                              B-027 (Obsidian)
                                                     â†“
                                              B-053 (Qdrant)
```

| Entrega | Bloqueia | Se atrasar |
|---------|----------|------------|
| B-008 a B-010 â€” CLI estrutura | Toda Onda 1 e 2 | +1 semana por item |
| B-018 â€” IntegraÃ§Ã£o Whisper | B-019 a B-026 (transcriÃ§Ã£o) | +2 dias |
| B-020 â€” IntegraÃ§Ã£o LLM | B-021 a B-026, B-038, B-043 | +3 dias |
| B-037 â€” IntegraÃ§Ã£o Movidesk | B-038 a B-042 (fechamento) | +3-5 dias |
| B-027 â€” IntegraÃ§Ã£o Obsidian | B-028 a B-036, B-053 | +2 dias |

> Para detalhes de cada item, consulte [[06-Planejamento/Backlog.md]].

---

## Marcos (Milestones)

| Marco | Data | Status | Checklist | Entregas |
|-------|:----:|:------:|:---------:|----------|
| **M1 â€” Setup Completo** | 10/07/2026 | ðŸ”´ | â€” | B-001 a B-007: repositÃ³rio, ambiente, Docker, vault, estrutura de dados, CI |
| **M2 â€” GravaÃ§Ã£o Funcional** | 24/07/2026 | ðŸ”´ | Func. 1-2 | B-008 a B-017: CLI operacional, comandos iniciar/finalizar, gravaÃ§Ã£o com confirmaÃ§Ã£o, indicador visual, hotkeys |
| **M3 â€” TranscriÃ§Ã£o e Resumo** | 07/08/2026 | ðŸ”´ | Func. 3 | B-018 a B-022, B-025: Whisper API, LLM, transcriÃ§Ã£o, resumo estruturado |
| **M4 â€” MemÃ³ria no Obsidian** | 14/08/2026 | ðŸ”´ | Func. 5 | B-027 a B-036: integraÃ§Ã£o vault, anÃ¡lise de entidades, notas com template e links, aprovaÃ§Ã£o |
| **M5 â€” Fechamento de OS** | 21/08/2026 | ðŸ”´ | Func. 8 | B-037 a B-042: integraÃ§Ã£o Movidesk, sugestÃ£o de fechamento, gestÃ£o de status, envio |
| **M6 â€” GeraÃ§Ã£o de E-mail** | 28/08/2026 | ðŸ”´ | Func. 9 | B-043 a B-047: minutas de e-mail (compra e comunicado), envio com aprovaÃ§Ã£o |
| **M7 â€” Busca SemÃ¢ntica** | 04/09/2026 | ðŸ”´ | Func. 6 | B-053 a B-058: indexaÃ§Ã£o Qdrant, busca, histÃ³rico, ranqueamento |
| **M8 â€” MVP Completo** | 11/09/2026 | ðŸ”´ | Func. 1-10 | Sistema funcional ponta a ponta: M1 a M7 integrados, validaÃ§Ã£o com uso real |
| **M9 â€” EstabilizaÃ§Ã£o** | 25/09/2026 | ðŸ”´ | â€” | B-059 a B-065: Redis, fallback Whisper local, testes, backup, criptografia |
| **M10 â€” AutomaÃ§Ãµes** | 06/10/2026 | ðŸ”´ | â€” | B-066 a B-070: n8n configurado, workflows de integraÃ§Ã£o |
| **M11 â€” Interface Web** | 30/10/2026 | ðŸ”´ | â€” | B-071 a B-074: API REST, Web App bÃ¡sico |
| **M12 â€” Features AvanÃ§adas** | 30/11/2026 | ðŸ”´ | â€” | B-075 a B-082: sugestÃ£o proativa, dashboard, app tÃ©cnico (parcial) |

> **Status:** ðŸ”´ nÃ£o iniciado | ðŸŸ¡ em andamento | ðŸŸ¢ concluÃ­do

---

## Ondas de Entrega

### Onda 1 â€” FundaÃ§Ã£o e Ãudio (Semanas 1-3, 06/07 a 26/07)
**Foco:** CLI bÃ¡sica funcional e gravaÃ§Ã£o de Ã¡udio com seguranÃ§a

**Itens do Backlog:** B-001 a B-017

| Semana | PerÃ­odo | Sprint | Entregas |
|--------|---------|--------|----------|
| Semana 1 | 06-10/07 | Sprint 0 | B-001 a B-007: repositÃ³rio, ambiente Python, Docker (Postgres + Qdrant), vault Obsidian, estrutura de dados, CI bÃ¡sico |
| Semana 2 | 13-17/07 | Sprint 1 | B-008 a B-010: CLI com Typer, comandos `iniciar`, `finalizar`, `status` |
| Semana 3 | 20-24/07 | Sprint 2 | B-011 a B-017: gravaÃ§Ã£o com confirmaÃ§Ã£o, indicador visual, hotkey Ctrl+Shift+R, pausa/retorno |

**DependÃªncias:** Nenhuma externa. Hardware de Ã¡udio necessÃ¡rio.

---

### Onda 2 â€” IA e MemÃ³ria (Semanas 4-6, 27/07 a 16/08)
**Foco:** TranscriÃ§Ã£o, resumo e registro de conhecimento no Obsidian

**Itens do Backlog:** B-018 a B-036

| Semana | PerÃ­odo | Sprint | Entregas |
|--------|---------|--------|----------|
| Semana 4 | 27-31/07 | Sprint 3 | B-018 a B-022: integraÃ§Ã£o Whisper API, LLM, comando `transcrever`, `resumir`, resumo estruturado |
| Semana 5 | 03-07/08 | Sprint 4 | B-027 a B-033: integraÃ§Ã£o vault, anÃ¡lise de entidades, criaÃ§Ã£o de notas com template, links |
| Semana 6 | 10-14/08 | Sprint 5 | B-023 a B-026, B-034 a B-036: tratamento de erros, cache LLM, aprovaÃ§Ã£o/ediÃ§Ã£o, templates de nota |

**DependÃªncias:** Chaves de API (Whisper, Anthropic). Onda 1 completa (CLI + gravaÃ§Ã£o).

> Nota: B-024 (transcriÃ§Ã£o parcial) e B-026 (cache LLM) sÃ£o P2 â€” podem ser diferidos se o tempo apertar.

---

### Onda 3 â€” DocumentaÃ§Ã£o e IntegraÃ§Ãµes (Semanas 7-9, 17/08 a 06/09)
**Foco:** Fechamento de OS, e-mails, integraÃ§Ã£o com Movidesk

**Itens do Backlog:** B-037 a B-047

| Semana | PerÃ­odo | Sprint | Entregas |
|--------|---------|--------|----------|
| Semana 7 | 17-21/08 | Sprint 6 | B-037: POC + integraÃ§Ã£o API Movidesk (consulta de chamados). **Item crÃ­tico.** |
| Semana 8 | 24-28/08 | Sprint 7 | B-038 a B-042, B-047: sugestÃ£o de fechamento, resumo tÃ©cnico, definiÃ§Ã£o de status, envio |
| Semana 9 | 31/08-04/09 | Sprint 8 | B-043 a B-046: geraÃ§Ã£o de e-mail (compra + comunicado), templates, rascunho |

**DependÃªncias:** Token de API do Movidesk. Onda 2 completa (transcriÃ§Ã£o + Obsidian).

> **Risco:** Se a API do Movidesk for complexa, B-037 pode consumir toda a Semana 7. Buffer de 2 dias alocado.

---

### Onda 4 â€” FinalizaÃ§Ã£o do MVP (Semanas 10-11, 07/09 a 19/09)
**Foco:** AprovaÃ§Ãµes, busca, testes e ajustes finais

**Itens do Backlog:** B-048 a B-058

| Semana | PerÃ­odo | Sprint | Entregas |
|--------|---------|--------|----------|
| Semana 10 | 07-11/09 | Sprint 9 | B-048 a B-052: fila de aprovaÃ§Ãµes, comandos `pendentes`, `aprovar`, `editar`, `rejeitar`, log de auditoria |
| Semana 11 | 14-18/09 | Sprint 10 | B-053 a B-058: indexaÃ§Ã£o Qdrant, comando `buscar`, `historico`, ranqueamento. Testes de integraÃ§Ã£o |

**DependÃªncias:** Ondas 1-3 completas. Qdrant rodando.

---

### PÃ³s-MVP (Semanas 12+, 21/09 em diante)

**Itens do Backlog:** B-059 a B-082

| PerÃ­odo | Epic | Itens | Entregas |
|---------|:----:|:-----:|----------|
| Semanas 12-14 (21/09 a 11/10) | **Epic 7 â€” Estabilidade** | B-059 a B-065 | Redis, fallback Whisper local, mÃºltiplos providers LLM, testes automatizados, backup, criptografia |
| Semanas 15-16 (12/10 a 25/10) | **Epic 8 â€” n8n** | B-066 a B-070 | Setup n8n, workflows de e-mail, Movidesk, backup, webhook |
| Semanas 17-20 (26/10 a 22/11) | **Epic 9 â€” Web** | B-071 a B-074 | API REST FastAPI, Web App bÃ¡sico, notificaÃ§Ãµes WebSocket, upload mÃ­dia |
| Semanas 21-25 (23/11 a 27/12) | **Epic 10 â€” AvanÃ§ado** | B-075 a B-082 | SugestÃ£o proativa, grafo de conhecimento, dashboard, multi-usuÃ¡rio, app tÃ©cnico, WhatsApp, calendÃ¡rio, exportaÃ§Ã£o |

---

## Riscos do Cronograma

| Risco | Impacto | Probabilidade | MitigaÃ§Ã£o |
|-------|:-------:|:-------------:|-----------|
| Complexidade da API do Movidesk subestimada | Atraso na Onda 3 | MÃ©dia | POC dedicada na Semana 7; buffer de 2 dias alocado |
| Qualidade do Whisper abaixo do esperado | Retrabalho na Onda 2 | MÃ©dia | Testar com amostras reais na Semana 4; fallback Whisper local no PÃ³s-MVP |
| DependÃªncia de LLM (custo/disponibilidade) | Atraso geral | Baixa | Ter chave reserva; cache de respostas (B-026) |
| Escopo maior que o estimado | Atraso geral | Alta | RevisÃ£o semanal; cortar itens P1 se necessÃ¡rio |
| Disponibilidade reduzida do usuÃ¡rio para validaÃ§Ã£o | Atraso em todas as ondas | MÃ©dia | ValidaÃ§Ãµes assÃ­ncronas sempre que possÃ­vel |
| Problemas de ambiente (Windows Service, Named Pipe) | Atraso na Onda 1 | Baixa | POC do Named Pipe antes do Sprint 1 |

---

## Premissas

- **DedicaÃ§Ã£o:** Desenvolvimento contÃ­nuo em tempo parcial (~20h/semana), sem pausas planejadas entre ondas.
- **Deadline:** Sem data fixa. O MVP serÃ¡ considerado pronto quando passar nos [[06-Planejamento/Checklist-MVP.md|c critÃ©rios do Checklist MVP]].
- **ValidaÃ§Ã£o:** O usuÃ¡rio valida cada funcionalidade dentro da semana de entrega.
- **DependÃªncias externas:** Chaves de API (Whisper, LLM, Movidesk) disponÃ­veis antes do inÃ­cio de cada onda.
- **Feriados:** Sem feriados relevantes no perÃ­odo. Se houver, o cronograma desliza proporcionalmente.
- **Refinamento:** As estimativas serÃ£o ajustadas conforme o progresso real. Este roadmap Ã© um guia, nÃ£o uma promessa.

---

## Registro de Ajustes

| Data | Ajuste | Motivo |
|------|--------|--------|
| â€” | â€” | â€” |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

