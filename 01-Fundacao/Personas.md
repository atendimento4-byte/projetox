---
title: "Personas"
description: "Perfis de usuario: Supervisor, Tecnico e Cliente"
status: "concluido"
---

# Personas

> **Perfis dos usuÃ¡rios do sistema.**
> Apesar de o sistema ser inicialmente de uso individual, identificamos trÃªs personas que interagem direta ou indiretamente com o ecossistema.

---

## Persona 1 â€” Supervisor TÃ©cnico (VocÃª)

| Campo | DescriÃ§Ã£o |
|-------|-----------|
| **Nome** | Supervisor TÃ©cnico |
| **Papel** | UsuÃ¡rio primÃ¡rio do sistema. ResponsÃ¡vel pelo acompanhamento remoto, supervisÃ£o de tÃ©cnicos parceiros, configuraÃ§Ã£o de equipamentos e fechamento administrativo. |
| **Ferramentas atuais** | Movidesk (helpdesk), E-mail (Outlook/Gmail), Telefone, Software de acesso remoto |
| **Dores** | Processos burocrÃ¡ticos pÃ³s-atendimento consomem tempo (fechamento de OS, e-mails, documentaÃ§Ã£o). Conhecimento fica disperso â€” difÃ­cil recuperar soluÃ§Ãµes passadas. |
| **Necessidades** | Agilizar burocracias. Ter uma memÃ³ria organizada. Receber sugestÃµes inteligentes. Manter controle total sobre as aÃ§Ãµes. |
| **Como usa o sistema** | Acompanha atendimento remoto â†’ ativa gravaÃ§Ã£o â†’ pede transcriÃ§Ã£o/resumo â†’ pede registro no Obsidian â†’ pede sugestÃ£o de e-mail ou fechamento de OS â†’ aprova ou ajusta â†’ sistema executa. |
| **FrequÃªncia de uso** | DiÃ¡ria. 5 a 7 atendimentos por dia. |
| **NÃ­vel tÃ©cnico** | Alto â€” conhece bem as ferramentas e processos tÃ©cnicos. |
| **Objetivo com o sistema** | Reduzir tempo burocrÃ¡tico em 50%+ e construir uma base de conhecimento reutilizÃ¡vel. |

### CenÃ¡rio tÃ­pico

> JoÃ£o (Supervisor TÃ©cnico) estÃ¡ acompanhando remotamente a instalaÃ§Ã£o de um equipamento de rede. O tÃ©cnico parceiro estÃ¡ no local. Durante o atendimento, JoÃ£o ativa a gravaÃ§Ã£o de Ã¡udio para capturar as configuraÃ§Ãµes que estÃ£o sendo realizadas. Ao final, ele solicita ao assistente que transcreva os pontos-chave e sugira o resumo para fechamento da OS. O assistente tambÃ©m consulta o histÃ³rico e sugere um modelo de e-mail de comunicado interno. JoÃ£o revisa, aprova e o sistema executa as aÃ§Ãµes.

---

## Persona 2 â€” TÃ©cnico Parceiro

| Campo | DescriÃ§Ã£o |
|-------|-----------|
| **Nome** | TÃ©cnico Parceiro |
| **Papel** | Profissional terceirizado que executa o serviÃ§o presencialmente no local do cliente. |
| **Ferramentas atuais** | Telefone, Documento fÃ­sico de OS, Eventualmente ferramentas prÃ³prias |
| **Dores** | Precisa reportar o que foi feito ao Supervisor. Depende de papelada fÃ­sica (OS assinada). ComunicaÃ§Ã£o pode ser ineficiente. |
| **Necessidades** | Registrar rapidamente o que foi executado. Enviar evidÃªncias (fotos). Obter retorno do supervisor. |
| **InteraÃ§Ã£o com o sistema** | Indireta â€” o sistema coleta dados do atendimento (via supervisÃ£o remota) e gera documentaÃ§Ã£o. O tÃ©cnico parceiro interage com o sistema apenas atravÃ©s do Supervisor. |
| **FrequÃªncia de uso** | DiÃ¡ria ou conforme demanda de atendimentos. |
| **NÃ­vel tÃ©cnico** | MÃ©dio â€” conhece a execuÃ§Ã£o prÃ¡tica dos serviÃ§os. |
| **Objetivo com o sistema** | Facilitar o reporte pÃ³s-serviÃ§o e reduzir retrabalho de documentaÃ§Ã£o. |

### CenÃ¡rio tÃ­pico

> Carlos (TÃ©cnico Parceiro) estÃ¡ no cliente trocando um equipamento. Durante o serviÃ§o, ele tira fotos do antes/depois e informa ao Supervisor por telefone as configuraÃ§Ãµes realizadas. O sistema captura essas informaÃ§Ãµes via transcriÃ§Ã£o do Ã¡udio da chamada. Ao final, o Supervisor gera o resumo e Carlos recebe o documento de OS para assinar digitalmente.

---

## Persona 3 â€” Cliente

| Campo | DescriÃ§Ã£o |
|-------|-----------|
| **Nome** | Cliente |
| **Papel** | Pessoa fÃ­sica ou jurÃ­dica que solicita e recebe o atendimento tÃ©cnico. |
| **Ferramentas atuais** | Telefone, E-mail |
| **Dores** | NÃ£o tem visibilidade do andamento do serviÃ§o. Pode precisar aprovar orÃ§amentos. Recebe comunicados por e-mail. |
| **Necessidades** | Ser informado sobre o status do atendimento. Receber documentaÃ§Ã£o do serviÃ§o realizado. Aprovar orÃ§amentos quando necessÃ¡rio. |
| **InteraÃ§Ã£o com o sistema** | Indireta â€” recebe e-mails gerados pelo sistema (comunicados, solicitaÃ§Ãµes de compra, OS fechada). |
| **FrequÃªncia de uso** | Eventual (quando solicita um atendimento). |
| **NÃ­vel tÃ©cnico** | VariÃ¡vel â€” de leigo a tÃ©cnico. |
| **Objetivo com o sistema** | Receber um serviÃ§o bem documentado e ser informado adequadamente. |

### CenÃ¡rio tÃ­pico

> Maria (Cliente) solicitou a instalaÃ§Ã£o de um novo servidor. O tÃ©cnico parceiro foi ao local, o Supervisor acompanhou remotamente. Ao final, Maria recebe um e-mail automÃ¡tico com o resumo do serviÃ§o executado, configuraÃ§Ãµes realizadas e a OS para seus registros. Se houve necessidade de compra de material, ela recebe o e-mail de solicitaÃ§Ã£o de compra para aprovaÃ§Ã£o.

---

## Personas vs Funcionalidades

| Funcionalidade | Supervisor | TÃ©cnico Parceiro | Cliente |
|----------------|:----------:|:-----------------:|:-------:|
| Acompanhar atendimento remoto | âœ… Direto | âŒ | âŒ |
| Gravar Ã¡udio | âœ… Ativa | âŒ | âŒ |
| Transcrever/resumir | âœ… Solicita | âŒ | âŒ |
| Registrar no Obsidian | âœ… Solicita | âŒ | âŒ |
| Consultar histÃ³rico | âœ… Direto | âŒ | âŒ |
| Sugerir e-mail compra | âœ… Revisa e aprova | âŒ | ðŸ“¨ Recebe |
| Sugerir e-mail comunicado | âœ… Revisa e aprova | âŒ | ðŸ“¨ Recebe |
| Sugerir fechamento de OS | âœ… Revisa e aprova | âŒ | ðŸ“¨ Recebe cÃ³pia |
| Solicitar compra de material | âœ… Gera | ðŸ“ž Informa | âœ… Aprova |
| Documento de OS assinado | âœ… Recebe | âœ… Assina | âœ… Recebe |

> Ver [[01-Fundacao/Glossario.md|GlossÃ¡rio]] para definiÃ§Ãµes dos termos e [[02-Requisitos/Requisitos-Funcionais.md|Requisitos Funcionais]] para detalhes de cada funcionalidade.

---

**Premissas:**
- Inicialmente apenas o Supervisor utiliza o sistema diretamente.
- TÃ©cnico Parceiro e Cliente interagem indiretamente via e-mails e documentos gerados.

**Riscos:**
- Se o sistema for expandido para equipe, novas personas podem surgir (ex.: Gestor, Admin).
- TÃ©cnico Parceiro pode se beneficiar de acesso direto ao sistema no futuro.

**DÃºvidas em aberto:**
- O TÃ©cnico Parceiro deve ter acesso direto a alguma funcionalidade no futuro? (Ex.: app mobile para registrar fotos e assinar OS.)
- O Cliente deve ter um portal de acompanhamento?

**PrÃ³ximos passos:**
- Definir [[02-Requisitos/Requisitos-Funcionais.md|Requisitos Funcionais]] com base nas necessidades identificadas.
- Mapear [[02-Requisitos/Casos-de-Uso.md|Casos de Uso]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

