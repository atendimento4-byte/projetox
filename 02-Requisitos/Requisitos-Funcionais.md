---
title: "Requisitos Funcionais"
description: "38 requisitos funcionais organizados em 11 modulos"
status: "concluido"
---

# Requisitos Funcionais

> **Funcionalidades que o sistema deve implementar.**
> Organizados por mÃ³dulo. Cada RF possui identificador Ãºnico para rastreabilidade.

---

## ConvenÃ§Ãµes

| Prefixo | Significado |
|---------|-------------|
| **RF-ACOMP** | Acompanhamento de Atendimento |
| **RF-AUDIO** | GravaÃ§Ã£o e Ãudio |
| **RF-TRANS** | TranscriÃ§Ã£o |
| **RF-MEM** | MemÃ³ria e Conhecimento (Obsidian) |
| **RF-OS** | Ordem de ServiÃ§o |
| **RF-EMAIL** | E-mail e ComunicaÃ§Ãµes |
| **RF-IA** | InteligÃªncia Artificial e SugestÃµes |
| **RF-CONSULTA** | Consulta e HistÃ³rico |
| **RF-SEG** | SeguranÃ§a e Controle |
| **RF-INT** | IntegraÃ§Ãµes |
| **RF-UI** | Interface do UsuÃ¡rio |

---

## MÃ³dulo: Acompanhamento de Atendimento

### RF-ACOMP-001 â€” Iniciar Acompanhamento
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio inicie um novo acompanhamento de atendimento, associando-o a um chamado existente no Movidesk ou criando um registro avulso.
**Prioridade:** Alta
**Entrada:** NÃºmero do chamado ou identificador do cliente
**SaÃ­da:** SessÃ£o de acompanhamento ativa

### RF-ACOMP-002 â€” Finalizar Acompanhamento
**DescriÃ§Ã£o:** O sistema deve permitir finalizar o acompanhamento, encerrando a sessÃ£o e disponibilizando o resumo gerado para revisÃ£o.
**Prioridade:** Alta

### RF-ACOMP-003 â€” Associar TÃ©cnico Parceiro
**DescriÃ§Ã£o:** O sistema deve permitir associar um tÃ©cnico parceiro ao acompanhamento, registrando seu nome e contato.
**Prioridade:** MÃ©dia

### RF-ACOMP-004 â€” Registrar Tipo de Atendimento
**DescriÃ§Ã£o:** O sistema deve permitir classificar o atendimento por tipo (instalaÃ§Ã£o, manutenÃ§Ã£o, configuraÃ§Ã£o, suporte, etc.).
**Prioridade:** MÃ©dia

---

## MÃ³dulo: GravaÃ§Ã£o e Ãudio

### RF-AUDIO-001 â€” Iniciar GravaÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve iniciar a gravaÃ§Ã£o de Ã¡udio do atendimento **apenas mediante comando explÃ­cito do usuÃ¡rio**.
**Prioridade:** Alta
**Regra:** Jamais iniciar gravaÃ§Ã£o automaticamente. O usuÃ¡rio deve acionar via botÃ£o, hotkey ou comando de voz explÃ­cito.

### RF-AUDIO-002 â€” Parar GravaÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve parar a gravaÃ§Ã£o de Ã¡udio mediante comando do usuÃ¡rio.
**Prioridade:** Alta

### RF-AUDIO-003 â€” Indicador de GravaÃ§Ã£o Ativa
**DescriÃ§Ã£o:** O sistema deve exibir um indicador visual claro de que a gravaÃ§Ã£o estÃ¡ em andamento (ex.: LED, Ã­cone, aviso na interface).
**Prioridade:** Alta

### RF-AUDIO-004 â€” Armazenar GravaÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve armazenar o arquivo de Ã¡udio gravado em local seguro, associado ao acompanhamento correspondente.
**Prioridade:** Alta

### RF-AUDIO-005 â€” Apagar GravaÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio apague uma gravaÃ§Ã£o, com confirmaÃ§Ã£o explÃ­cita.
**Prioridade:** MÃ©dia

---

## MÃ³dulo: TranscriÃ§Ã£o

### RF-TRANS-001 â€” Transcrever Ãudio
**DescriÃ§Ã£o:** O sistema deve transcrever o Ã¡udio gravado para texto utilizando o Whisper (ou tecnologia equivalente).
**Prioridade:** Alta

### RF-TRANS-002 â€” Extrair Pontos-Chave
**DescriÃ§Ã£o:** O sistema deve extrair pontos-chave da transcriÃ§Ã£o, identificando problemas relatados, soluÃ§Ãµes aplicadas, decisÃµes tomadas e equipamentos envolvidos.
**Prioridade:** Alta

### RF-TRANS-003 â€” Gerar Resumo Estruturado
**DescriÃ§Ã£o:** O sistema deve gerar um resumo estruturado do atendimento contendo: problema, soluÃ§Ã£o, equipamentos envolvidos, configuraÃ§Ãµes realizadas, observaÃ§Ãµes.
**Prioridade:** Alta

### RF-TRANS-004 â€” Revisar e Editar TranscriÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio revise e edite a transcriÃ§Ã£o e o resumo antes de utilizÃ¡-los.
**Prioridade:** Alta

---

## MÃ³dulo: MemÃ³ria e Conhecimento (Obsidian)

### RF-MEM-001 â€” Registrar Conhecimento no Obsidian
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio solicite o registro de informaÃ§Ãµes no Obsidian de forma organizada, criando ou atualizando notas em pastas coerentes com o conteÃºdo.
**Prioridade:** Alta

### RF-MEM-002 â€” Estruturar Notas Automaticamente
**DescriÃ§Ã£o:** O sistema deve organizar as notas no Obsidian seguindo uma estrutura predefinida (clientes, equipamentos, procedimentos, soluÃ§Ãµes, atendimentos) e criar links entre notas relacionadas.
**Prioridade:** Alta

### RF-MEM-003 â€” Criar Links Entre Notas
**DescriÃ§Ã£o:** Ao registrar conhecimento, o sistema deve criar automaticamente links entre notas relacionadas (ex.: cliente â†’ equipamento â†’ atendimento â†’ soluÃ§Ã£o).
**Prioridade:** Alta

### RF-MEM-004 â€” Atualizar Notas Existentes
**DescriÃ§Ã£o:** O sistema deve atualizar notas existentes no Obsidian quando novas informaÃ§Ãµes relevantes forem identificadas (ex.: adicionar novo atendimento ao histÃ³rico do cliente).
**Prioridade:** Alta

### RF-MEM-005 â€” Manter Backups do Vault
**DescriÃ§Ã£o:** O sistema deve realizar backups periÃ³dicos do vault do Obsidian para evitar perda de dados.
**Prioridade:** MÃ©dia

> Nota: A estrutura do vault do Obsidian Ã© detalhada em [[05-Dados/Memoria-Obsidian.md]].

---

## MÃ³dulo: Ordem de ServiÃ§o

### RF-OS-001 â€” Sugerir Preenchimento de Fechamento
**DescriÃ§Ã£o:** Com base na transcriÃ§Ã£o e resumo, o sistema deve sugerir o preenchimento dos campos de fechamento da OS (resumo tÃ©cnico, configuraÃ§Ãµes, equipamentos trocados, hora/data).
**Prioridade:** Alta

### RF-OS-002 â€” Gerenciar MÃºltiplos Status de OS
**DescriÃ§Ã£o:** O sistema deve permitir a definiÃ§Ã£o do status adequado da OS: Aguardando LogÃ­stica, AprovaÃ§Ã£o de OrÃ§amento, Retorno do Cliente, PendÃªncia do Cliente, Resolvido, Retorno da OS.
**Prioridade:** Alta

### RF-OS-003 â€” Registrar Status "Retorno da OS"
**DescriÃ§Ã£o:** Quando o atendimento envolver tÃ©cnico parceiro em campo, o sistema deve sugerir o status "Retorno da OS" (nÃ£o "Resolvido"), indicando que aguarda documento assinado.
**Prioridade:** Alta

### RF-OS-004 â€” Registrar MÃ­dia na OS
**DescriÃ§Ã£o:** O sistema deve permitir anexar fotos e vÃ­deos ao registro da OS, associando-os ao resumo do atendimento.
**Prioridade:** MÃ©dia

### RF-OS-005 â€” Integrar Fechamento com Movidesk
**DescriÃ§Ã£o:** O sistema deve enviar o fechamento da OS para o Movidesk (resumo, status, mÃ­dia), **mediante aprovaÃ§Ã£o do usuÃ¡rio**.
**Prioridade:** Alta

---

## MÃ³dulo: E-mail e ComunicaÃ§Ãµes

### RF-EMAIL-001 â€” Sugerir E-mail de SolicitaÃ§Ã£o de Compra
**DescriÃ§Ã£o:** O sistema deve gerar uma minuta de e-mail de solicitaÃ§Ã£o de compra contendo: descritivo do material, justificativa, dados do cliente e motivo da solicitaÃ§Ã£o.
**Prioridade:** Alta

### RF-EMAIL-002 â€” Sugerir E-mail de Comunicado Interno/Externo
**DescriÃ§Ã£o:** O sistema deve gerar uma minuta de e-mail de comunicado (interno ou externo) com base no contexto do atendimento.
**Prioridade:** Alta

### RF-EMAIL-003 â€” Personalizar Templates de E-mail
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio revise, edite e personalize os e-mails sugeridos antes do envio.
**Prioridade:** Alta

### RF-EMAIL-004 â€” Enviar E-mail (com AprovaÃ§Ã£o)
**DescriÃ§Ã£o:** O sistema deve enviar o e-mail apenas apÃ³s aprovaÃ§Ã£o explÃ­cita do usuÃ¡rio.
**Prioridade:** Alta

---

## MÃ³dulo: InteligÃªncia Artificial e SugestÃµes

### RF-IA-001 â€” Sugerir SoluÃ§Ã£o com Base em HistÃ³rico
**DescriÃ§Ã£o:** Durante um atendimento, o sistema deve consultar o banco vetorial e o Obsidian para identificar casos semelhantes e sugerir soluÃ§Ãµes aplicadas anteriormente.
**Prioridade:** Alta

### RF-IA-002 â€” Sugerir Procedimentos
**DescriÃ§Ã£o:** O sistema deve sugerir procedimentos padronizados com base no tipo de atendimento e equipamento envolvido.
**Prioridade:** MÃ©dia

### RF-IA-003 â€” Responder Perguntas Durante Atendimento
**DescriÃ§Ã£o:** O sistema deve permitir que o usuÃ¡rio faÃ§a perguntas em linguagem natural durante o atendimento e receba respostas baseadas na base de conhecimento.
**Prioridade:** Alta

### RF-IA-004 â€” Contextualizar Respostas
**DescriÃ§Ã£o:** As respostas do sistema devem levar em conta o contexto do atendimento atual (cliente, equipamento, problema).
**Prioridade:** Alta

> Nota: Os agentes de IA que implementam estes requisitos sÃ£o detalhados em [[04-Arquitetura/Agentes.md]].

---

## MÃ³dulo: Consulta e HistÃ³rico

### RF-CONSULTA-001 â€” Consultar HistÃ³rico do Cliente
**DescriÃ§Ã£o:** O sistema deve permitir consultar o histÃ³rico completo de atendimentos de um cliente, incluindo soluÃ§Ãµes aplicadas e equipamentos envolvidos.
**Prioridade:** Alta

### RF-CONSULTA-002 â€” Pesquisar na Base de Conhecimento
**DescriÃ§Ã£o:** O sistema deve permitir pesquisa textual e semÃ¢ntica em toda a base de conhecimento do Obsidian.
**Prioridade:** Alta

### RF-CONSULTA-003 â€” Visualizar Relacionamentos
**DescriÃ§Ã£o:** O sistema deve exibir graficamente os relacionamentos entre entidades (cliente â†’ equipamento â†’ atendimento â†’ soluÃ§Ã£o).
**Prioridade:** Baixa

### RF-CONSULTA-004 â€” Recuperar Atendimento Anterior
**DescriÃ§Ã£o:** O sistema deve permitir recuperar o registro completo de um atendimento anterior pelo nÃºmero do chamado, data ou cliente.
**Prioridade:** MÃ©dia

---

## MÃ³dulo: SeguranÃ§a e Controle

### RF-SEG-001 â€” AprovaÃ§Ã£o ExplÃ­cita para AÃ§Ãµes CrÃ­ticas
**DescriÃ§Ã£o:** Nenhuma aÃ§Ã£o externa (envio de e-mail, fechamento de OS, alteraÃ§Ã£o no Movidesk, registro em lote no Obsidian) deve ocorrer sem aprovaÃ§Ã£o explÃ­cita do usuÃ¡rio.
**Prioridade:** CrÃ­tica

### RF-SEG-002 â€” Confirmar Antes de Gravar Ãudio
**DescriÃ§Ã£o:** O sistema deve solicitar confirmaÃ§Ã£o antes de iniciar qualquer gravaÃ§Ã£o de Ã¡udio.
**Prioridade:** CrÃ­tica

### RF-SEG-003 â€” Log de Auditoria
**DescriÃ§Ã£o:** O sistema deve registrar em log todas as aÃ§Ãµes executadas, incluindo decisÃµes do usuÃ¡rio (aprovou, recusou, editou).
**Prioridade:** Alta

### RF-SEG-004 â€” Notificar AÃ§Ãµes Pendentes
**DescriÃ§Ã£o:** O sistema deve notificar o usuÃ¡rio quando houver aÃ§Ãµes pendentes de aprovaÃ§Ã£o (ex.: e-mail aguardando revisÃ£o).
**Prioridade:** MÃ©dia

---

## MÃ³dulo: IntegraÃ§Ãµes

### RF-INT-001 â€” Integrar com Movidesk
**DescriÃ§Ã£o:** O sistema deve integrar com a API do Movidesk para consultar chamados, atualizar status, registrar resumos e anexar mÃ­dia.
**Prioridade:** Alta

### RF-INT-002 â€” Integrar com ServiÃ§o de E-mail
**DescriÃ§Ã£o:** O sistema deve integrar com o serviÃ§o de e-mail do usuÃ¡rio (Gmail, Outlook, etc.) para envio de e-mails sugeridos.
**Prioridade:** Alta

### RF-INT-003 â€” Integrar com Obsidian
**DescriÃ§Ã£o:** O sistema deve integrar com o Obsidian (via plugin ou API local) para criar, atualizar e consultar notas.
**Prioridade:** Alta

### RF-INT-004 â€” Integrar com n8n
**DescriÃ§Ã£o:** O sistema deve integrar com n8n para fluxos de automaÃ§Ã£o que envolvam mÃºltiplos serviÃ§os.
**Prioridade:** MÃ©dia

### RF-INT-005 â€” Integrar com CalendÃ¡rio
**DescriÃ§Ã£o:** O sistema deve integrar com calendÃ¡rio (Google Calendar, Outlook) para agendamento de retornos e prazos.
**Prioridade:** Baixa

---

## MÃ³dulo: Interface do UsuÃ¡rio

### RF-UI-001 â€” Interface de Acompanhamento
**DescriÃ§Ã£o:** O sistema deve fornecer uma interface (CLI, web ou desktop) que exiba o acompanhamento em tempo real, com status do atendimento, gravaÃ§Ã£o ativa e sugestÃµes.
**Prioridade:** Alta

### RF-UI-002 â€” Comandos RÃ¡pidos
**DescriÃ§Ã£o:** O sistema deve permitir comandos rÃ¡pidos do usuÃ¡rio (hotkeys ou comandos de texto) para aÃ§Ãµes frequentes: iniciar/parar gravaÃ§Ã£o, pedir resumo, registrar no Obsidian.
**Prioridade:** Alta

### RF-UI-003 â€” Painel de AprovaÃ§Ãµes
**DescriÃ§Ã£o:** O sistema deve apresentar um painel centralizado com todas as aÃ§Ãµes pendentes de aprovaÃ§Ã£o do usuÃ¡rio.
**Prioridade:** Alta

### RF-UI-004 â€” Indicadores de Status
**DescriÃ§Ã£o:** O sistema deve exibir indicadores visuais do estado atual: gravando, processando, aguardando aprovaÃ§Ã£o, aÃ§Ã£o executada.
**Prioridade:** MÃ©dia

---

## Matriz de Prioridades

| Prioridade | Quantidade |
|------------|------------|
| CrÃ­tica | 2 |
| Alta | 25 |
| MÃ©dia | 9 |
| Baixa | 2 |

---

**Premissas:**
- Os RFs podem ser refinados, divididos ou agrupados durante a fase de arquitetura.
- A priorizaÃ§Ã£o final serÃ¡ ajustada com base no MVP.

**Riscos:**
- Escopo pode aumentar se novos RFs surgirem durante o desenvolvimento.
- DependÃªncia de APIs externas (Movidesk) pode impactar RFs de integraÃ§Ã£o.

**DÃºvidas em aberto:**
- A interface serÃ¡ CLI (terminal), web ou desktop? Isso impacta RF-UI.
- O sistema precisa funcionar offline parcialmente?

**PrÃ³ximos passos:**
- Definir [[02-Requisitos/Requisitos-Nao-Funcionais.md|Requisitos NÃ£o Funcionais]].
- Detalhar [[02-Requisitos/Casos-de-Uso.md|Casos de Uso]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

