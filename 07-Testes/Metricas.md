---
title: "Metricas"
description: "Metricas de sucesso, performance, qualidade, custo e alertas"
status: "novo"
---

# MÃ©tricas

> **MÃ©tricas obrigatÃ³rias para monitorar, avaliar e melhorar loops, agentes e fluxos do sistema.**

---

## 1. MÃ©tricas por ExecuÃ§Ã£o

### 1.1 â€” MÃ©tricas de Sucesso

| MÃ©trica | FÃ³rmula | Unidade | FrequÃªncia |
|---------|---------|:-------:|:----------:|
| Taxa de sucesso | `execuÃ§Ãµes_sucesso / total_execucoes * 100` | % | Por execuÃ§Ã£o |
| Taxa de erro | `execuÃ§Ãµes_erro / total_execucoes * 100` | % | Por execuÃ§Ã£o |
| Objetivo alcanÃ§ado | `1` se objetivo atingido, `0` se nÃ£o | binÃ¡rio | Por execuÃ§Ã£o |

### 1.2 â€” MÃ©tricas de Performance

| MÃ©trica | DescriÃ§Ã£o | Coleta |
|---------|-----------|--------|
| Tempo total | DuraÃ§Ã£o do loop do inÃ­cio ao fim (ms) | Timestamp inÃ­cio - fim |
| NÃºmero de iteraÃ§Ãµes | Contagem de iteraÃ§Ãµes do loop | Contador por execuÃ§Ã£o |
| Chamadas ao LLM | NÃºmero de chamadas ao modelo | Contador de chamadas |
| Tokens de entrada | Total de tokens de prompt + contexto | Soma de cada chamada |
| Tokens de saÃ­da | Total de tokens de resposta | Soma de cada chamada |
| Chamadas Ã s ferramentas | NÃºmero de ferramentas utilizadas | Contador de tool calls |

### 1.3 â€” MÃ©tricas de Qualidade

| MÃ©trica | DescriÃ§Ã£o | Coleta |
|---------|-----------|--------|
| CorreÃ§Ãµes necessÃ¡rias | NÃºmero de re-prompts por respostas invÃ¡lidas | Contador por execuÃ§Ã£o |
| DÃ©jÃ  vu | NÃºmero de vezes que resposta repetida foi detectada | Contador |
| Falhas recuperadas | Falhas que o sistema resolveu automaticamente | Contador |
| Falhas fatais | Falhas que exigiram intervenÃ§Ã£o humana | Contador |

---

## 2. MÃ©tricas por Agente

| Agente | MÃ©tricas EspecÃ­ficas |
|--------|---------------------|
| **A01 â€” TranscriÃ§Ã£o** | PrecisÃ£o da transcriÃ§Ã£o (%), Tempo de transcriÃ§Ã£o (ms), Tamanho do Ã¡udio (KB) |
| **A02 â€” MemÃ³ria** | Entidades identificadas (n), Notas criadas (n), Taxa de acerto de classificaÃ§Ã£o (%) |
| **A03 â€” DocumentaÃ§Ã£o** | Resumos gerados (n), AprovaÃ§Ãµes sem ediÃ§Ã£o (%), Tempo de geraÃ§Ã£o (ms) |
| **A04 â€” ComunicaÃ§Ã£o** | E-mails gerados (n), E-mails enviados (n), Taxa de ediÃ§Ã£o antes de envio (%) |
| **A05 â€” Consulta** | Consultas realizadas (n), Tempo mÃ©dio de resposta (ms), Taxia de aceitaÃ§Ã£o de sugestÃµes (%) |

---

## 3. MÃ©tricas de Custo

| MÃ©trica | FÃ³rmula | FrequÃªncia |
|---------|---------|:----------:|
| Custo por execuÃ§Ã£o | `soma(custo_chamada_llm) + soma(custo_api_externa)` | Por execuÃ§Ã£o |
| Custo por agente | `soma(custo_chamadas_agente)` | Por agente |
| Custo diÃ¡rio | `soma(custo_execucoes_dia)` | DiÃ¡rio |
| Custo mensal | `soma(custo_execucoes_mes)` | Mensal |

---

## 4. MÃ©tricas de Confiabilidade

| MÃ©trica | FÃ³rmula | Alerta em |
|---------|---------|:---------:|
| MTBF (Mean Time Between Failures) | `tempo_total / numero_falhas` | < 1 hora |
| MTTR (Mean Time To Recover) | `tempo_recuperacao_total / falhas_recuperadas` | > 5 min |
| Disponibilidade do agente | `tempo_ok / tempo_total * 100` | < 95% |
| Taxa de rollback | `rollbacks / execucoes * 100` | > 5% |

---

## 5. MÃ©tricas de Observabilidade

| MÃ©trica | DescriÃ§Ã£o | Formato |
|---------|-----------|---------|
| Logs emitidos | Contagem de logs por nÃ­vel | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| Eventos publicados | Eventos no Event Bus (contagem por tipo) | `evento:contagem` |
| Tracing ativo | Spans ativos por execuÃ§Ã£o | Span ID, Parent Span ID |
| Alertas disparados | Alertas acima do limiar | `alerta:nome:valor` |

---

## 6. Formato de EmissÃ£o

MÃ©tricas sÃ£o emitidas em logs estruturados com prefixo `METRICA:`:

```json
{
  "metrica": "tempo_total_ms",
  "valor": 12500,
  "id_execucao": "exec_001",
  "agente": "A01",
  "timestamp": "2026-07-02T10:30:00Z",
  "tags": {"modo": "sandbox", "fluxo": "transcricao"}
}
```

---

## 7. Alertas

| MÃ©trica | Limiar | AÃ§Ã£o |
|---------|:------:|------|
| Tempo total | > 60s | Log WARNING |
| Taxa de erro | > 10% | Log ERROR + notificar |
| Custo por execuÃ§Ã£o | > $0.50 | Bloquear execuÃ§Ã£o + notificar |
| Falhas fatais consecutivas | > 3 | Desabilitar agente + notificar |
| Chamadas LLM por execuÃ§Ã£o | > 5 | Log WARNING |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

