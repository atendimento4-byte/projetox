---
title: "Limites de Execucao"
description: "Limites por loop, ambiente e globais do sistema"
status: "novo"
---

# Limites de ExecuÃ§Ã£o

> **Limites obrigatÃ³rios para todo loop do sistema: quando parar, o que monitorar e o que fazer ao atingir o limite.**

---

## 1. Filosofia

Todo loop DEVE ter limites definidos antes de executar. Limites protegem contra:
- Loops infinitos (bugs)
- Custo excessivo de LLM
- Consumo excessivo de memÃ³ria
- DegradaÃ§Ã£o da experiÃªncia do usuÃ¡rio
- ExaustÃ£o de recursos do sistema

---

## 2. Limites por Loop

### 2.1 â€” Loop de Agente

| Limite | Valor PadrÃ£o | Unidade | Ocorre |
|--------|:------------:|:-------:|--------|
| IteraÃ§Ãµes mÃ¡ximas | 10 | iteraÃ§Ãµes | Agente repete sem progresso |
| Tempo mÃ¡ximo | 60 | segundos | Desde o inÃ­cio atÃ© o fim |
| Chamadas LLM | 5 | chamadas | Por execuÃ§Ã£o do agente |
| Ferramentas usadas | 8 | ferramentas | Por execuÃ§Ã£o do agente |
| Custo mÃ¡ximo | 0.50 | USD | Por execuÃ§Ã£o do agente |
| Tokens de entrada | 8000 | tokens | Soma de prompt + contexto |
| Tokens de saÃ­da | 2000 | tokens | Soma de respostas |

### 2.2 â€” Loop de OrquestraÃ§Ã£o (Hermes)

| Limite | Valor PadrÃ£o | Unidade | Ocorre |
|--------|:------------:|:-------:|--------|
| Agentes acionados | 5 | agentes | Por comando do usuÃ¡rio |
| Tempo mÃ¡ximo | 120 | segundos | Desde o comando atÃ© o resultado |
| AÃ§Ãµes pendentes | 10 | aÃ§Ãµes | Na fila de aprovaÃ§Ã£o |
| Etapas do fluxo | 20 | etapas | Por fluxo completo |

### 2.3 â€” Loop de Fluxo (Processo)

| Limite | Valor PadrÃ£o | Unidade | Ocorre |
|--------|:------------:|:-------:|--------|
| Etapas no fluxo | 15 | etapas | Fluxo Macro |
| Retries por etapa | 3 | tentativas | Por etapa com falha |
| Tempo por etapa | 30 | segundos | Desde o inÃ­cio da etapa |

---

## 3. AÃ§Ã£o ao Atingir Limite

| Limite | AÃ§Ã£o |
|--------|------|
| IteraÃ§Ãµes mÃ¡ximas | Abortar loop, logar "loop infinito detectado", notificar usuÃ¡rio |
| Tempo mÃ¡ximo | Abortar loop, logar timeout, notificar usuÃ¡rio |
| Chamadas LLM | Bloquear novas chamadas, usar fallback ou abortar |
| Custo mÃ¡ximo | Abortar loop, notificar usuÃ¡rio |
| Tokens mÃ¡ximos | Truncar contexto mais antigo, logar aviso |
| Retries mÃ¡ximos | Pular etapa, marcar como falha, continuar fluxo |

---

## 4. Limites por Ambiente

| Ambiente | IteraÃ§Ãµes | Tempo | Chamadas LLM | Custo |
|----------|:---------:|:-----:|:------------:|:-----:|
| Dry Run | 1 | 1s | 0 | $0 |
| Sandbox | 5 | 30s | 3 | $0 (mock) |
| SimulaÃ§Ã£o | 10 | 60s | 5 | $0.10 |
| ProduÃ§Ã£o | 10 | 120s | 5 | $0.50 |

---

## 5. Limites Globais do Sistema

| Recurso | Limite | Monitoramento |
|---------|:------:|--------------|
| MemÃ³ria do daemon | 512 MB | PSUtil a cada 10s |
| Loops simultÃ¢neos | 3 | Contador de execuÃ§Ãµes ativas |
| RequisiÃ§Ãµes IPC/min | 60 | Rate limiter no Named Pipe |
| Tamanho do contexto | 100 KB | Por sessÃ£o ativa |
| Arquivos de Ã¡udio | 500 MB | Por sessÃ£o |

---

## 6. ConfiguraÃ§Ã£o

Limites podem ser sobrescritos via config.yaml:

```yaml
execucao:
  limites:
    iteracoes_maximas: 10
    tempo_maximo_segundos: 60
    chamadas_llm_maximas: 5
    custo_maximo_usd: 0.50
  ambiente:
    modo: producao  # dry-run | sandbox | simulacao | producao
```

> Ver [[04-Arquitetura/Configuracao.md|Sistema de ConfiguraÃ§Ã£o]].

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

