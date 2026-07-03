---
title: "Agentes de IA"
description: "5 agentes de IA: Transcricao, Memoria, Documentacao, Comunicacao, Consulta"
status: "concluido"
---

# Agentes (IA)

> **DefiniÃ§Ã£o dos agentes de inteligÃªncia artificial, suas responsabilidades, interaÃ§Ãµes e configuraÃ§Ãµes.**
>
> Os agentes sÃ£o coordenados pelo Hermes conforme definido na [[04-Arquitetura/ADRs.md|ADR-002]].

---

## VisÃ£o Geral

O sistema utiliza mÃºltiplos agentes de IA especializados, coordenados pelo Hermes (orquestrador). Cada agente possui uma responsabilidade especÃ­fica e utiliza o LLM + ferramentas apropriadas para sua funÃ§Ã£o.

```mermaid
flowchart TD
    H[Hermes Orquestrador] --> A1[Agente de TranscriÃ§Ã£o]
    H --> A2[Agente de MemÃ³ria]
    H --> A3[Agente de DocumentaÃ§Ã£o]
    H --> A4[Agente de ComunicaÃ§Ã£o]
    H --> A5[Agente de Consulta]
    
    A1 --> W[Whisper]
    A1 --> L1[LLM - ExtraÃ§Ã£o]
    A2 --> L2[LLM - ClassificaÃ§Ã£o]
    A2 --> V[Banco Vetorial]
    A2 --> O[Obsidian]
    A3 --> L3[LLM - GeraÃ§Ã£o]
    A3 --> M[Movidesk]
    A4 --> L4[LLM - RedaÃ§Ã£o]
    A4 --> E[E-mail]
    A5 --> L5[LLM - AnÃ¡lise]
    A5 --> V
    A5 --> O
```

---

## A01 â€” Agente de TranscriÃ§Ã£o

**Responsabilidade:** Coordenar o processo de transcriÃ§Ã£o de Ã¡udio e extraÃ§Ã£o de pontos-chave.

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Ativado por** | Comando do usuÃ¡rio ("transcrever", "resumir") |
| **Ferramentas** | Whisper (transcriÃ§Ã£o), LLM (extraÃ§Ã£o de pontos-chave) |
| **SaÃ­da** | Resumo estruturado do atendimento |

### Fluxo de Trabalho

1. Recebe solicitaÃ§Ã£o de transcriÃ§Ã£o do Hermes
2. Envia Ã¡udio para Whisper (local ou API)
3. Recebe transcriÃ§Ã£o em texto
4. Envia transcriÃ§Ã£o para LLM com prompt especializado:
   ```
   Extraia os seguintes pontos-chave deste atendimento tÃ©cnico:
   - Problema relatado
   - SoluÃ§Ã£o aplicada
   - Equipamentos envolvidos
   - ConfiguraÃ§Ãµes realizadas
   - ObservaÃ§Ãµes relevantes
   
   TranscriÃ§Ã£o: [texto]
   ```
5. Estrutura o resultado em formato padronizado
6. Retorna ao Hermes para exibiÃ§Ã£o e aprovaÃ§Ã£o

### Prompt Especializado

```
VocÃª Ã© um assistente especializado em atendimentos tÃ©cnicos.
Analise a transcriÃ§Ã£o fornecida e extraia APENAS as informaÃ§Ãµes
solicitadas. Seja objetivo e tÃ©cnico. Use termos padronizados.

Formato de saÃ­da (Markdown):
- Problema: [descriÃ§Ã£o concisa]
- SoluÃ§Ã£o: [descriÃ§Ã£o concisa]
- Equipamentos: [lista separada por vÃ­rgulas]
- ConfiguraÃ§Ãµes: [lista de configuraÃ§Ãµes alteradas]
- ObservaÃ§Ãµes: [informaÃ§Ãµes adicionais relevantes]
```

---

## A02 â€” Agente de MemÃ³ria

**Responsabilidade:** Gerenciar o registro de conhecimento no Obsidian de forma organizada e estruturada.

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Ativado por** | Comando do usuÃ¡rio ("registrar no Obsidian", "salvar conhecimento") |
| **Ferramentas** | LLM (classificaÃ§Ã£o e estruturaÃ§Ã£o), Obsidian adapter, Banco Vetorial |
| **SaÃ­da** | Notas criadas/atualizadas no Obsidian |

### Fluxo de Trabalho

1. Recebe solicitaÃ§Ã£o de registro + conteÃºdo do atendimento
2. Analisa o conteÃºdo e identifica entidades:
   - Cliente (nome, empresa, contato)
   - Equipamentos (tipo, modelo, configuraÃ§Ãµes)
   - Procedimentos (passos executados)
   - SoluÃ§Ãµes (problema â†’ soluÃ§Ã£o)
3. Verifica no Obsidian se entidades jÃ¡ existem
4. Sugere estrutura de notas:
   - Se cliente novo: criar nota em `Clientes/{Cliente}.md`
   - Se cliente existente: atualizar nota com novo atendimento
   - Se equipamento novo: criar nota em `Equipamentos/{Tipo}/{Equipamento}.md`
   - Se soluÃ§Ã£o recorrente: vincular Ã  soluÃ§Ã£o existente
5. Gera conteÃºdo das notas com links entre elas
6. Retorna prÃ©via para aprovaÃ§Ã£o do usuÃ¡rio
7. ApÃ³s aprovaÃ§Ã£o, executa a criaÃ§Ã£o/atualizaÃ§Ã£o

### Regras de EstruturaÃ§Ã£o

| Entidade | Pasta | Nome do Arquivo | Formato |
|----------|-------|-----------------|---------|
| Cliente | `Clientes/` | `Nome da Empresa.md` | Frontmatter + HistÃ³rico |
| Equipamento | `Equipamentos/{Tipo}/` | `Modelo.md` | EspecificaÃ§Ãµes + Atendimentos |
| Procedimento | `Procedimentos/` | `Nome do Procedimento.md` | Passos + Equipamentos |
| SoluÃ§Ã£o | `Solucoes/` | `Problema - SoluÃ§Ã£o.md` | Problema + Causa + SoluÃ§Ã£o |
| Atendimento | `Atendimentos/{Ano}/` | `YYYY-MM-DD - Cliente - Resumo.md` | Resumo + Links |

> A estrutura do vault que este agente manipula estÃ¡ em [[05-Dados/Memoria-Obsidian.md]].

---

## A03 â€” Agente de DocumentaÃ§Ã£o (OS)

**Responsabilidade:** Sugerir o preenchimento do fechamento da Ordem de ServiÃ§o com base no resumo do atendimento.

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Ativado por** | Comando do usuÃ¡rio ("sugerir fechamento", "fechar OS") |
| **Ferramentas** | LLM (geraÃ§Ã£o de resumo tÃ©cnico), Movidesk adapter |
| **SaÃ­da** | PrÃ©via de fechamento de OS para aprovaÃ§Ã£o |

### Fluxo de Trabalho

1. Recebe solicitaÃ§Ã£o + resumo do atendimento + dados do chamado
2. Verifica no chamado se hÃ¡ tÃ©cnico parceiro associado
3. Gera conteÃºdo para campos do Movidesk:
   - **Resumo tÃ©cnico:** Texto descritivo do serviÃ§o executado
   - **ConfiguraÃ§Ãµes realizadas:** Lista de alteraÃ§Ãµes
   - **Equipamentos trocados:** Lista com modelos e quantidades
   - **Hora/data:** Preenchido automaticamente
4. Determina status adequado:
   - Com tÃ©cnico parceiro â†’ "Retorno da OS"
   - Sem tÃ©cnico parceiro â†’ "Resolvido"
5. Retorna prÃ©via completa para revisÃ£o do usuÃ¡rio
6. ApÃ³s aprovaÃ§Ã£o, envia ao Movidesk

### Prompt Especializado

```
Com base no resumo do atendimento tÃ©cnico abaixo, gere o conteÃºdo
para o fechamento de uma Ordem de ServiÃ§o no Movidesk.

Seja tÃ©cnico e objetivo. Inclua apenas informaÃ§Ãµes relevantes.

Resumo: [resumo]

Campos a preencher:
1. Resumo TÃ©cnico (2-3 parÃ¡grafos)
2. ConfiguraÃ§Ãµes Realizadas (lista)
3. Equipamentos Envolvidos/Trocados (lista)
```

---

## A04 â€” Agente de ComunicaÃ§Ã£o

**Responsabilidade:** Gerar minutas de e-mail (solicitaÃ§Ã£o de compra e comunicados) com base no contexto do atendimento.

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Ativado por** | Comando do usuÃ¡rio ("gerar e-mail de compra", "gerar comunicado") |
| **Ferramentas** | LLM (redaÃ§Ã£o), E-mail adapter |
| **SaÃ­da** | Minuta de e-mail para revisÃ£o |

### Fluxo de Trabalho

**E-mail de SolicitaÃ§Ã£o de Compra:**
1. Pergunta ao usuÃ¡rio quais materiais sÃ£o necessÃ¡rios (ou infere do contexto)
2. Gera minuta com: descritivo do material, justificativa, dados do cliente
3. Usa template: SolicitaÃ§Ã£o de Compra - {Cliente} - {Material}
4. Retorna minuta para revisÃ£o

**E-mail de Comunicado:**
1. Pergunta o tipo: interno (equipe) ou externo (cliente)
2. Gera minuta com tom apropriado:
   - Interno: informal, direto
   - Externo: formal, educado
3. Inclui resumo do atendimento
4. Retorna minuta para revisÃ£o

### Templates Base

**SolicitaÃ§Ã£o de Compra:**
```
Assunto: SolicitaÃ§Ã£o de Compra - {Cliente} - {Material}

Prezados,

Solicito a compra do(s) seguinte(s) material(is) para atendimento
ao cliente {Cliente}:

{Lista de materiais}

Justificativa: {Justificativa}

Atenciosamente,
{Nome}
```

**Comunicado Externo:**
```
Assunto: {Assunto} - {Cliente}

Prezado(a) {Cliente},

Informamos que o atendimento referente a {Assunto} foi realizado.
{Resumo do atendimento}

Segue em anexo a documentaÃ§Ã£o do serviÃ§o.

Atenciosamente,
{Equipe}
```

---

## A05 â€” Agente de Consulta

**Responsabilidade:** Responder perguntas do usuÃ¡rio com base na base de conhecimento e sugerir soluÃ§Ãµes com base em casos anteriores.

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Ativado por** | Pergunta do usuÃ¡rio em linguagem natural ou comando de sugestÃ£o |
| **Ferramentas** | LLM (anÃ¡lise e compreensÃ£o), Banco Vetorial, Obsidian adapter |
| **SaÃ­da** | Resposta contextualizada com fontes |

### Fluxo de Trabalho

1. Recebe pergunta do usuÃ¡rio (ex.: "Qual a senha padrÃ£o do equipamento X?", "JÃ¡ vimos esse problema antes?")
2. Extrai termos de busca da pergunta
3. Consulta banco vetorial (Qdrant) por similaridade semÃ¢ntica
4. Consulta Obsidian por matching de tags e palavras-chave
5. Combina resultados e ranqueia por relevÃ¢ncia
6. Envia contexto + pergunta para LLM gerar resposta
7. Retorna resposta com indicaÃ§Ã£o das fontes (links para notas do Obsidian)

### Exemplos de Perguntas

| Pergunta | AÃ§Ã£o |
|----------|------|
| "Qual a senha do roteador do cliente X?" | Busca equipamento â†’ senha no Obsidian |
| "JÃ¡ resolvemos esse problema antes?" | Busca similaridade semÃ¢ntica no banco vetorial |
| "Qual procedimento para instalaÃ§Ã£o do equipamento Y?" | Busca procedimento no Obsidian |
| "Quando foi o Ãºltimo atendimento do cliente Z?" | Busca histÃ³rico do cliente |

---

## Matriz de Agentes vs LLM Usage

| Agente | Tarefa | Modelo Recomendado | Custo Relativo |
|--------|--------|-------------------|:--------------:|
| A01 â€” TranscriÃ§Ã£o | ExtraÃ§Ã£o de pontos-chave | Haiku / 4o-mini | Baixo |
| A02 â€” MemÃ³ria | ClassificaÃ§Ã£o e estruturaÃ§Ã£o | Sonnet / 4o | MÃ©dio |
| A03 â€” DocumentaÃ§Ã£o | GeraÃ§Ã£o de resumo tÃ©cnico | Sonnet / 4o | MÃ©dio |
| A04 â€” ComunicaÃ§Ã£o | RedaÃ§Ã£o de e-mails | Haiku / 4o-mini | Baixo |
| A05 â€” Consulta | AnÃ¡lise e resposta | Sonnet / 4o | MÃ©dio |

---

## OrquestraÃ§Ã£o pelo Hermes

O Hermes coordena os agentes da seguinte forma:

1. **Recebe comando do usuÃ¡rio** (via CLI)
2. **Interpreta a intenÃ§Ã£o** (qual agente acionar)
3. **Aciona o agente** com contexto necessÃ¡rio
4. **Aguarda resultado** ou **executa em background** (com notificaÃ§Ã£o)
5. **Apresenta resultado** para revisÃ£o do usuÃ¡rio
6. **Aguarda aprovaÃ§Ã£o** antes de executar aÃ§Ãµes externas
7. **Executa e registra** apÃ³s aprovaÃ§Ã£o

### Exemplo de Fluxo Completo

```
UsuÃ¡rio: "iniciar acompanhamento 12345"
â†’ Hermes: Aciona Acompanhamento â†’ consulta Movidesk â†’ cria sessÃ£o

UsuÃ¡rio: "gravar" (hotkey)
â†’ Hermes: Pede confirmaÃ§Ã£o â†’ inicia gravaÃ§Ã£o

UsuÃ¡rio: "parar"
â†’ Hermes: Para gravaÃ§Ã£o â†’ salva Ã¡udio

UsuÃ¡rio: "transcrever"
â†’ Hermes: Aciona A01 (TranscriÃ§Ã£o) â†’ envia Ã¡udio â†’ recebe resumo â†’ exibe

UsuÃ¡rio: "salvar conhecimento"
â†’ Hermes: Aciona A02 (MemÃ³ria) â†’ analisa conteÃºdo â†’ sugere notas â†’ exibe prÃ©via

UsuÃ¡rio: "aprovar tudo"
â†’ Hermes: Executa todas as aÃ§Ãµes aprovadas â†’ Obsidian: criar notas
                                                      â†’ A03: gerar fechamento
                                                      â†’ exibe prÃ©via fechamento

UsuÃ¡rio: "fechar OS"
â†’ Hermes: Envia fechamento para Movidesk â†’ registra em log
```

---

**Premissas:**
- Cada agente utiliza o LLM via a mesma interface (ILLM), com prompts especializados.
- Agentes podem ser refinados, fundidos ou divididos conforme necessidade.

**Riscos:**
- Agentes dependentes de LLM podem gerar respostas inconsistentes se os prompts nÃ£o forem bem calibrados.
- Custo de LLM pode aumentar com uso frequente de modelos mais caros (A03, A05).

**DÃºvidas em aberto:**
- Os agentes devem ter "personalidade" ou tom especÃ­fico?
- Deve haver logging separado por agente para debugging?

**PrÃ³ximos passos:**
- Detalhar Banco de Dados e MemÃ³ria (Obsidian).

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

