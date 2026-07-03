---
title: "Indice do SDD"
description: "Indice geral de navegacao da documentacao do projeto"
status: "concluido"
---

# Ãndice do Software Design Document â€” Hermes + Obsidian

> **Ãndice geral de navegaÃ§Ã£o da documentaÃ§Ã£o do projeto.**
>
> **Legenda:** âœ… concluÃ­do | ðŸ†• novo

---

## MÃ©tricas do Projeto

| MÃ©trica                            | Valor             |
| ---------------------------------- | ----------------- |
| **Documentos** | 49 |
| **Requisitos Funcionais**          | 38 (11 mÃ³dulos)   |
| **Requisitos NÃ£o Funcionais**      | 23 (7 categorias) |
| **Casos de Uso**                   | 10                |
| **DecisÃµes de Arquitetura (ADRs)** | 15                |
| **Componentes do Sistema**         | 13                |
| **Riscos Mapeados**                | 11 (4 categorias) |
| **Objetivos EspecÃ­ficos**          | 7                 |
| **Agentes de IA** | 5             |
| **Diagramas Mermaid**              | 15                |
| **Total de Linhas**                | ~11.200            |
| **Skills do Hermes (prompts)**      | 14                |
| **Palavras (estimado)**            | ~125.000           |

---

## Mapa de ConexÃµes dos Documentos

```mermaid
graph TD
    classDef fund fill:#e1f5fe
    classDef req fill:#fff3e0
    classDef comp fill:#f3e5f5
    classDef arq fill:#e8f5e9
    classDef dados fill:#fce4ec
    classDef plan fill:#fff8e1
    classDef enri fill:#e0f2f1

    G["GlossÃ¡rio"]:::fund
    V["VisÃ£o Geral"]:::fund
    O["Objetivos"]:::fund
    P["Personas"]:::fund
    RF["Requisitos Funcionais"]:::req
    RN["Requisitos NÃ£o Funcionais"]:::req
    UC["Casos de Uso"]:::req
    FX["Fluxos"]:::comp
    RS["Riscos"]:::comp
    AD["ADRs"]:::arq
    AQ["Arquitetura"]:::arq
    CP["Componentes"]:::arq
    CF["ConfiguraÃ§Ã£o"]:::arq
    OP["OperaÃ§Ã£o"]:::arq
    IN["IntegraÃ§Ãµes"]:::arq
    SG["SeguranÃ§a"]:::arq
    PV["Privacidade"]:::arq
    AG["Agentes"]:::arq
    BD["Banco de Dados"]:::dados
    MO["MemÃ³ria Obsidian"]:::dados
    MV["MVP"]:::plan
    BL["Backlog"]:::plan
    RD["Roadmap"]:::plan
    EF["EvoluÃ§Ã£o Futura"]:::plan
    CK["Checklist MVP"]:::plan
    ST["Setup"]:::enri
    MR["Matriz Rastreab."]:::enri
    DP["DecisÃµes Pend."]:::enri
    CV["ConvenÃ§Ãµes"]:::enri
    GI["GlossÃ¡rio Ilustrado"]:::enri

    O --> RF
    O --> RN
    P --> UC
    G --> UC
    RF --> UC
    RN --> UC
    UC --> FX
    FX --> RS
    RS --> AD
    AD --> AQ
    AD --> CP
    AD --> CF
    AD --> OP
    AD --> IN
    AD --> SG
    AD --> AG
    AG --> MO
    CP --> MO
    IN --> MO
    BD --> MO
    SG --> PV
    BD --> SG
    BD --> PV
    RF --> MV
    MV --> BL
    BL --> RD
    RD --> EF
    MV --> CK
    AQ --> CV
    OP --> CV
    CF --> ST
    OP --> ST
    AD --> MR
    RF --> MR
    UC --> MR
    FX --> MR
    MO --> GI
    AQ --> GI
    CP --> GI
```

---

## NavegaÃ§Ã£o RÃ¡pida

| Tipo | Documentos |
|------|-----------|
| **FundaÃ§Ã£o** | 1-4: GlossÃ¡rio, VisÃ£o, Objetivos, Personas |
| **Requisitos** | 5-7: RFs, RNFs, Casos de Uso |
| **Comportamento** | 8-9: Fluxos, Riscos |
| **Arquitetura** | 10-19: ADRs, Arquitetura, Componentes, Config, OperaÃ§Ã£o, IntegraÃ§Ãµes, Movidesk-API, SeguranÃ§a, Privacidade, Agentes |
| **Dados** | 20-21: Banco de Dados, MemÃ³ria Obsidian |
| **Planejamento** | 22-26: MVP, Backlog, Roadmap, EvoluÃ§Ã£o, Checklist |
| **Enriquecimento** | 27-32: Setup, Matriz, DecisÃµes, ConvenÃ§Ãµes, GlossÃ¡rio Ilustrado, Estrutura Projeto |
| **Testes** | 33-45: EstratÃ©gia, Plano, ValidaÃ§Ã£o, Checklist, SimulaÃ§Ã£o, Falhas, CritÃ©rios, Gates, Rollback, Limites, MÃ©tricas, Dados, Mocks |
| **OrquestraÃ§Ã£o (Hermes)** | 46-49: ConstituiÃ§Ã£o, Skills, Ref RÃ¡pida, Bootstrap |

**Leitura recomendada:**
- **Primeiros passos:** GlossÃ¡rio > VisÃ£o Geral > Objetivos > Personas
- **ImplementaÃ§Ã£o:** ADRs > Arquitetura > Componentes > OperaÃ§Ã£o > ConfiguraÃ§Ã£o
- **Planejamento:** MVP > Backlog > Roadmap > Checklist MVP
- **VisÃ£o completa do dado:** Banco de Dados > MemÃ³ria Obsidian
- **Testes e validaÃ§Ã£o:** EstratÃ©gia > Plano > ValidaÃ§Ã£o Loop > SimulaÃ§Ã£o > Mocks
- **OrquestraÃ§Ã£o (Hermes):** Bootstrap (primeiro comando) > Skills (prompts) > ConstituiÃ§Ã£o (workflow) > Logs (handover)

---

## Fase 1 â€” FundaÃ§Ã£o

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 1 | [[01-Fundacao/Glossario.md\|GlossÃ¡rio]] | 25+ termos, 5 categorias (DomÃ­nio, Status OS, Componentes, AÃ§Ãµes, Dados) | concluÃ­do |
| 2 | [[01-Fundacao/Visao-Geral.md\|VisÃ£o Geral]] | PropÃ³sito, Contexto atual, O que faz, Tecnologias, PÃºblico, CritÃ©rios | concluÃ­do |
| 3 | [[01-Fundacao/Objetivos.md\|Objetivos]] | 1 Objetivo Geral, 7 OE, 4 ONFs com mÃ©tricas | concluÃ­do |
| 4 | [[01-Fundacao/Personas.md\|Personas]] | 3 personas (Supervisor, TÃ©cnico, Cliente), CenÃ¡rios, Matriz vs Funcionalidades | concluÃ­do |

## Fase 2 â€” Requisitos

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 5 | [[02-Requisitos/Requisitos-Funcionais.md\|Requisitos Funcionais]] | 38 RFs, 11 mÃ³dulos (ACOMP, AUDIO, TRANS, MEM, OS, EMAIL, IA, CONSULTA, SEG, INT, UI) | concluÃ­do |
| 6 | [[02-Requisitos/Requisitos-Nao-Funcionais.md\|Requisitos NÃ£o Funcionais]] | 23 RNFs, 7 categorias (DES, DISP, SEG, PRIV, USA, MAN, PORT), Matriz de prioridades | concluÃ­do |
| 7 | [[02-Requisitos/Casos-de-Uso.md\|Casos de Uso]] | 10 UCs (UC-001 a UC-010), 4 atores, Fluxo principal + alternativos + regras de negÃ³cio | concluÃ­do |

## Fase 3 â€” Comportamento & Riscos

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 8 | [[03-Comportamento/Fluxos.md\|Fluxos]] | 7 fluxos (Macro, GravaÃ§Ã£o, Registro, Fechamento OS, E-mail, Consulta, AprovaÃ§Ãµes), 7 diagramas Mermaid | concluÃ­do |
| 9 | [[03-Comportamento/Riscos.md\|Riscos]] | 11 riscos (6 tÃ©cnicos, 3 seguranÃ§a, 2 projeto, 1 negÃ³cio), Matriz com ADRs vinculadas | concluÃ­do |

## Fase 4 â€” Arquitetura & Componentes

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 10 | [[04-Arquitetura/ADRs.md\|DecisÃµes de Arquitetura (ADRs)]] | 15 ADRs (ADR-001 a 015), Cada uma com Contexto, OpÃ§Ãµes, DecisÃ£o, Vantagens, Desvantagens | concluÃ­do |
| 11 | [[04-Arquitetura/Arquitetura.md\|Arquitetura Geral]] | Hexagonal (Ports & Adapters), Processos, MÃ¡quina de estados, ConcorrÃªncia async, Startup/Shutdown, Hierarquia de erros, Logging, Stack, Diagrama de pacotes | concluÃ­do |
| 12 | [[04-Arquitetura/Componentes.md\|Componentes]] | 13 componentes (C01-C13), Cada um com Interface (Port) + ImplementaÃ§Ã£o (Adapter) + DependÃªncias + Matriz | concluÃ­do |
| 13 | [[04-Arquitetura/Configuracao.md\|Sistema de ConfiguraÃ§Ã£o]] | YAML centralizado, JSON Schema, ResoluÃ§Ã£o de secrets (env + Credential Manager), Perfis, CLI | concluÃ­do |
| 14 | [[04-Arquitetura/Operacao.md\|OperaÃ§Ã£o do Sistema]] | Windows Service, Named Pipe IPC (:8790), JSON-RPC, 40+ comandos CLI, 20 hotkeys, TUI, Monitoramento, ExpansÃ£o TCP futura | concluÃ­do |
| 15 | [[04-Arquitetura/Integracoes.md\|IntegraÃ§Ãµes]] | 8 integraÃ§Ãµes (Movidesk, Obsidian, E-mail, LLM, n8n, Whisper, Qdrant, Ãudio), Matriz completa | concluÃ­do |
| 16 | [[04-Arquitetura/Movidesk-API.md\|API Movidesk (ReferÃªncia)]] | Schema completo do ticket, sub-recursos, OData filters, exemplos JSON, mapeamento C08 | novo |
| 17 | [[04-Arquitetura/Seguranca.md\|SeguranÃ§a]] | AutenticaÃ§Ã£o, Criptografia (repouso/trÃ¢nsito), Controle de acesso, Logs de auditoria, Backup, Resposta a incidentes | concluÃ­do |
| 18 | [[04-Arquitetura/Privacidade.md\|Privacidade]] | Dados coletados, Consentimento, LGPD, RetenÃ§Ã£o, MinimizaÃ§Ã£o, PseudonimizaÃ§Ã£o, Riscos de privacidade | concluÃ­do |
| 19 | [[04-Arquitetura/Agentes.md\|Agentes de IA]] | 5 agentes (TranscriÃ§Ã£o, MemÃ³ria, DocumentaÃ§Ã£o, ComunicaÃ§Ã£o, Consulta), Prompts, Fluxos, Matriz de uso LLM, OrquestraÃ§Ã£o | concluÃ­do |

## Fase 5 â€” Dados & MemÃ³ria

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 20 | [[05-Dados/Banco-de-Dados.md\|Banco de Dados]] | PostgreSQL (DDL), Redis (cache/sessÃ£o), Qdrant (vetorial), Fluxo de dados, Backup, 2 diagramas Mermaid | concluÃ­do |
| 21 | [[05-Dados/Memoria-Obsidian.md\|MemÃ³ria (Obsidian)]] | Estrutura de pastas, 5 tipos de nota, Templates YAML, Regras de linking, Tags, Boas prÃ¡ticas, Exemplos reais | concluÃ­do |

## Fase 6 â€” Planejamento & EvoluÃ§Ã£o

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 22 | [[06-Planejamento/MVP.md\|MVP]] | CritÃ©rios, Escopo (entra/nÃ£o entra), Arquitetura simplificada, Componentes MVP vs PÃ³s-MVP, Estimativa, CritÃ©rios de aceitaÃ§Ã£o, EntregÃ¡veis | concluÃ­do |
| 23 | [[06-Planejamento/Backlog.md\|Backlog]] | Sprint 0 + 6 Epics MVP + 4 Epics PÃ³s-MVP, Dezenas de itens priorizados (P0/P1/P2/P3), Estimativas | concluÃ­do |
| 24 | [[06-Planejamento/Roadmap.md\|Roadmap]] | 4 ondas (10 semanas) + PÃ³s-MVP, Marcos, Timeline Mermaid, Riscos do cronograma | concluÃ­do |
| 25 | [[06-Planejamento/Evolucao-Futura.md\|EvoluÃ§Ã£o Futura]] | ExpansÃ£o de pÃºblico, IA avanÃ§ada, IntegraÃ§Ãµes adicionais, Funcionalidades futuras, 3 cenÃ¡rios, Matriz de evoluÃ§Ã£o | concluÃ­do |
| 26 | [[06-Planejamento/Checklist-MVP.md\|Checklist MVP]] | 10 funcionalidades checkÃ¡veis, 39 itens de verificaÃ§Ã£o | novo |

## Fase 7 â€” Enriquecimento

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 27 | [[00-Index/Setup-Guia.md\|Guia de Setup]] | PrÃ©-requisitos, Docker Compose, Ambiente Python, Config inicial, VerificaÃ§Ã£o, Primeira execuÃ§Ã£o | novo |
| 28 | [[00-Index/Matriz-Rastreabilidade.md\|Matriz de Rastreabilidade]] | OEs vs RFs, RFs vs UCs, UCs vs Fluxos, Riscos vs ADRs, ADRs vs Arquitetura | novo |
| 29 | [[00-Index/Decisoes-Pendentes.md\|DecisÃµes Pendentes]] | 1 pendente (DP-001), 5 resolvidas (ADRs status, Persona, Chamado/OS, Porta) | novo |
| 30 | [[04-Arquitetura/Convencoes-Codigo.md\|ConvenÃ§Ãµes de CÃ³digo]] | 10 seÃ§Ãµes: DDD TÃ¡tico (Aggregate, VO, Event, Repository), Resultado[T,E], logging JSON, testes por camada, DI, pipeline CI/CD | concluÃ­do |
| 31 | [[01-Fundacao/Glossario-Ilustrado.md\|GlossÃ¡rio Ilustrado]] | 3 diagramas Mermaid: Ecossistema de Atores, Arquitetura Simplificada, Fluxo de Atendimento | novo |
| 32 | [[04-Arquitetura/Estrutura-Projeto.md\|Estrutura do Projeto]] | Ãrvore completa de diretÃ³rios, 5 bounded contexts, regras de dependÃªncia, checklist para novo contexto | novo |

## Fase 8 â€” Testes e ValidaÃ§Ã£o

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 33 | [[07-Testes/Estrategia-Testes.md\|EstratÃ©gia de Testes]] | PirÃ¢mide (unit â†’ fluxo â†’ integraÃ§Ã£o â†’ regressÃ£o â†’ recuperaÃ§Ã£o â†’ seguranÃ§a â†’ observabilidade â†’ performance â†’ escala), 10 categorias, modos Dry Run/Sandbox/SimulaÃ§Ã£o/ProduÃ§Ã£o | novo |
| 34 | [[07-Testes/Plano-Testes.md\|Plano de Testes]] | Matriz com 30+ testes por agente (A01-A05), orquestraÃ§Ã£o, fluxos, seguranÃ§a, observabilidade, humanos â€” ID, objetivo, prÃ©-condiÃ§Ãµes, entradas, resultado, prioridade | novo |
| 35 | [[07-Testes/Validacao-Loop.md\|ValidaÃ§Ã£o de Loop]] | 4 gates por iteraÃ§Ã£o (prÃ©-execuÃ§Ã£o, pÃ³s-LLM, pÃ³s-ferramenta, pÃ³s-aÃ§Ã£o), critÃ©rios de parada (normal/erro/intervenÃ§Ã£o), checkpoints com rollback | novo |
| 36 | [[07-Testes/Checklist-Loop.md\|Checklist de Loop]] | 10 seÃ§Ãµes de verificaÃ§Ã£o (riscos, cenÃ¡rios, limites, parada, testes, gates, agentes, auditoria, observabilidade, aprovaÃ§Ã£o final) | novo |
| 37 | [[07-Testes/Simulacao.md\|SimulaÃ§Ã£o]] | 4 modos de execuÃ§Ã£o: Dry Run (validaÃ§Ã£o), Sandbox (lÃ³gica), SimulaÃ§Ã£o (dados), ProduÃ§Ã£o (real). Tabela comparativa, critÃ©rios de aprovaÃ§Ã£o por modo | novo |
| 38 | [[07-Testes/Cenarios-Falha.md\|CenÃ¡rios de Falha]] | 13 cenÃ¡rios (LLM, timeout, ferramenta off, API off, autenticaÃ§Ã£o, arquivo, contexto, inconsistÃªncia, interrupÃ§Ã£o, loop infinito, dependÃªncia circular, memÃ³ria, cancelamento) com causa + detecÃ§Ã£o + recuperaÃ§Ã£o | novo |
| 39 | [[07-Testes/Criterios-Aceitacao.md\|CritÃ©rios de AceitaÃ§Ã£o]] | CritÃ©rios por tipo de teste, por agente (A01-A05), por funcionalidade MVP (1-10) | novo |
| 40 | [[07-Testes/Quality-Gates.md\|Quality Gates]] | 7 gates obrigatÃ³rios (requisitos â†’ planejamento â†’ contexto â†’ documentaÃ§Ã£o â†’ simulaÃ§Ã£o â†’ resultados â†’ aprovaÃ§Ã£o humana), quem aprova, automÃ¡tico ou manual | novo |
| 41 | [[07-Testes/Estrategia-Rollback.md\|EstratÃ©gia de Rollback]] | 4 nÃ­veis (N1 etapa, N2 iteraÃ§Ã£o, N3 loop, N4 sessÃ£o), mecanismo de compensaÃ§Ã£o, procedimento, log de rollback, limitaÃ§Ãµes | novo |
| 42 | [[07-Testes/Limites-Execucao.md\|Limites de ExecuÃ§Ã£o]] | Limites por loop (iteraÃ§Ãµes, tempo, LLM, ferramentas, custo, tokens), por ambiente (dry-run/sandbox/simulaÃ§Ã£o/produÃ§Ã£o), globais do sistema | novo |
| 43 | [[07-Testes/Metricas.md\|MÃ©tricas]] | MÃ©tricas de sucesso, performance, qualidade, custo, confiabilidade, observabilidade. Alertas com limiares. Formato JSON estruturado | novo |
| 44 | [[07-Testes/Dados-Teste.md\|Dados de Teste]] | 5 clientes fictÃ­cios, 5 chamados simulados, 2 transcriÃ§Ãµes sintÃ©ticas, e-mails de exemplo, 6 equipamentos mock. Factories e versionamento | novo |
| 45 | [[07-Testes/Servicos-Mock.md\|ServiÃ§os Mock]] | Mocks para Movidesk, Whisper, LLM, SMTP, Obsidian, Qdrant, Named Pipe. Comportamentos, cenÃ¡rios de erro, registro de chamadas para assertions | novo |

## Fase 9 â€” OrquestraÃ§Ã£o (Hermes externo + OpenCode)

| # | Documento | Destaques | Status |
|---|-----------|-----------|--------|
| 46 | [[00-Index/HERMES.md\|ConstituiÃ§Ã£o do Hermes]] | Identidade, workflow loop (Contextoâ†’Taskâ†’OpenCodeâ†’RevisÃ£oâ†’Docsâ†’Decidir), template de tarefa, sistema de 10 estados, governance layer, handover | novo |
| 47 | [[00-Index/Hermes-Skills.md\|Hermes Skills (12 prompts)]] | 12 templates de prompt para o Hermes externo: Context Loader, Task Manager, Reviewer, Doc Sync, Architecture Reviewer, ADR Manager, Memory, Research, OC Executor, Git, Testing, Quality Checker | novo |
| 48 | [[00-Index/Hermes-Ref.md\|Hermes Ref RÃ¡pida]] | Arquitetura externa, 12 skills, estados da task, regras, fluxo completo de trabalho | novo |
| 49 | [[00-Index/Bootstrap.md\|Bootstrap]] | Roteiro de primeira execuÃ§Ã£o: abrir Hermes (nousresearch.com), colar Context Loader, abrir OpenCode, ciclo de trabalho | novo |

---

