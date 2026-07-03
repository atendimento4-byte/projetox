---
title: "Privacidade"
description: "Dados coletados, consentimento, LGPD, retencao e minimizacao"
status: "concluido"
---

# Privacidade

> **Tratamento de dados pessoais, consentimento e conformidade com a LGPD.**
>
> Ver tambÃ©m [[04-Arquitetura/Seguranca.md|SeguranÃ§a]] para mecanismos de proteÃ§Ã£o de dados.

---

## PrincÃ­pios

1. **Consentimento:** Nenhum dado pessoal Ã© coletado sem autorizaÃ§Ã£o explÃ­cita.
2. **Finalidade:** Dados sÃ£o coletados apenas para a finalidade do atendimento tÃ©cnico.
3. **Necessidade:** Apenas os dados estritamente necessÃ¡rios sÃ£o armazenados.
4. **TransparÃªncia:** O usuÃ¡rio sabe exatamente quais dados estÃ£o sendo coletados e por quÃª.
5. **Controle:** O usuÃ¡rio pode solicitar a exclusÃ£o de seus dados a qualquer momento.

---

## 1. Dados Pessoais Coletados

### Pelo Sistema

| Dado | Origem | Finalidade | Armazenamento |
|------|--------|------------|---------------|
| Nome do cliente | Movidesk / usuÃ¡rio | IdentificaÃ§Ã£o do atendimento | Obsidian (nota do cliente) |
| Empresa/CNPJ | Movidesk / usuÃ¡rio | Contexto do atendimento | Obsidian (nota do cliente) |
| Contato (telefone/e-mail) | Movidesk / usuÃ¡rio | ComunicaÃ§Ã£o | Obsidian (nota do cliente) |
| GravaÃ§Ãµes de Ã¡udio | Microfone (com consentimento) | TranscriÃ§Ã£o e memÃ³ria | Disco local (90 dias) |
| Dados de equipamentos | UsuÃ¡rio / atendimento | Registro de configuraÃ§Ãµes | Obsidian (nota do equipamento) |
| HistÃ³rico de atendimentos | Gerado pelo sistema | MemÃ³ria e consulta futura | Obsidian + PostgreSQL |

### Pelo Movidesk (jÃ¡ existente)

O sistema apenas consulta dados jÃ¡ existentes no Movidesk. NÃ£o coleta dados adicionais do Movidesk alÃ©m do necessÃ¡rio para o atendimento.

### Pelo LLM

Nenhum dado pessoal Ã© enviado ao LLM sem que o usuÃ¡rio saiba e aprove. As solicitaÃ§Ãµes ao LLM devem:
- Conter apenas o contexto necessÃ¡rio para a tarefa (ex.: resumo do atendimento, sem nome completo se nÃ£o necessÃ¡rio)
- Ser mascaradas quando possÃ­vel (ex.: usar "Cliente X" em vez do nome real em prompts de sugestÃ£o)

---

## 2. Consentimento

### GravaÃ§Ã£o de Ãudio

- **Nunca** iniciar gravaÃ§Ã£o automaticamente.
- O usuÃ¡rio deve acionar a gravaÃ§Ã£o â†’ sistema exibe confirmaÃ§Ã£o â†’ usuÃ¡rio confirma.
- Indicador visual **obrigatÃ³rio** durante toda a gravaÃ§Ã£o.
- O usuÃ¡rio pode parar a gravaÃ§Ã£o a qualquer momento.
- Log registra: timestamp de inÃ­cio/fim, duraÃ§Ã£o, origem do comando.

### Registro no Obsidian

- O sistema sugere alteraÃ§Ãµes (criaÃ§Ã£o/atualizaÃ§Ã£o de notas).
- O usuÃ¡rio revisa a prÃ©via e aprova/edita/rejeita.
- Nada Ã© escrito no Obsidian sem aprovaÃ§Ã£o.

### Envio de E-mails

- O sistema gera minuta.
- O usuÃ¡rio revisa e aprova o envio.

---

## 3. Conformidade LGPD

### Direitos do Titular (Art. 18 LGPD)

| Direito | Como o sistema atende |
|---------|----------------------|
| ConfirmaÃ§Ã£o da existÃªncia de tratamento | UsuÃ¡rio pode consultar todos os dados armazenados |
| Acesso aos dados | Via consulta no Obsidian e PostgreSQL |
| CorreÃ§Ã£o de dados incompletos/inexatos | UsuÃ¡rio pode editar notas no Obsidian |
| AnonimizaÃ§Ã£o, bloqueio ou eliminaÃ§Ã£o | UsuÃ¡rio pode excluir notas, gravaÃ§Ãµes e dados |
| Portabilidade | Dados em formato .md (Obsidian) e JSON |
| EliminaÃ§Ã£o dos dados tratados com consentimento | ExclusÃ£o manual ou por polÃ­tica de retenÃ§Ã£o |

### Base Legal para Tratamento (Art. 7Âº LGPD)

| Finalidade | Base Legal |
|------------|------------|
| Registro de atendimento tÃ©cnico | LegÃ­timo interesse (Art. 7Âº, IX) |
| GravaÃ§Ã£o de Ã¡udio (quando autorizada) | Consentimento (Art. 7Âº, I) |
| ComunicaÃ§Ã£o com cliente | ExecuÃ§Ã£o de contrato (Art. 7Âº, V) |
| HistÃ³rico e memÃ³ria | LegÃ­timo interesse (Art. 7Âº, IX) |

---

## 4. PolÃ­tica de RetenÃ§Ã£o

| Tipo de Dado | PerÃ­odo | Fundamento | AÃ§Ã£o apÃ³s perÃ­odo |
|--------------|---------|------------|-------------------|
| GravaÃ§Ãµes de Ã¡udio | 90 dias | Necessidade de transcriÃ§Ã£o e revisÃ£o | ExclusÃ£o automÃ¡tica (com aviso prÃ©vio) |
| TranscriÃ§Ãµes e resumos | Indeterminado | MemÃ³ria do atendimento | Mantido no Obsidian |
| Dados de clientes (Obsidian) | Indeterminado | Relacionamento comercial contÃ­nuo | Mantido (atualizÃ¡vel) |
| Logs de auditoria | 1 ano | Compliance e seguranÃ§a | CompactaÃ§Ã£o |
| Cache de API Movidesk | 30 dias | Performance | Limpeza automÃ¡tica |

> A implementaÃ§Ã£o no banco de dados estÃ¡ em [[05-Dados/Banco-de-Dados.md]].

### ExclusÃ£o Antecipada
- O usuÃ¡rio pode solicitar exclusÃ£o de qualquer dado a qualquer momento.
- O sistema deve permitir exclusÃ£o seletiva (apagar gravaÃ§Ã£o de um atendimento especÃ­fico, apagar dados de um cliente).

---

## 5. Medidas de Privacidade

### MinimizaÃ§Ã£o de Dados

- Apenas dados necessÃ¡rios para o atendimento sÃ£o armazenados.
- Dados sensÃ­veis (raÃ§a, religiÃ£o, saÃºde, etc.) **nÃ£o** sÃ£o coletados em hipÃ³tese alguma.
- Se o LLM receber dados do atendimento, apenas o estritamente necessÃ¡rio para a tarefa.

### PseudonimizaÃ§Ã£o

| CenÃ¡rio | Medida |
|---------|--------|
| Prompts para LLM | Substituir nome do cliente por "Cliente #ID" quando possÃ­vel |
| Logs de auditoria | Registrar ID do atendimento, nÃ£o nome completo |
| Compartilhamento externo (futuro) | Pseudonimizar dados antes de compartilhar |

### TransparÃªncia

- O sistema informa ao usuÃ¡rio quando estÃ¡ gravando, processando ou enviando dados.
- O usuÃ¡rio pode consultar a qualquer momento quais dados estÃ£o armazenados.
- PolÃ­tica de privacidade documentada.

---

## 6. Riscos de Privacidade

| Risco | Probabilidade | Impacto | MitigaÃ§Ã£o |
|-------|:------------:|:-------:|-----------|
| GravaÃ§Ã£o acidental de Ã¡udio nÃ£o autorizado | Baixa | CrÃ­tico | Dupla confirmaÃ§Ã£o + indicador visual |
| Vazamento de dados via LLM | Baixa | Alto | MinimizaÃ§Ã£o de dados em prompts |
| Acesso indevido ao vault do Obsidian | Baixa | Alto | Criptografia do vault (opcional) |
| ExposiÃ§Ã£o de dados em backups | Baixa | Alto | Backups criptografados |
| Compartilhamento acidental de dados sensÃ­veis | Baixa | MÃ©dio | RevisÃ£o de conteÃºdo antes de envio |

---

**Premissas:**
- O sistema Ã© de uso individual e local. NÃ£o hÃ¡ compartilhamento de dados com terceiros.
- As gravaÃ§Ãµes de Ã¡udio sÃ£o armazenadas localmente e nÃ£o enviadas a terceiros (exceto para transcriÃ§Ã£o, quando autorizado).

**Riscos:**
- A LGPD exige que o controlador (vocÃª) garanta os direitos dos titulares. O sistema deve facilitar isso.

**DÃºvidas em aberto:**
- Clientes devem ser informados sobre a gravaÃ§Ã£o do atendimento? (Recomendado: aviso no inÃ­cio da chamada.)
- Deve haver um termo de consentimento formal para gravaÃ§Ã£o?

**PrÃ³ximos passos:**
- Detalhar Agentes de IA.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

