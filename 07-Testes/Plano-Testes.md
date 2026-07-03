---
title: "Plano de Testes"
description: "Matriz com 30+ testes por agente (A01-A05)"
status: "novo"
---

# Plano de Testes

> **Matriz completa de testes por loop, agente e fluxo. Cada caso de teste possui ID, objetivo, prÃ©-condiÃ§Ãµes, entradas, resultado esperado e prioridade.**

---

## 1. ConvenÃ§Ãµes

| Campo | DescriÃ§Ã£o |
|-------|-----------|
| **ID** | Identificador Ãºnico do teste |
| **Objetivo** | O que o teste valida |
| **PrÃ©-condiÃ§Ãµes** | Estado necessÃ¡rio antes do teste |
| **Entradas** | Dados fornecidos ao sistema |
| **Resultado esperado** | Comportamento esperado apÃ³s execuÃ§Ã£o |
| **Prioridade** | P0 (bloqueante) / P1 (importante) / P2 (desejÃ¡vel) |

---

## 2. Testes de Loop de Agente

### A01 â€” Agente de TranscriÃ§Ã£o

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-A01-001 | Transcrever Ã¡udio com sucesso | Ãudio vÃ¡lido disponÃ­vel, Whisper mock pronto | Arquivo WAV 30s | Texto transcrito retornado | P0 |
| T-A01-002 | TranscriÃ§Ã£o com Ã¡udio corrompido | Ãudio invÃ¡lido | Arquivo binÃ¡rio corrompido | Erro de transcriÃ§Ã£o com mensagem clara | P0 |
| T-A01-003 | ExtraÃ§Ã£o de pontos-chave via LLM | TranscriÃ§Ã£o completa | Texto transcrito + prompt | Resumo estruturado com problema, soluÃ§Ã£o, decisÃµes | P0 |
| T-A01-004 | LLM retorna resposta inconsistente | Ãudio vÃ¡lido, LLM mock configurado para erro | Ãudio vÃ¡lido | Re-prompt atÃ© 3x, depois erro notificado | P1 |

### A02 â€” Agente de MemÃ³ria

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-A02-001 | AnÃ¡lise de entidades | TranscriÃ§Ã£o completa | Texto do atendimento | Lista de entidades (cliente, equipamento, soluÃ§Ã£o) | P0 |
| T-A02-002 | CriaÃ§Ã£o de nota com template | Entidades identificadas, vault mock | Dados estruturados | Nota criada no diretÃ³rio correto com frontmatter | P0 |
| T-A02-003 | DetecÃ§Ã£o de entidade existente | Cliente jÃ¡ existe no vault | Nome do cliente | Link para nota existente em vez de criar nova | P0 |
| T-A02-004 | AtualizaÃ§Ã£o de nota existente | Nota do cliente existe | Nova informaÃ§Ã£o | Nota atualizada com novo conteÃºdo + histÃ³rico | P1 |

### A03 â€” Agente de DocumentaÃ§Ã£o

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-A03-001 | GeraÃ§Ã£o de resumo de OS | TranscriÃ§Ã£o + dados da sessÃ£o | Texto completo | Resumo tÃ©cnico formatado para Movidesk | P0 |
| T-A03-002 | DefiniÃ§Ã£o de status OS | InformaÃ§Ã£o se tÃ©cnico esteve presente | Dados da sessÃ£o | Status "Resolvido" ou "Retorno da OS" correto | P0 |
| T-A03-003 | Resumo rejeitado pelo usuÃ¡rio | Resumo gerado, aguardando aprovaÃ§Ã£o | Comando "rejeitar" | Resumo descartado, log registrado | P0 |

### A04 â€” Agente de ComunicaÃ§Ã£o

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-A04-001 | GeraÃ§Ã£o de e-mail de compra | Dados do chamado + peÃ§as | Template + dados | E-mail formatado com itens e justificativa | P0 |
| T-A04-002 | GeraÃ§Ã£o de comunicado | Dados do atendimento | Template + dados | Comunicado formatado | P0 |
| T-A04-003 | Envio de e-mail com aprovaÃ§Ã£o | E-mail gerado, usuÃ¡rio aprova | Comando "aprovar" | E-mail marcado como enviado no mock | P0 |

### A05 â€” Agente de Consulta

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-A05-001 | Busca semÃ¢ntica com resultados | Qdrant mock com dados indexados | Pergunta do usuÃ¡rio | Lista de resultados por similaridade | P0 |
| T-A05-002 | Busca sem resultados relevantes | Qdrant mock vazio | Pergunta sem match | Mensagem "Nenhum resultado relevante" | P0 |
| T-A05-003 | SugestÃ£o durante atendimento | SessÃ£o ativa, histÃ³rico disponÃ­vel | Contexto atual | SugestÃ£o exibida baseada em casos similares | P1 |

---

## 3. Testes de Loop de OrquestraÃ§Ã£o

| ID | Objetivo | PrÃ©-condiÃ§Ãµes | Entradas | Resultado esperado | Prio |
|:--:|----------|---------------|----------|--------------------|:----:|
| T-ORQ-001 | Fluxo completo de acompanhamento | Todos os mocks prontos | Comando `iniciar` â†’ `gravar` â†’ `parar` â†’ `transcrever` â†’ `salvar` â†’ `finalizar` | Cada etapa executa e produz saÃ­da esperada | P0 |
| T-ORQ-002 | Cancelamento durante gravaÃ§Ã£o | SessÃ£o ativa, gravando | Ctrl+C | GravaÃ§Ã£o interrompida, Ã¡udio parcial salvo, sessÃ£o consistente | P0 |
| T-ORQ-003 | AprovaÃ§Ã£o em lote | MÃºltiplas aÃ§Ãµes pendentes | Comando `aprovar tudo` | Todas as aÃ§Ãµes aprovadas executadas em ordem | P0 |
| T-ORQ-004 | RejeiÃ§Ã£o de aÃ§Ã£o crÃ­tica | AÃ§Ã£o que modifica sistema externo | Comando `rejeitar` | AÃ§Ã£o descartada, log registrado | P0 |
| T-ORQ-005 | Timeout no agente | Agente mock configurado para timeout | Qualquer comando | Timeout detectado, usuÃ¡rio notificado | P1 |

---

## 4. Testes de Fluxo

| ID | Objetivo | Fluxo | Prio |
|:--:|----------|:-----:|:----:|
| T-FLUXO-001 | Macro do atendimento completo executado sem erros | Fluxo 1 | P0 |
| T-FLUXO-002 | GravaÃ§Ã£o e transcriÃ§Ã£o com interrupÃ§Ã£o | Fluxo 2 | P0 |
| T-FLUXO-003 | Registro de conhecimento com aprovaÃ§Ã£o | Fluxo 3 | P0 |
| T-FLUXO-004 | Fechamento de OS com status correto | Fluxo 4 | P0 |
| T-FLUXO-005 | GeraÃ§Ã£o de e-mail com template | Fluxo 5 | P0 |
| T-FLUXO-006 | Consulta de histÃ³rico com sugestÃ£o | Fluxo 6 | P1 |
| T-FLUXO-007 | Painel de aprovaÃ§Ãµes com mÃºltiplas aÃ§Ãµes | Fluxo 7 | P0 |

> Ver [[03-Comportamento/Fluxos.md|Fluxos]] para detalhes de cada fluxo.

---

## 5. Testes de SeguranÃ§a

| ID | Objetivo | Prio |
|:--:|----------|:----:|
| T-SEG-001 | AÃ§Ã£o sem aprovaÃ§Ã£o Ã© bloqueada | P0 |
| T-SEG-002 | Comando sem sessÃ£o ativa Ã© rejeitado | P0 |
| T-SEG-003 | Log registra todas as aÃ§Ãµes (inclusive bloqueadas) | P0 |
| T-SEG-004 | Token invÃ¡lido no Named Pipe Ã© rejeitado | P1 |
| T-SEG-005 | Dados sensÃ­veis nÃ£o aparecem em logs | P1 |

---

## 6. Testes de Observabilidade

| ID | Objetivo | Prio |
|:--:|----------|:----:|
| T-OBS-001 | Log estruturado gerado para cada aÃ§Ã£o | P0 |
| T-OBS-002 | Correlation ID propagado em toda cadeia | P0 |
| T-OBS-003 | MÃ©tricas de execuÃ§Ã£o emitidas | P0 |
| T-OBS-004 | Log de auditoria completo ao final da execuÃ§Ã£o | P0 |

---

## 7. Testes Humanos

| ID | Objetivo | Roteiro |
|:--:|----------|---------|
| T-HUM-001 | Fluxo completo de atendimento real | Iniciar â†’ gravar â†’ transcrever â†’ resumir â†’ salvar â†’ fechar |
| T-HUM-002 | Qualidade da transcriÃ§Ã£o | Comparar transcriÃ§Ã£o com Ã¡udio original |
| T-HUM-003 | Clareza das sugestÃµes | SugestÃ£o faz sentido? FÃ¡cil de entender? |
| T-HUM-004 | ExperiÃªncia de aprovaÃ§Ã£o | Processo de aprovaÃ§Ã£o Ã© fluido ou atrapalha? |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

