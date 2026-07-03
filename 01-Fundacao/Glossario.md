---
title: "Glossario"
description: "Definicoes dos principais termos, siglas e conceitos do dominio"
status: "concluido"
---

# GlossÃ¡rio

> **DefiniÃ§Ã£o dos termos tÃ©cnicos e de domÃ­nio utilizados no projeto.**
> Mantenha este documento atualizado conforme novos termos surgirem.

---

## Termos do DomÃ­nio

| Termo | DefiniÃ§Ã£o |
|-------|-----------|
| **Cliente** | Pessoa fÃ­sica ou jurÃ­dica que solicita ou recebe o atendimento tÃ©cnico. Pode ser um usuÃ¡rio domÃ©stico (PF) ou uma empresa contratante (PJ). |
| **TÃ©cnico Parceiro** | Profissional terceirizado ou parceiro que realiza o atendimento presencial em campo. Executa o serviÃ§o no local do cliente. |
| **Supervisor** | VocÃª â€” responsÃ¡vel pelo acompanhamento remoto, supervisÃ£o dos tÃ©cnicos parceiros, configuraÃ§Ãµes de equipamentos e fechamento administrativo dos atendimentos. |
| **Chamado / OS** | Registro de solicitaÃ§Ã£o de atendimento. Representa a sessÃ£o completa de atendimento. OS (Ordem de ServiÃ§o) Ã© o documento formal que registra a execuÃ§Ã£o. SÃ£o termos equivalentes. |

## Status de OS

| Termo | DefiniÃ§Ã£o |
|-------|-----------|
| **OS â€” Resolvido** | Status final do atendimento. Utilizado quando o serviÃ§o foi concluÃ­do sem envolvimento de tÃ©cnico parceiro em campo. |
| **OS â€” Retorno da OS** | Status intermediÃ¡rio. Utilizado quando hÃ¡ tÃ©cnico parceiro em campo â€” o atendimento aguarda o documento de OS assinado pelo tÃ©cnico parceiro para ser finalizado. |
| **OS â€” Aguardando LogÃ­stica** | Status que indica pendÃªncia de material ou logÃ­stica para conclusÃ£o do serviÃ§o. |
| **OS â€” AprovaÃ§Ã£o de OrÃ§amento** | Status que indica aguardo de aprovaÃ§Ã£o de orÃ§amento pelo cliente. |
| **OS â€” Retorno do Cliente** | Status que indica aguardo de retorno ou posicionamento do cliente. |
| **OS â€” PendÃªncia do Cliente** | Status que indica pendÃªncia atribuÃ­da ao cliente (ex.: nÃ£o forneceu acesso, nÃ£o disponibilizou equipamento). |

## Componentes do Sistema

| Termo | DefiniÃ§Ã£o |
|-------|-----------|
| **Hermes** | Orquestrador principal do sistema â€” gerencia o fluxo de eventos, aciona agentes, controla permissÃµes e coordena as interaÃ§Ãµes entre mÃ³dulos. |
| **Obsidian** | Ferramenta de conhecimento utilizada como memÃ³ria persistente do sistema. Armazena conhecimento organizado em notas interligadas sobre clientes, equipamentos, procedimentos e soluÃ§Ãµes. |
| **Whisper** | Modelo de transcriÃ§Ã£o de Ã¡udio para texto (OpenAI Whisper). Utilizado para transcrever gravaÃ§Ãµes de atendimentos. |
| **LLM** | Modelo de Linguagem de Grande Escala (Large Language Model) â€” Claude, GPT ou Gemini. ResponsÃ¡vel por gerar resumos, sugerir textos, analisar contextos e auxiliar nas respostas. |
| **Banco Vetorial** | Banco de dados especializado em armazenar e consultar embeddings vetoriais (Qdrant ou Chroma). Utilizado para busca semÃ¢ntica no histÃ³rico e na memÃ³ria. |
| **n8n** | Plataforma de automaÃ§Ã£o de fluxos de trabalho (workflow automation). Utilizada para orquestrar integraÃ§Ãµes entre serviÃ§os (e-mail, Movidesk, etc.). |
| **MCP** | Model Context Protocol â€” protocolo para integraÃ§Ã£o de ferramentas e contexto com LLMs. |
| **Embedding** | RepresentaÃ§Ã£o vetorial de texto que captura significado semÃ¢ntico. Utilizado para busca por similaridade no banco vetorial. |

## AÃ§Ãµes e Processos

| Termo | DefiniÃ§Ã£o |
|-------|-----------|
| **Acompanhamento Remoto** | AÃ§Ã£o de conectar-se remotamente ao equipamento do cliente para diagnosticar, configurar ou resolver problemas, com supervisÃ£o direta sua. |
| **Fechamento de OS** | Processo de finalizaÃ§Ã£o do atendimento que inclui: registrar resumo tÃ©cnico, anexar fotos/vÃ­deos, documentar configuraÃ§Ãµes realizadas, listar equipamentos trocados, registrar hora/data e definir status adequado. |
| **E-mail de SolicitaÃ§Ã£o de Compra** | Comunicado gerado para solicitar aquisiÃ§Ã£o de material necessÃ¡rio para conclusÃ£o do atendimento. ContÃ©m descritivo do material, justificativa e dados do cliente. |
| **E-mail de Comunicado Interno/Externo** | Comunicado gerado para informar partes interessadas sobre o andamento ou conclusÃ£o do atendimento. Pode ser interno (equipe) ou externo (cliente). |
| **TranscriÃ§Ã£o de Pontos-Chave** | ExtraÃ§Ã£o seletiva de partes relevantes do Ã¡udio do atendimento, convertendo-as em texto resumido â€” nÃ£o Ã© a transcriÃ§Ã£o literal completa, mas um resumo dos pontos importantes. |
| **Registro de Conhecimento** | AÃ§Ã£o de salvar no Obsidian, de forma organizada e estruturada, informaÃ§Ãµes relevantes aprendidas durante o atendimento para consulta futura. |

## Conceitos de Dados e MemÃ³ria

| Termo | DefiniÃ§Ã£o |
|-------|-----------|
| **MemÃ³ria Persistente** | Base de conhecimento de longo prazo armazenada no Obsidian. Inclui dados de clientes, procedimentos, soluÃ§Ãµes, configuraÃ§Ãµes e relacionamentos entre informaÃ§Ãµes. |
| **HistÃ³rico do Cliente** | Conjunto de todos os atendimentos anteriores, soluÃ§Ãµes aplicadas, equipamentos envolvidos e observaÃ§Ãµes registradas para um determinado cliente. |
| **Relacionamento entre InformaÃ§Ãµes** | Links e conexÃµes estabelecidas no Obsidian entre notas diferentes (ex.: um equipamento ligado a um cliente, uma soluÃ§Ã£o ligada a um procedimento). |

---

**Premissas:**
- OS termos podem ser refinados durante as prÃ³ximas fases do projeto.
- Novos termos serÃ£o adicionados conforme novos mÃ³dulos forem definidos.

**Riscos:**
- Termos ambÃ­guos podem causar inconsistÃªncia entre documentos. Revisar periodicamente.

**DecisÃµes:**
- "Chamado" e "OS" sÃ£o sinÃ´nimos. "Chamado" Ã© o termo principal; "OS" refere-se ao documento formal.
- "Supervisor" Ã© a persona principal (anteriormente "UsuÃ¡rio do Sistema").

**PrÃ³ximos passos:**
- Validar este glossÃ¡rio antes de prosseguir.
- Revisar e complementar conforme novos documentos forem criados.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

