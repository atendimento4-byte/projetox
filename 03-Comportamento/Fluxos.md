---
title: "Fluxos"
description: "7 fluxos com diagramas Mermaid"
status: "concluido"
---

# Fluxos

> **Diagramas e descriÃ§Ãµes dos fluxos do sistema (normais e alternativos).**
> Todos os fluxos abaixo representam o comportamento esperado do sistema.
>
> Estes fluxos implementam os [[02-Requisitos/Casos-de-Uso.md|Casos de Uso]] do sistema.

---

## Fluxo 1 â€” Macro do Atendimento Completo

```mermaid
flowchart TD
    A[Cliente contata setor de atendimento] --> B[Setor abre chamado no Movidesk]
    B --> C[Setor contacta tÃ©cnico parceiro]
    C --> D[TÃ©cnico parceiro vai ao local]
    D --> E[VocÃª inicia acompanhamento remoto]
    E --> F[ExecuÃ§Ã£o do serviÃ§o]
    F --> G{NecessÃ¡rio Ã¡udio?}
    G -->|Sim| H[Ativa gravaÃ§Ã£o de Ã¡udio]
    H --> I[Transcreve e resume]
    G -->|NÃ£o| I
    I --> J{NecessÃ¡rio registro de conhecimento?}
    J -->|Sim| K[Solicita registro no Obsidian]
    K --> L[Aprova/Altera e confirma]
    J -->|NÃ£o| L
    L --> M{NecessÃ¡rio e-mail?}
    M -->|Compra| N[Gera e-mail solicitaÃ§Ã£o de compra]
    M -->|Comunicado| O[Gera e-mail de comunicado]
    M -->|NÃ£o| P
    N --> P
    O --> P
    P[Fechamento de OS]
    P --> Q{TÃ©cnico parceiro?}
    Q -->|Sim| R[Sugere status Retorno da OS + gera documento]
    Q -->|NÃ£o| S[Sugere status Resolvido]
    R --> T[Supervisor revisa e aprova]
    S --> T
    T --> U[Atualiza Movidesk]
    U --> V[Anexa documento assinado?]
    V -->|Sim| W[Atualiza status para Resolvido]
    V -->|NÃ£o| X[Aguardando documento]
    X --> V
```

> Este fluxo cobre os Casos de Uso [[02-Requisitos/Casos-de-Uso.md|UC-001 a UC-010]].

---

## Fluxo 2 â€” GravaÃ§Ã£o e TranscriÃ§Ã£o de Ãudio

```mermaid
flowchart TD
    A[Acompanhamento ativo] --> B{UsuÃ¡rio aciona gravaÃ§Ã£o?}
    B -->|Sim| C[Sistema pede confirmaÃ§Ã£o]
    C --> D{UsuÃ¡rio confirma?}
    D -->|Sim| E[Inicia gravaÃ§Ã£o]
    D -->|NÃ£o| F[NÃ£o grava]
    E --> G[Indicador visual ativo]
    G --> H{UsuÃ¡rio para gravaÃ§Ã£o?}
    H -->|Sim| I[Para gravaÃ§Ã£o]
    H -->|NÃ£o| G
    I --> J{UsuÃ¡rio solicita transcriÃ§Ã£o?}
    J -->|Sim| K[Envia Ã¡udio para Whisper]
    K --> L{TranscriÃ§Ã£o OK?}
    L -->|Sim| M[Processa com LLM]
    L -->|NÃ£o| N[Notifica erro]
    N --> O[Tenta novamente ou usa outro Ã¡udio]
    M --> P[Gera resumo estruturado]
    P --> Q[Exibe para revisÃ£o]
    Q --> R{UsuÃ¡rio aprova?}
    R -->|Sim| S[Resumo pronto para uso]
    R -->|Editar| T[UsuÃ¡rio edita]
    T --> S
    R -->|Regenerar| K
```

---

## Fluxo 3 â€” Registro de Conhecimento no Obsidian

```mermaid
flowchart TD
    A[ConteÃºdo gerado (resumo)] --> B{UsuÃ¡rio solicita registro?}
    B -->|Sim| C[Sistema analisa entidades]
    C --> D[Identifica: cliente, equipamentos, soluÃ§Ã£o, procedimento]
    D --> E{Cliente jÃ¡ existe?}
    E -->|Sim| F[Sugere atualizar nota existente]
    E -->|NÃ£o| G[Sugere criar nova nota de cliente]
    F --> H
    G --> H{Equipamento jÃ¡ existe?}
    H -->|Sim| I[Sugere atualizar nota do equipamento]
    H -->|NÃ£o| J[Sugere criar nota do equipamento]
    I --> K
    J --> K{SoluÃ§Ã£o jÃ¡ registrada?}
    K -->|Sim| L[Sugere vincular Ã  soluÃ§Ã£o existente]
    K -->|NÃ£o| M[Sugere criar nova nota de soluÃ§Ã£o]
    L --> N
    M --> N[Sugere nota de atendimento com links]
    N --> O[Exibe prÃ©via das alteraÃ§Ãµes]
    O --> P{UsuÃ¡rio aprova?}
    P -->|Sim| Q[Cria/atualiza notas no Obsidian]
    Q --> R[Estabelece links entre notas]
    P -->|Editar| S[UsuÃ¡rio personaliza]
    S --> Q
    P -->|Rejeitar| T[Descarta alteraÃ§Ãµes]
```

---

## Fluxo 4 â€” Fechamento de OS

```mermaid
flowchart TD
    A[Atendimento finalizado] --> B{UsuÃ¡rio solicita sugestÃ£o de fechamento?}
    B -->|Sim| C[Sistema consulta dados do chamado no Movidesk]
    C --> D[Monta prÃ©via do fechamento]
    D --> E[TÃ©cnico parceiro em campo?]
    E -->|Sim| F[Sugere status: Retorno da OS]
    E -->|NÃ£o| G[Sugere status: Resolvido]
    F --> H[Inclui: aguardando documento assinado]
    H --> I[Sugere e-mail para tÃ©cnico parceiro]
    G --> J[Inclui: resumo tÃ©cnico, configs, equipamentos]
    I --> K
    J --> K[Exibe prÃ©via para revisÃ£o]
    K --> L{UsuÃ¡rio aprova?}
    L -->|Sim| M{Status Ã© Retorno da OS?}
    M -->|Sim| N[Atualiza Movidesk com Retorno da OS + gera doc]
    M -->|NÃ£o| O[Atualiza Movidesk com Resolvido]
    N --> P[Aguardando documento assinado]
    P --> Q{Documento recebido?}
    Q -->|Sim| R[Atualiza para Resolvido]
    Q -->|NÃ£o| P
    L -->|Editar| S[UsuÃ¡rio ajusta]
    S --> K
    L -->|Rejeitar| T[Cancela fechamento]
```

---

## Fluxo 5 â€” GeraÃ§Ã£o de E-mail

```mermaid
flowchart TD
    A{UsuÃ¡rio solicita e-mail?} -->|Compra| B[Sistema pergunta materiais necessÃ¡rios]
    A -->|Comunicado| C[Sistema pergunta tipo: interno/externo]
    B --> D[UsuÃ¡rio informa materiais]
    D --> E[Sistema gera minuta]
    C --> F{Interno ou externo?}
    F -->|Interno| G[Sistema gera minuta tom informal]
    F -->|Externo| H[Sistema gera minuta tom formal]
    E --> I
    G --> I
    H --> I[Exibe minuta para revisÃ£o]
    I --> J{UsuÃ¡rio aprova?}
    J -->|Sim| K[Envia e-mail]
    J -->|Editar| L[UsuÃ¡rio edita]
    L --> I
    J -->|Rejeitar| M[Descarta e-mail]
    J -->|Rascunho| N[Salva como rascunho]
    K --> O[Registra no histÃ³rico]
    N --> O
```

---

## Fluxo 6 â€” Consulta de HistÃ³rico e SugestÃ£o de SoluÃ§Ã£o

```mermaid
flowchart TD
    A[UsuÃ¡rio pergunta ou pede sugestÃ£o] --> B[Sistema extrai contexto do atendimento]
    B --> C[Cliente, equipamento, sintomas]
    C --> D[Busca no banco vetorial]
    D --> E[Busca no Obsidian]
    E --> F{Encontrou casos similares?}
    F -->|Sim| G[Lista resultados por relevÃ¢ncia]
    G --> H[UsuÃ¡rio seleciona um caso]
    H --> I[Exibe detalhes: soluÃ§Ã£o, nota, histÃ³rico]
    F -->|NÃ£o| J[Informa: nenhum caso similar]
    J --> K[Sugere registrar como novo conhecimento]
    K --> L{UsuÃ¡rio quer registrar?}
    L -->|Sim| M[Fluxo de registro no Obsidian]
    L -->|NÃ£o| N[Encerra consulta]
```

---

## Fluxo 7 â€” Painel de AprovaÃ§Ãµes

```mermaid
flowchart TD
    A[HÃ¡ aÃ§Ãµes pendentes] --> B[Sistema notifica usuÃ¡rio]
    B --> C[UsuÃ¡rio acessa painel]
    C --> D[Lista aÃ§Ãµes pendentes]
    D --> E[Para cada aÃ§Ã£o:]
    E --> F{UsuÃ¡rio decide}
    F -->|Aprovar| G[Sistema executa aÃ§Ã£o]
    F -->|Editar| H[Abre editor para ajustes]
    H --> G
    F -->|Rejeitar| I[Sistema descarta aÃ§Ã£o]
    F -->|Sonegar| J[MantÃ©m pendente]
    G --> K[Registra em log]
    I --> K
    J --> D
    K --> L{Ainda hÃ¡ pendÃªncias?}
    L -->|Sim| D
    L -->|NÃ£o| M[Painel vazio]
```

---

**Premissas:**
- Todos os fluxos assumem que o Supervisor estÃ¡ logado e com acompanhamento ativo (quando aplicÃ¡vel).
- Fluxos alternativos podem ser adicionados conforme novos Casos de Uso forem identificados.

**Riscos:**
- Fluxos complexos podem ter variaÃ§Ãµes nÃ£o mapeadas â€” revisar com uso real.
- DependÃªncia de serviÃ§os externos (Movidesk, e-mail, LLM) pode introduzir latÃªncia nÃ£o prevista nos fluxos.

**DÃºvidas em aberto:**
- Deve haver um fluxo especÃ­fico para "Pausar e Retomar Acompanhamento"?
- Fluxo de "backup automÃ¡tico do vault Obsidian" deve ser mapeado?

**PrÃ³ximos passos:**
- Identificar e documentar [[03-Comportamento/Riscos.md|Riscos]].
- Iniciar [[04-Arquitetura/Arquitetura.md|Arquitetura]] e [[04-Arquitetura/Componentes.md|Componentes]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

