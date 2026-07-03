---
title: "Casos de Uso"
description: "10 casos de uso com fluxos principal e alternativos"
status: "concluido"
---

# Casos de Uso

> **DescriÃ§Ã£o detalhada das interaÃ§Ãµes entre atores e o sistema.**
> Cada caso de uso descreve um fluxo principal, fluxos alternativos e regras de negÃ³cio.

---

## Atores

| Ator | DescriÃ§Ã£o |
|------|-----------|
| **Supervisor** | UsuÃ¡rio primÃ¡rio do sistema. Acompanha atendimentos remotamente, ativa funÃ§Ãµes e aprova aÃ§Ãµes. |
| **Sistema** | O assistente inteligente (Hermes + mÃ³dulos). |
| **Movidesk** | Sistema externo de helpdesk. |
| **ServiÃ§o de E-mail** | Provedor de e-mail externo. |
| **Obsidian** | Sistema de notas utilizado como memÃ³ria persistente. |

> Ver [[01-Fundacao/Glossario.md|GlossÃ¡rio]] para definiÃ§Ãµes completas dos atores e termos.

---

## UC-001 â€” Iniciar Acompanhamento de Atendimento

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Supervisor estÃ¡ logado no sistema.
**PÃ³s-condiÃ§Ãµes:** SessÃ£o de acompanhamento ativa, associada a um chamado ou cliente.

**Fluxo principal:**
1. Supervisor solicita iniciar novo acompanhamento.
2. Sistema exibe opÃ§Ãµes: informar nÃºmero do chamado ou nome do cliente.
3. Supervisor informa o nÃºmero do chamado.
4. Sistema consulta o Movidesk e obtÃ©m dados do chamado (cliente, tipo, tÃ©cnico associado).
5. Sistema cria sessÃ£o de acompanhamento com status "Em Andamento".
6. Sistema exibe a tela de acompanhamento com dados do chamado.

**Fluxo alternativo A â€” Chamado nÃ£o encontrado:**
3a. Supervisor informa nÃºmero do chamado.
4a. Movidesk retorna erro (chamado inexistente).
5a. Sistema notifica Supervisor.
6a. Sistema permite criar acompanhamento avulso (sem vÃ­nculo com chamado).

**Fluxo alternativo B â€” Acompanhamento avulso:**
3b. Supervisor opta por criar acompanhamento avulso.
4b. Sistema solicita dados mÃ­nimos: nome do cliente, tipo de atendimento.
5b. Sistema cria sessÃ£o de acompanhamento sem vÃ­nculo com Movidesk.

**Regras de negÃ³cio:**
- Apenas um acompanhamento pode estar ativo por vez.
- O acompanhamento avulso pode ser vinculado a um chamado posteriormente.

---

## UC-002 â€” Gravar Ãudio do Atendimento

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Acompanhamento ativo.
**PÃ³s-condiÃ§Ãµes:** Ãudio sendo gravado OU Ã¡udio salvo no sistema.

**Fluxo principal â€” Iniciar gravaÃ§Ã£o:**
1. Supervisor aciona comando "Iniciar GravaÃ§Ã£o" (hotkey / botÃ£o / comando de voz).
2. Sistema exibe confirmaÃ§Ã£o: "Iniciar gravaÃ§Ã£o de Ã¡udio?"
3. Supervisor confirma.
4. Sistema inicia gravaÃ§Ã£o.
5. Sistema exibe indicador visual de gravaÃ§Ã£o ativa (Ã­cone/led vermelho).
6. Sistema registra em log: inÃ­cio da gravaÃ§Ã£o com timestamp.

**Fluxo principal â€” Parar gravaÃ§Ã£o:**
1. Supervisor aciona comando "Parar GravaÃ§Ã£o".
2. Sistema para a gravaÃ§Ã£o.
3. Sistema oculta indicador de gravaÃ§Ã£o ativa.
4. Sistema salva o arquivo de Ã¡udio associado ao acompanhamento.
5. Sistema registra em log: fim da gravaÃ§Ã£o com timestamp e tamanho do arquivo.

**Fluxo alternativo A â€” Recusa de confirmaÃ§Ã£o:**
3a. Supervisor nÃ£o confirma a gravaÃ§Ã£o.
4a. Sistema nÃ£o inicia gravaÃ§Ã£o. Nenhum dado Ã© registrado.

**Regras de negÃ³cio:**
- Jamais iniciar gravaÃ§Ã£o automaticamente.
- Indicador visual de gravaÃ§Ã£o Ã© obrigatÃ³rio enquanto grava.
- Supervisor pode pausar e retomar a gravaÃ§Ã£o.

---

## UC-003 â€” Transcrever e Resumir Atendimento

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Acompanhamento ativo E Ã¡udio gravado OU em andamento.
**PÃ³s-condiÃ§Ãµes:** TranscriÃ§Ã£o e resumo estruturado disponÃ­veis para revisÃ£o.

**Fluxo principal:**
1. Supervisor solicita "Transcrever Ãudio" ou "Gerar Resumo".
2. Sistema envia Ã¡udio para transcriÃ§Ã£o (Whisper).
3. Whisper retorna transcriÃ§Ã£o em texto.
4. Sistema processa transcriÃ§Ã£o com LLM para extrair pontos-chave.
5. Sistema gera resumo estruturado contendo:
   - Problema relatado
   - SoluÃ§Ã£o aplicada
   - Equipamentos envolvidos
   - ConfiguraÃ§Ãµes realizadas
   - ObservaÃ§Ãµes
6. Sistema exibe transcriÃ§Ã£o e resumo para revisÃ£o do Supervisor.
7. Supervisor pode editar, aprovar ou solicitar nova geraÃ§Ã£o.

**Fluxo alternativo A â€” TranscriÃ§Ã£o em andamento (Ã¡udio ainda gravando):**
1a. Supervisor solicita transcriÃ§Ã£o parcial.
2a-7a. Sistema transcreve apenas o trecho jÃ¡ gravado atÃ© o momento.

**Fluxo alternativo B â€” Falha na transcriÃ§Ã£o:**
3a. Whisper retorna erro (Ã¡udio corrompido, ruÃ­do excessivo).
4a. Sistema notifica Supervisor sobre a falha.
5a. Sistema solicita nova gravaÃ§Ã£o ou uso de Ã¡udio alternativo.

**Regras de negÃ³cio:**
- TranscriÃ§Ãµes e resumos sÃ£o sempre revisados pelo Supervisor antes do uso.
- O Ã¡udio original Ã© preservado mesmo apÃ³s transcriÃ§Ã£o (atÃ© polÃ­tica de retenÃ§Ã£o).

---

## UC-004 â€” Registrar Conhecimento no Obsidian

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Resumo do atendimento gerado OU informaÃ§Ãµes relevantes identificadas.
**PÃ³s-condiÃ§Ãµes:** Conhecimento registrado no Obsidian com estrutura e links adequados.

**Fluxo principal:**
1. Supervisor solicita "Registrar no Obsidian".
2. Sistema analisa o conteÃºdo do atendimento e identifica entidades:
   - Cliente (jÃ¡ existe no Obsidian? Novo?)
   - Equipamentos envolvidos
   - SoluÃ§Ã£o aplicada
   - Procedimento utilizado
3. Sistema sugere estrutura de notas a serem criadas/atualizadas:
   - Nota do cliente (atualizar histÃ³rico)
   - Nota do equipamento (criar ou atualizar)
   - Nota de procedimento (se novo)
   - Nota de atendimento (link para todas as anteriores)
4. Sistema exibe prÃ©via das alteraÃ§Ãµes propostas.
5. Supervisor revisa e aprova.
6. Sistema cria/atualiza as notas no Obsidian.
7. Sistema estabelece links entre as notas (cliente â†’ equipamento â†’ atendimento â†’ soluÃ§Ã£o).

**Fluxo alternativo A â€” Supervisor personaliza:**
1a-5a. Supervisor edita manualmente as notas propostas antes de aprovar.
6a. Sistema aplica as alteraÃ§Ãµes personalizadas.

**Fluxo alternativo B â€” Cliente/equipamento jÃ¡ existe:**
2a. Sistema detecta que cliente jÃ¡ possui nota no Obsidian.
3a. Sistema sugere apenas atualizaÃ§Ã£o da nota existente (adicionar novo atendimento ao histÃ³rico).

**Regras de negÃ³cio:**
- Todas as alteraÃ§Ãµes no Obsidian passam por aprovaÃ§Ã£o do Supervisor.
- O sistema mantÃ©m consistÃªncia nos links entre notas.
- O vault do Obsidian tem estrutura de pastas predefinida.

---

## UC-005 â€” Sugerir Fechamento de OS

**Ator principal:** Supervisor
**Atores secundÃ¡rios:** Movidesk
**PrÃ©-condiÃ§Ãµes:** Atendimento finalizado, resumo gerado.
**PÃ³s-condiÃ§Ãµes:** OS atualizada no Movidesk com status e resumo corretos.

**Fluxo principal â€” Sem tÃ©cnico parceiro:**
1. Supervisor solicita "Sugerir Fechamento de OS".
2. Sistema consulta dados do chamado no Movidesk.
3. Sistema preenche campos sugeridos com base no resumo:
   - Resumo tÃ©cnico
   - ConfiguraÃ§Ãµes realizadas
   - Equipamentos trocados
   - Hora/data
4. Sistema sugere status "Resolvido".
5. Sistema exibe prÃ©via do fechamento.
6. Supervisor revisa, ajusta se necessÃ¡rio, e aprova.
7. Sistema envia atualizaÃ§Ã£o para o Movidesk.
8. Sistema registra em log: OS fechada com sucesso.

**Fluxo principal â€” Com tÃ©cnico parceiro em campo:**
1-3. Idem fluxo principal.
4. Sistema sugere status "Retorno da OS".
5. Sistema adiciona campo: "Aguardando documento assinado do tÃ©cnico parceiro".
6. Sistema sugere e-mail para envio do documento de OS ao tÃ©cnico parceiro.
7. Supervisor aprova.
8. Sistema atualiza Movidesk com status "Retorno da OS".
9. Sistema gera documento de OS para assinatura do tÃ©cnico parceiro.
10. Sistema registra em log: OS atualizada para Retorno da OS.

**Fluxo alternativo A â€” OS requer aprovaÃ§Ã£o de orÃ§amento:**
2a. Sistema identifica que OS requer aprovaÃ§Ã£o de orÃ§amento.
4a. Sistema sugere status "AprovaÃ§Ã£o de OrÃ§amento".
5a. Sistema gera e-mail de solicitaÃ§Ã£o de aprovaÃ§Ã£o para o cliente.
6a-8a. Supervisor revisa e aprova.

**Regras de negÃ³cio:**
- O Supervisor revisa e aprova todo fechamento de OS antes de enviar ao Movidesk.
- O status "Retorno da OS" sÃ³ Ã© aplicado quando hÃ¡ tÃ©cnico parceiro em campo.
- Fotos e vÃ­deos podem ser anexados ao fechamento.

---

## UC-006 â€” Gerar E-mail de SolicitaÃ§Ã£o de Compra

**Ator principal:** Supervisor
**Atores secundÃ¡rios:** ServiÃ§o de E-mail
**PrÃ©-condiÃ§Ãµes:** Atendimento em andamento ou finalizado, identificada necessidade de compra de material.
**PÃ³s-condiÃ§Ãµes:** E-mail de solicitaÃ§Ã£o de compra enviado (apÃ³s aprovaÃ§Ã£o).

**Fluxo principal:**
1. Supervisor solicita "Gerar E-mail de SolicitaÃ§Ã£o de Compra".
2. Sistema consulta resumo do atendimento para extrair contexto.
3. Sistema pergunta: "Quais materiais sÃ£o necessÃ¡rios?"
4. Supervisor informa os materiais (ou sistema sugere com base no contexto).
5. Sistema gera minuta de e-mail contendo:
   - Descritivo do material
   - Justificativa da solicitaÃ§Ã£o
   - Dados do cliente (nome, empresa)
   - Motivo da solicitaÃ§Ã£o (baseado no atendimento)
   - DestinatÃ¡rio (departamento de compras / almoxarifado)
6. Sistema exibe minuta para revisÃ£o.
7. Supervisor edita se necessÃ¡rio e aprova.
8. Sistema envia e-mail.
9. Sistema registra no histÃ³rico do atendimento: e-mail de compra enviado.

**Fluxo alternativo A â€” Supervisor quer salvar rascunho:**
7a. Supervisor opta por salvar como rascunho.
8a. Sistema salva minuta localmente, associada ao atendimento.

**Regras de negÃ³cio:**
- O e-mail sÃ³ Ã© enviado apÃ³s aprovaÃ§Ã£o explÃ­cita do Supervisor.
- O sistema pode sugerir materiais com base no tipo de atendimento.

---

## UC-007 â€” Gerar E-mail de Comunicado

**Ator principal:** Supervisor
**Atores secundÃ¡rios:** ServiÃ§o de E-mail
**PrÃ©-condiÃ§Ãµes:** Atendimento em andamento ou finalizado, necessidade de comunicado identificada.
**PÃ³s-condiÃ§Ãµes:** E-mail de comunicado enviado (apÃ³s aprovaÃ§Ã£o).

**Fluxo principal:**
1. Supervisor solicita "Gerar E-mail de Comunicado".
2. Sistema pergunta o tipo: "(I) Interno (equipe) / (E) Externo (cliente)".
3. Supervisor seleciona o tipo.
4. Sistema gera minuta com base no resumo do atendimento.
5. Sistema exibe minuta para revisÃ£o.
6. Supervisor edita se necessÃ¡rio e aprova.
7. Sistema envia e-mail.
8. Sistema registra no histÃ³rico do atendimento.

**Regras de negÃ³cio:**
- Comunicado interno: tom informal, para equipe tÃ©cnica.
- Comunicado externo: tom formal, para o cliente.
- O e-mail sÃ³ Ã© enviado apÃ³s aprovaÃ§Ã£o do Supervisor.

---

## UC-008 â€” Consultar HistÃ³rico e Sugerir SoluÃ§Ã£o

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Acompanhamento ativo.
**PÃ³s-condiÃ§Ãµes:** SugestÃ£o de soluÃ§Ã£o exibida com base em casos anteriores.

**Fluxo principal:**
1. Supervisor pergunta ao sistema: "JÃ¡ vimos esse problema antes?" ou "Sugira uma soluÃ§Ã£o".
2. Sistema consulta o banco vetorial e o Obsidian com base no contexto atual (cliente, equipamento, sintomas do problema).
3. Sistema identifica atendimentos anteriores com problemas similares.
4. Sistema retorna:
   - Atendimento(s) anterior(es) relacionados
   - SoluÃ§Ã£o aplicada anteriormente
   - Grau de similaridade
   - Link para a nota no Obsidian
5. Sistema exibe sugestÃ£o para o Supervisor.

**Fluxo alternativo A â€” Nenhum resultado encontrado:**
3a. Sistema nÃ£o encontra casos similares.
4a. Sistema informa: "Nenhum caso similar encontrado no histÃ³rico".
5a. Sistema sugere: "Deseja registrar este atendimento como novo conhecimento?"

**Fluxo alternativo B â€” MÃºltiplos resultados:**
3b. Sistema encontra mÃºltiplos casos similares.
4b. Sistema lista os casos ordenados por relevÃ¢ncia.
5b. Supervisor seleciona um caso para ver detalhes.

**Regras de negÃ³cio:**
- A busca considera: cliente, equipamento, descriÃ§Ã£o do problema, soluÃ§Ãµes aplicadas.
- O grau de similaridade Ã© calculado por embedding semÃ¢ntico.

---

## UC-009 â€” Responder Pergunta Durante Atendimento

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Acompanhamento ativo.
**PÃ³s-condiÃ§Ãµes:** Resposta contextual exibida.

**Fluxo principal:**
1. Supervisor faz uma pergunta em linguagem natural (ex.: "Qual a senha padrÃ£o do equipamento X?").
2. Sistema consulta a base de conhecimento (Obsidian + banco vetorial).
3. Sistema retorna resposta com base no conhecimento registrado.
4. Sistema indica a fonte da resposta (nota do Obsidian, atendimento anterior, etc.).

**Fluxo alternativo A â€” Resposta nÃ£o encontrada:**
3a. Sistema nÃ£o encontra resposta na base.
4a. Sistema informa que nÃ£o tem essa informaÃ§Ã£o.
5a. Sistema pergunta: "Deseja pesquisar na web?" ou "Deseja registrar a resposta quando descobrir?"

**Regras de negÃ³cio:**
- Respostas sÃ£o baseadas exclusivamente no conhecimento registrado (Obsidian + banco vetorial).
- O sistema pode usar o LLM para interpretar a pergunta e buscar a resposta.

---

## UC-010 â€” Revisar e Aprovar AÃ§Ãµes Pendentes

**Ator principal:** Supervisor
**PrÃ©-condiÃ§Ãµes:** Existem aÃ§Ãµes pendentes de aprovaÃ§Ã£o (rascunhos de e-mail, sugestÃµes de fechamento, registros no Obsidian).
**PÃ³s-condiÃ§Ãµes:** AÃ§Ãµes aprovadas, rejeitadas ou editadas conforme decisÃ£o do Supervisor.

**Fluxo principal:**
1. Supervisor acessa o painel de aÃ§Ãµes pendentes.
2. Sistema lista todas as aÃ§Ãµes aguardando aprovaÃ§Ã£o, com prÃ©via de cada uma.
3. Para cada aÃ§Ã£o, Supervisor pode:
   - (A) Aprovar â†’ sistema executa a aÃ§Ã£o.
   - (E) Editar â†’ sistema abre editor para ajustes antes de executar.
   - (R) Rejeitar â†’ sistema descarta a aÃ§Ã£o sem executar.
   - (S) Sonegar â†’ sistema mantÃ©m como pendente para depois.
4. Sistema registra em log a decisÃ£o para cada aÃ§Ã£o.

**Regras de negÃ³cio:**
- AÃ§Ãµes crÃ­ticas nunca expiram automaticamente â€” aguardam decisÃ£o do Supervisor.
- O painel exibe aÃ§Ãµes ordenadas por urgÃªncia.

> Estes casos de uso sÃ£o implementados nos fluxos descritos em [[03-Comportamento/Fluxos.md]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

