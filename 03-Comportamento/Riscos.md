---
title: "Riscos"
description: "11 riscos mapeados com matriz de ADRs vinculadas"
status: "concluido"
---

# Riscos

> **IdentificaÃ§Ã£o, anÃ¡lise e planos de mitigaÃ§Ã£o de riscos do projeto.**
> Cada risco Ã© classificado por probabilidade, impacto e severidade.

---

## Legenda

| Atributo | Valores |
|----------|---------|
| **Probabilidade** | Baixa / MÃ©dia / Alta |
| **Impacto** | Baixo / MÃ©dio / Alto / CrÃ­tico |
| **Severidade** | Baixa / MÃ©dia / Alta / CrÃ­tica |
| **Status** | Aberto / Mitigado / Aceito / Encerrado |

---

## Riscos TÃ©cnicos

### RISK-TEC-001 â€” Falha na TranscriÃ§Ã£o de Ãudio

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | O Whisper pode nÃ£o transcrever corretamente Ã¡udios com ruÃ­do ambiente, sotaques carregados, termos tÃ©cnicos ou baixa qualidade de Ã¡udio. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-003]] |
| **MitigaÃ§Ã£o** | Implementar validaÃ§Ã£o da qualidade do Ã¡udio antes do envio. Oferecer opÃ§Ã£o de correÃ§Ã£o manual da transcriÃ§Ã£o. Treinar modelo com vocabulÃ¡rio tÃ©cnico do domÃ­nio (fine-tuning). |
| **Plano de contingÃªncia** | UsuÃ¡rio pode digitar o resumo manualmente se a transcriÃ§Ã£o falhar repetidamente. |

### RISK-TEC-002 â€” LatÃªncia do LLM

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | O tempo de resposta do LLM (Claude/GPT/Gemini) pode ser alto durante horÃ¡rios de pico, impactando a fluidez do atendimento. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | MÃ©dio |
| **Severidade** | MÃ©dia |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-002]] |
| **MitigaÃ§Ã£o** | Implementar cache de respostas frequentes. Usar modelo local (via Ollama) para consultas simples. Exibir indicador de "processando" para feedback ao usuÃ¡rio. |
| **Plano de contingÃªncia** | UsuÃ¡rio pode continuar o atendimento sem IA e solicitar processamento posterior. |

### RISK-TEC-003 â€” DependÃªncia de API do Movidesk

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | A API do Movidesk pode sofrer alteraÃ§Ãµes, ficar indisponÃ­vel ou ter limitaÃ§Ãµes de rate limit que impactam as integraÃ§Ãµes. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-007]] |
| **MitigaÃ§Ã£o** | Implementar camada de abstraÃ§Ã£o sobre a API do Movidesk (adapter pattern). Documentar versÃ£o da API utilizada. Monitorar disponibilidade. |
| **Plano de contingÃªncia** | Manter modo offline com registro local e sincronizaÃ§Ã£o posterior quando a API retornar. |

### RISK-TEC-004 â€” Qualidade da GravaÃ§Ã£o de Ãudio

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | A gravaÃ§Ã£o de Ã¡udio pode capturar ruÃ­do ambiente, eco, mÃºltiplas vozes simultÃ¢neas ou baixo volume, comprometendo a transcriÃ§Ã£o. |
| **Probabilidade** | Alta |
| **Impacto** | MÃ©dio |
| **Severidade** | MÃ©dia |
| **Status** | Aberto |
| **ADR Relacionado** | â€” |
| **MitigaÃ§Ã£o** | Implementar filtro de ruÃ­do bÃ¡sico. Orientar uso de microfone adequado. Validar nÃ­vel de Ã¡udio antes da gravaÃ§Ã£o. |
| **Plano de contingÃªncia** | UsuÃ¡rio pode complementar a transcriÃ§Ã£o manualmente. |

### RISK-TEC-005 â€” Perda de Dados no Obsidian

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | O vault do Obsidian pode corromper, arquivos podem ser sobrescritos incorretamente ou dados podem ser perdidos por erro do sistema. |
| **Probabilidade** | Baixa |
| **Impacto** | CrÃ­tico |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-001]] |
| **MitigaÃ§Ã£o** | Implementar backup automÃ¡tico do vault (versÃµes locais + nuvem). Usar operaÃ§Ãµes atÃ´micas de escrita. Manter git como versionamento do vault. |
| **Plano de contingÃªncia** | Restaurar backup mais recente. Recuperar dados perdidos via logs de auditoria. |

### RISK-TEC-006 â€” Conflito de Notas no Obsidian

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | O sistema pode criar notas duplicadas ou links inconsistentes no Obsidian se a lÃ³gica de identificaÃ§Ã£o de entidades falhar. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | MÃ©dio |
| **Severidade** | MÃ©dia |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-001]] |
| **MitigaÃ§Ã£o** | Implementar validaÃ§Ã£o antes da criaÃ§Ã£o de notas (verificar se jÃ¡ existe). Exibir prÃ©via das alteraÃ§Ãµes para aprovaÃ§Ã£o do usuÃ¡rio. |
| **Plano de contingÃªncia** | UsuÃ¡rio pode corrigir manualmente as notas no Obsidian. |

---

## Riscos de SeguranÃ§a e Privacidade

### RISK-SEG-001 â€” GravaÃ§Ã£o NÃ£o Autorizada

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | A gravaÃ§Ã£o de Ã¡udio pode iniciar sem o conhecimento do usuÃ¡rio (bug, falha de seguranÃ§a, acionamento acidental). |
| **Probabilidade** | Baixa |
| **Impacto** | CrÃ­tico |
| **Severidade** | CrÃ­tica |
| **Status** | Mitigado |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-012]] |
| **MitigaÃ§Ã£o** | Dupla confirmaÃ§Ã£o obrigatÃ³ria. Indicador visual sempre presente durante gravaÃ§Ã£o. Log de auditoria com timestamp. Testes de seguranÃ§a especÃ­ficos. |
| **Plano de contingÃªncia** | Parada imediata da gravaÃ§Ã£o + notificaÃ§Ã£o + exclusÃ£o do arquivo nÃ£o autorizado. |

### RISK-SEG-002 â€” Vazamento de Dados de Clientes

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | Dados de clientes armazenados no Obsidian ou no banco de dados podem ser acessados por terceiros nÃ£o autorizados. |
| **Probabilidade** | Baixa |
| **Impacto** | CrÃ­tico |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | â€” |
| **MitigaÃ§Ã£o** | Criptografia em repouso (AES-256). AutenticaÃ§Ã£o do usuÃ¡rio. NÃ£o compartilhar vault em nuvem sem criptografia adicional. |
| **Plano de contingÃªncia** | RotaÃ§Ã£o de chaves. NotificaÃ§Ã£o ao usuÃ¡rio. RevisÃ£o de acesso. |

### RISK-SEG-003 â€” ExposiÃ§Ã£o de Chaves de API

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | Chaves de API (LLM, Movidesk, e-mail) podem ser expostas em cÃ³digo, logs ou arquivos de configuraÃ§Ã£o. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-010]] |
| **MitigaÃ§Ã£o** | Uso de variÃ¡veis de ambiente ou vault de secrets (ex.: Windows Credential Manager). Nunca hardcodar chaves. .gitignore para arquivos de configuraÃ§Ã£o. |
| **Plano de contingÃªncia** | Rotacionar chaves imediatamente. Remover exposiÃ§Ã£o. |

---

## Riscos de Projeto

### RISK-PROJ-001 â€” Escopo Crescente (Scope Creep)

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | Novas funcionalidades podem ser solicitadas durante o desenvolvimento, aumentando o escopo alÃ©m do planejado. |
| **Probabilidade** | Alta |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | â€” |
| **MitigaÃ§Ã£o** | Definir MVP claro. Usar backlog priorizado. Toda nova funcionalidade deve passar por anÃ¡lise de impacto antes de ser adicionada. |
| **Plano de contingÃªncia** | Realocar funcionalidades para versÃµes futuras. |

### RISK-PROJ-002 â€” Complexidade de IntegraÃ§Ã£o

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | A integraÃ§Ã£o entre mÃºltiplos sistemas (Hermes, Obsidian, Movidesk, n8n, LLM, banco vetorial) pode ser mais complexa que o estimado. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | [[04-Arquitetura/ADRs.md\|ADR-007]] |
| **MitigaÃ§Ã£o** | Definir interfaces claras entre componentes. Prototipar integraÃ§Ãµes crÃ­ticas primeiro. Isolar cada integraÃ§Ã£o em mÃ³dulo independente. |
| **Plano de contingÃªncia** | Simplificar integraÃ§Ãµes no MVP (ex.: reduzir nÃºmero de serviÃ§os integrados). |

### RISK-PROJ-003 â€” Curva de Aprendizado das Tecnologias

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | Tecnologias como banco vetorial, Hermes (orquestrador) e MCP podem exigir aprendizado adicional que impacta o cronograma. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | MÃ©dio |
| **Severidade** | MÃ©dia |
| **Status** | Aberto |
| **ADR Relacionado** | â€” |
| **MitigaÃ§Ã£o** | Reservar tempo para POC (prova de conceito) de cada tecnologia antes da implementaÃ§Ã£o completa. |
| **Plano de contingÃªncia** | Substituir tecnologia por alternativa mais conhecida se o aprendizado for muito custoso. |

---

## Riscos de NegÃ³cio

### RISK-NEG-001 â€” Baixa AdoÃ§Ã£o

| Atributo | Valor |
|----------|-------|
| **DescriÃ§Ã£o** | O sistema pode nÃ£o ser adotado no dia a dia se for mais lento ou mais complexo que o processo manual atual. |
| **Probabilidade** | MÃ©dia |
| **Impacto** | Alto |
| **Severidade** | Alta |
| **Status** | Aberto |
| **ADR Relacionado** | â€” |
| **MitigaÃ§Ã£o** | Foco em usabilidade e reduÃ§Ã£o real de tempo. Desenvolver com feedback contÃ­nuo do usuÃ¡rio. MVP enxuto que resolve a maior dor primeiro. |
| **Plano de contingÃªncia** | Identificar gargalos de adoÃ§Ã£o e iterar. |

---

## Matriz de Riscos

| ID | Risco | Probabilidade | Impacto | Severidade | Status | ADR Relacionado |
|----|-------|:------------:|:-------:|:----------:|:------:|
| RISK-TEC-001 | Falha na transcriÃ§Ã£o | MÃ©dia | Alto | Alta | Aberto | [[04-Arquitetura/ADRs.md\|ADR-003]] |
| RISK-TEC-002 | LatÃªncia do LLM | MÃ©dia | MÃ©dio | MÃ©dia | Aberto | [[04-Arquitetura/ADRs.md\|ADR-002]] |
| RISK-TEC-003 | DependÃªncia API Movidesk | MÃ©dia | Alto | Alta | Aberto | [[04-Arquitetura/ADRs.md\|ADR-007]] |
| RISK-TEC-004 | Qualidade da gravaÃ§Ã£o | Alta | MÃ©dio | MÃ©dia | Aberto | â€” |
| RISK-TEC-005 | Perda de dados Obsidian | Baixa | CrÃ­tico | Alta | Aberto | [[04-Arquitetura/ADRs.md\|ADR-001]] |
| RISK-TEC-006 | Conflito de notas | MÃ©dia | MÃ©dio | MÃ©dia | Aberto | [[04-Arquitetura/ADRs.md\|ADR-001]] |
| RISK-SEG-001 | GravaÃ§Ã£o nÃ£o autorizada | Baixa | CrÃ­tico | CrÃ­tica | Mitigado | [[04-Arquitetura/ADRs.md\|ADR-012]] |
| RISK-SEG-002 | Vazamento de dados | Baixa | CrÃ­tico | Alta | Aberto | â€” |
| RISK-SEG-003 | ExposiÃ§Ã£o de chaves API | MÃ©dia | Alto | Alta | Aberto | [[04-Arquitetura/ADRs.md\|ADR-010]] |
| RISK-PROJ-001 | Escopo crescente | Alta | Alto | Alta | Aberto | â€” |
| RISK-PROJ-002 | Complexidade integraÃ§Ã£o | MÃ©dia | Alto | Alta | Aberto | [[04-Arquitetura/ADRs.md\|ADR-007]] |
| RISK-PROJ-003 | Curva de aprendizado | MÃ©dia | MÃ©dio | MÃ©dia | Aberto | â€” |
| RISK-NEG-001 | Baixa adoÃ§Ã£o | MÃ©dia | Alto | Alta | Aberto | â€” |

---

**Premissas:**
- Riscos devem ser revisados a cada fase do projeto.
- Novos riscos podem ser adicionados conforme o projeto avanÃ§a.

**Riscos:**
- (Meta-risco) Riscos nÃ£o identificados podem surgir durante a implementaÃ§Ã£o.

**DÃºvidas em aberto:**
- Devem ser mapeados riscos financeiros (custo de APIs, hospedagem)?
- Deve haver um plano de resposta a incidentes de seguranÃ§a formal?

**PrÃ³ximos passos:**
- Iniciar documentaÃ§Ã£o de Arquitetura e DecisÃµes de Arquitetura (ADRs).

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

