---
title: "Criterios de Aceitacao"
description: "Criterios por tipo de teste, agente e funcionalidade MVP"
status: "novo"
---

# CritÃ©rios de AceitaÃ§Ã£o

> **CritÃ©rios objetivos que determinam se um loop passou ou falhou em cada nÃ­vel de teste.**

---

## 1. CritÃ©rios por Tipo de Teste

### 1.1 â€” UnitÃ¡rios

| CritÃ©rio | Aprovado se |
|----------|-------------|
| FunÃ§Ãµes puras | Retorno igual ao esperado para todas as entradas no boundary test |
| ValidaÃ§Ã£o de schema | Schema rejeita entradas invÃ¡lidas e aceita vÃ¡lidas |
| Parsing de LLM | Resposta malformada Ã© detectada e tratada |
| FormataÃ§Ã£o | SaÃ­da segue o formato esperado |

### 1.2 â€” Fluxo

| CritÃ©rio | Aprovado se |
|----------|-------------|
| Etapas completas | Cada etapa executa e produz saÃ­da esperada |
| Fluxo alternativo | Caminhos de erro executam corretamente |
| Encadeamento | SaÃ­da de uma etapa Ã© entrada vÃ¡lida da prÃ³xima |

### 1.3 â€” IntegraÃ§Ã£o

| CritÃ©rio | Aprovado se |
|----------|-------------|
| Agente â†’ Agente | Mensagem transmitida e interpretada corretamente |
| CLI â†’ Daemon | Comando enviado e resposta recebida via Named Pipe |
| Daemon â†’ ServiÃ§o | Chamada ao serviÃ§o externo (mock) executada |

### 1.4 â€” RecuperaÃ§Ã£o

| CritÃ©rio | Aprovado se |
|----------|-------------|
| Retry | ApÃ³s falha temporÃ¡ria, sistema recupera e continua |
| Checkpoint | ApÃ³s falha fatal, checkpoint permite restaurar estado |
| NotificaÃ§Ã£o | UsuÃ¡rio Ã© notificado em casos que exigem intervenÃ§Ã£o |

### 1.5 â€” SeguranÃ§a

| CritÃ©rio | Aprovado se |
|----------|-------------|
| AprovaÃ§Ã£o | Nenhuma aÃ§Ã£o externa executada sem aprovaÃ§Ã£o |
| PermissÃ£o | AÃ§Ã£o sem permissÃ£o Ã© bloqueada com erro claro |
| Log | Toda aÃ§Ã£o (inclusive bloqueada) Ã© registrada |

### 1.6 â€” Performance

| CritÃ©rio | Aprovado se |
|----------|-------------|
| Tempo total | Loop completo em < 30s (sandbox) |
| Chamadas LLM | <= 5 por execuÃ§Ã£o |
| MemÃ³ria | < 100 MB adicional por execuÃ§Ã£o |

### 1.7 â€” Observabilidade

| CritÃ©rio | Aprovado se |
|----------|-------------|
| Logs | Todos os eventos esperados foram logados |
| Correlation ID | Mesmo ID propagado por toda a cadeia |
| MÃ©tricas | MÃ©tricas obrigatÃ³rias emitidas |

---

## 2. CritÃ©rios por Agente

| Agente | CritÃ©rios |
|--------|-----------|
| **A01 â€” TranscriÃ§Ã£o** | Ãudio â†’ Whisper â†’ texto â†’ LLM â†’ resumo estruturado. Tempo < 30s |
| **A02 â€” MemÃ³ria** | AnÃ¡lise de entidades â†’ classificaÃ§Ã£o â†’ notas criadas com links. PrecisÃ£o > 80% |
| **A03 â€” DocumentaÃ§Ã£o** | TranscriÃ§Ã£o â†’ resumo OS â†’ formataÃ§Ã£o â†’ prÃ©via para aprovaÃ§Ã£o |
| **A04 â€” ComunicaÃ§Ã£o** | Template + dados â†’ e-mail gerado â†’ formataÃ§Ã£o correta |
| **A05 â€” Consulta** | Pergunta â†’ busca Qdrant â†’ contexto â†’ LLM â†’ resposta. Tempo < 15s |

---

## 3. CritÃ©rios por Funcionalidade MVP

| Funcionalidade | CritÃ©rio de AceitaÃ§Ã£o |
|----------------|----------------------|
| 1 â€” Acompanhamento | CLI `iniciar` â†’ sessÃ£o ativa â†’ CLI `finalizar` â†’ sessÃ£o encerrada |
| 2 â€” GravaÃ§Ã£o | `gravar` com confirmaÃ§Ã£o â†’ indicador visual â†’ `parar` â†’ arquivo salvo |
| 3 â€” TranscriÃ§Ã£o | Ãudio transcrito â†’ texto exibido na CLI |
| 4 â€” Resumo IA | `resumir` â†’ resumo estruturado â†’ aprovaÃ§Ã£o/ediÃ§Ã£o possÃ­vel |
| 5 â€” Notas Obsidian | Notas criadas com template â†’ links entre notas |
| 6 â€” Consulta | `buscar` â†’ resultados por similaridade â†’ exibidos |
| 7 â€” SugestÃ£o | Durante sessÃ£o â†’ sugestÃµes exibidas â†’ aceitar/rejeitar |
| 8 â€” Fechamento OS | Resumo gerado â†’ aprovado â†’ Movidesk atualizado |
| 9 â€” E-mail | Minuta gerada â†’ editÃ¡vel â†’ enviada |
| 10 â€” SeguranÃ§a | AÃ§Ã£o crÃ­tica negada sem aprovaÃ§Ã£o â†’ log registrado |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

