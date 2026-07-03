---
title: "Visao Geral"
description: "Proposito, contexto, funcionalidades e tecnologias do sistema"
status: "concluido"
---

# VisÃ£o Geral

> **DescriÃ§Ã£o de alto nÃ­vel do sistema, propÃ³sito, contexto e justificativa.**

---

## Nome do Projeto

**Hermes + Obsidian** â€” Assistente Inteligente para Atendimentos TÃ©cnicos

## PropÃ³sito

Construir um assistente pessoal inteligente que acompanhe atendimentos tÃ©cnicos remotos, registre conhecimento de forma estruturada, crie memÃ³ria persistente e automatize tarefas administrativas â€” mantendo sempre o usuÃ¡rio no controle de todas as aÃ§Ãµes executadas.

## Contexto Atual

O fluxo de trabalho hoje funciona da seguinte forma:

1. O cliente entra em contato com o setor de atendimento.
2. O setor de atendimento abre um chamado no **Movidesk** e contacta o tÃ©cnico parceiro.
3. O tÃ©cnico parceiro desloca-se atÃ© o local do cliente.
4. VocÃª Ã© acionado para realizar o **acompanhamento remoto**.
5. VocÃªs executam o serviÃ§o conjuntamente (vocÃª remoto, tÃ©cnico presencial).
6. Ao final, inicia-se a fase burocrÃ¡tica:
   - Dependendo do caso, Ã© necessÃ¡rio enviar **e-mail de solicitaÃ§Ã£o de compra** ou **e-mail de comunicado**.
   - Ã‰ preciso **documentar** todo o atendimento no Movidesk (resumo, fotos, vÃ­deos, configuraÃ§Ãµes, equipamentos trocados).
   - A OS precisa ser **fechada** com o status correto (Resolvido ou Retorno da OS, aguardando documento assinado).

**Principal dor:** A fase burocrÃ¡tica pÃ³s-atendimento consome tempo significativo e Ã© repetitiva, desviando o foco do trabalho tÃ©cnico.

## O Que o Sistema Deve Fazer

### Durante o Atendimento

- Gravar Ã¡udio **apenas quando autorizado** pelo usuÃ¡rio.
- Transcrever pontos-chave do atendimento em tempo real ou sob demanda.
- Identificar problemas, soluÃ§Ãµes e decisÃµes importantes.
- Consultar automaticamente o histÃ³rico do cliente e atendimentos anteriores para auxiliar na tomada de decisÃ£o.
- Sugerir soluÃ§Ãµes com base em casos semelhantes jÃ¡ registrados.

### ApÃ³s o Atendimento

- Sugerir o preenchimento do resumo de fechamento da OS com base na transcriÃ§Ã£o.
- Sugerir a abertura de e-mails (solicitaÃ§Ã£o de compra, comunicados) com texto prÃ©-preenchido.
- Registrar conhecimento no **Obsidian** de forma organizada e estruturada.
- Manter relacionamentos entre informaÃ§Ãµes (cliente â†’ equipamento â†’ soluÃ§Ã£o â†’ procedimento).

### Requisito Fundamental

**Nenhuma aÃ§Ã£o crÃ­tica ocorre automaticamente.** Toda sugestÃ£o deve passar por aprovaÃ§Ã£o explÃ­cita do usuÃ¡rio antes de ser executada. O assistente Ã© um facilitador, nÃ£o um substituto.

## Tecnologias Previstas

| Componente | Tecnologia | FunÃ§Ã£o |
|------------|------------|--------|
| Orquestrador | Hermes | Gerencia fluxos e coordena agentes |
| MemÃ³ria | Obsidian | Armazenamento persistente de conhecimento |
| TranscriÃ§Ã£o | Whisper | ConversÃ£o de Ã¡udio em texto |
| LLM | Claude / GPT / Gemini | GeraÃ§Ã£o de resumos, sugestÃµes e anÃ¡lises |
| Banco Vetorial | Qdrant / Chroma | Busca semÃ¢ntica no histÃ³rico |
| AutomaÃ§Ã£o | n8n | IntegraÃ§Ã£o entre serviÃ§os |
| Banco Relacional | PostgreSQL | Dados estruturados do sistema |
| Cache | Redis | Performance e sessÃµes |
| APIs Externas | Movidesk, E-mail | IntegraÃ§Ã£o com sistemas existentes |

> Nota: Consulte [[04-Arquitetura/ADRs.md|ADRs]] para a justificativa de cada tecnologia.

## PÃºblico-Alvo

- **Inicialmente:** Apenas vocÃª (uso pessoal).
- **Futuramente:** Possibilidade de expandir para equipe.

## CritÃ©rios de Sucesso

- ReduÃ§Ã£o do tempo gasto em tarefas burocrÃ¡ticas pÃ³s-atendimento.
- Facilidade para registrar e recuperar conhecimento tÃ©cnico.
- PrecisÃ£o nas sugestÃµes do assistente (resumos, e-mails, soluÃ§Ãµes).
- Confiabilidade â€” nenhuma aÃ§Ã£o nÃ£o autorizada deve ocorrer.

---

**Premissas:**
- O sistema serÃ¡ usado inicialmente apenas por vocÃª.
- O Movidesk possui API funcional para consulta e atualizaÃ§Ã£o de chamados.
- O Obsidian serÃ¡ o repositÃ³rio central de conhecimento.
- HaverÃ¡ conexÃ£o com internet para acesso aos LLMs e serviÃ§os externos.

**Riscos:**
- DependÃªncia de API do Movidesk â€” se sofrer alteraÃ§Ãµes, pode impactar integraÃ§Ãµes.
- Qualidade da transcriÃ§Ã£o do Whisper pode variar com ruÃ­do ambiente ou sotaques.
- Obsidian sem versionamento pode levar a perda acidental de dados.

**DÃºvidas em aberto:**
- O sistema serÃ¡ uma aplicaÃ§Ã£o desktop, web ou CLI? (A definir na Arquitetura.)
- Como serÃ¡ feita a ativaÃ§Ã£o da gravaÃ§Ã£o de Ã¡udio? (Hotkey, comando de voz, botÃ£o?)
- O processamento do Ã¡udio serÃ¡ local ou em nuvem?

**PrÃ³ximos passos:**
- Definir [[01-Fundacao/Objetivos.md|Objetivos]] formais do sistema.
- Detalhar [[01-Fundacao/Personas.md|Personas]].
- Mapear [[02-Requisitos/Requisitos-Funcionais.md|Requisitos Funcionais]] e [[02-Requisitos/Requisitos-Nao-Funcionais.md|NÃ£o Funcionais]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

