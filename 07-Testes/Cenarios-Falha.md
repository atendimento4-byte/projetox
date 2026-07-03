---
title: "Cenarios de Falha"
description: "13 cenarios de falha com causa, deteccao e recuperacao"
status: "novo"
---

# CenÃ¡rios de Falha

> **Cada cenÃ¡rio de falha possÃ­vel em loops de agente, orquestraÃ§Ã£o e fluxo, com causa, detecÃ§Ã£o e recuperaÃ§Ã£o.**

---

## 1. Falha do LLM

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | API do LLM retorna erro 5xx, timeout ou resposta malformada |
| **Sintoma** | Agente nÃ£o consegue gerar saÃ­da, resposta nÃ£o segue schema |
| **DetecÃ§Ã£o** | ValidaÃ§Ã£o de schema falha, timeout expira, HTTP error |
| **RecuperaÃ§Ã£o** | Retry com backoff exponencial (3x). ApÃ³s 3 falhas, notificar usuÃ¡rio |
| **Log** | `erro_llm.json` com prompt, resposta parcial, tentativas |
| **Impacto** | Loop pausa atÃ© resoluÃ§Ã£o manual |

---

## 2. Timeout

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | ServiÃ§o externo nÃ£o responde dentro do limite configurado |
| **Sintoma** | Agente aguarda resposta indefinidamente |
| **DetecÃ§Ã£o** | Timer do agente expira |
| **RecuperaÃ§Ã£o** | Cancelar requisiÃ§Ã£o, registrar timeout, tentar via mock em modo degradado |
| **Log** | `timeout.json` com serviÃ§o, tempo limite, tentativas |
| **Impacto** | Funcionalidade afetada fica indisponÃ­vel atÃ© retry |

---

## 3. Ferramenta IndisponÃ­vel

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Whisper local nÃ£o instalado, Qdrant off, Redis off |
| **Sintoma** | Agente tenta usar ferramenta e falha |
| **DetecÃ§Ã£o** | Erro de conexÃ£o, comando nÃ£o encontrado |
| **RecuperaÃ§Ã£o** | Verificar status da ferramenta, tentar fallback (ex: API no lugar de local) |
| **Log** | `ferramenta_indisponivel.json` |
| **Impacto** | Funcionalidade parcial atÃ© restauraÃ§Ã£o |

---

## 4. API IndisponÃ­vel (Movidesk)

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Servidor Movidesk fora do ar, rede indisponÃ­vel |
| **Sintoma** | Chamadas Ã  API falham |
| **DetecÃ§Ã£o** | HTTP 503, timeout de conexÃ£o |
| **RecuperaÃ§Ã£o** | Enfileirar aÃ§Ã£o pendente, notificar usuÃ¡rio, retry automÃ¡tico apÃ³s 5min |
| **Log** | `api_indisponivel.json` com aÃ§Ã£o pendente enfileirada |
| **Impacto** | Fechamento de OS e consultas bloqueados atÃ© recuperaÃ§Ã£o |

---

## 5. Erro de AutenticaÃ§Ã£o

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Token Movidesk expirado, chave LLM invÃ¡lida |
| **Sintoma** | ServiÃ§o retorna HTTP 401/403 |
| **DetecÃ§Ã£o** | Resposta de erro de autenticaÃ§Ã£o |
| **RecuperaÃ§Ã£o** | Notificar usuÃ¡rio, tentar renovar token (se aplicÃ¡vel), pausar execuÃ§Ã£o |
| **Log** | `erro_autenticacao.json` com serviÃ§o e hint de resoluÃ§Ã£o |
| **Impacto** | ServiÃ§o afetado bloqueado atÃ© nova autenticaÃ§Ã£o |

---

## 6. Arquivo Inexistente

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Ãudio para transcriÃ§Ã£o nÃ£o encontrado, nota do Obsidian nÃ£o existe |
| **Sintoma** | Erro de leitura |
| **DetecÃ§Ã£o** | FileNotFoundError ou similar |
| **RecuperaÃ§Ã£o** | Verificar caminho, listar alternativas, notificar usuÃ¡rio |
| **Log** | `arquivo_inexistente.json` com caminho e contexto |

---

## 7. Contexto InvÃ¡lido

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Estado da sessÃ£o inconsistente, dados corrompidos |
| **Sintoma** | Agente age sobre dados que nÃ£o fazem sentido |
| **DetecÃ§Ã£o** | ValidaÃ§Ã£o de consistÃªncia do contexto falha |
| **RecuperaÃ§Ã£o** | Resetar contexto para Ãºltimo checkpoint vÃ¡lido, logar inconsistÃªncia |
| **Log** | `contexto_invalido.json` com dump do estado corrompido |

---

## 8. Resposta Inconsistente do LLM

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | LLM gera resposta fora do schema, com campos faltantes ou valores absurdos |
| **Sintoma** | Parsing de resposta falha, valores nÃ£o passam em validaÃ§Ã£o |
| **DetecÃ§Ã£o** | ValidaÃ§Ã£o de schema (Pydantic), range checks |
| **RecuperaÃ§Ã£o** | Re-prompt com instruÃ§Ã£o mais explÃ­cita. ApÃ³s 3 falhas, abortar e notificar |
| **Log** | `resposta_inconsistente.json` com prompt, resposta, erros de validaÃ§Ã£o |

---

## 9. InterrupÃ§Ã£o do UsuÃ¡rio

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | UsuÃ¡rio pressiona Ctrl+C, comando `cancelar`, fecha terminal |
| **Sintoma** | Loop interrompido abruptamente |
| **DetecÃ§Ã£o** | Signal handler, flag de cancelamento |
| **RecuperaÃ§Ã£o** | Finalizar operaÃ§Ã£o atual, salvar checkpoint, notificar usuÃ¡rio do estado |
| **Log** | `interrupcao_usuario.json` com ponto de interrupÃ§Ã£o e estado salvo |

---

## 10. Loop Infinito

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Agente repete mesma aÃ§Ã£o sem progresso, ciclo sem condiÃ§Ã£o de saÃ­da |
| **Sintoma** | Mesma ferramenta chamada repetidamente, mesmo resultado |
| **DetecÃ§Ã£o** | Detector de repetiÃ§Ã£o (mesma aÃ§Ã£o > 3x), limite de iteraÃ§Ãµes excedido |
| **RecuperaÃ§Ã£o** | ForÃ§ar parada, logar loop detectado, notificar usuÃ¡rio |
| **Log** | `loop_infinito.json` com histÃ³rico de aÃ§Ãµes e ponto de repetiÃ§Ã£o |

---

## 11. DependÃªncia Circular

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Agente A chama agente B que chama agente A |
| **Sintoma** | ExecuÃ§Ã£o never termina, pilha de chamadas cresce |
| **DetecÃ§Ã£o** | Rastro de agentes visitados, detecÃ§Ã£o de ciclo |
| **RecuperaÃ§Ã£o** | Abortar execuÃ§Ã£o, logar ciclo detectado |
| **Log** | `dependencia_circular.json` com grafo de chamadas |

---

## 12. MemÃ³ria Corrompida

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | Arquivo do Obsidian com frontmatter invÃ¡lido, banco com dados inconsistentes |
| **Sintoma** | Agente lÃª dados e nÃ£o consegue interpretar |
| **DetecÃ§Ã£o** | Parsing de frontmatter falha, validaÃ§Ã£o de schema |
| **RecuperaÃ§Ã£o** | Isolar registro corrompido, notificar usuÃ¡rio, tentar recovery automÃ¡tico |
| **Log** | `memoria_corrompida.json` com caminho do arquivo e erro |

---

## 13. Cancelamento da ExecuÃ§Ã£o

| Atributo | DescriÃ§Ã£o |
|----------|-----------|
| **Causa** | UsuÃ¡rio ou processo externo solicita cancelamento |
| **Sintoma** | Loop em execuÃ§Ã£o recebe sinal de parada |
| **DetecÃ§Ã£o** | Sinal recebido via IPC ou comando CLI |
| **RecuperaÃ§Ã£o** | Parar operaÃ§Ã£o atual, reverter aÃ§Ãµes nÃ£o confirmadas, salvar checkpoint |
| **Log** | `execucao_cancelada.json` com motivo e estado |

---

## 14. Resumo por Tipo

| Tipo de Falha | FrequÃªncia Esperada | Gravidade | RecuperaÃ§Ã£o AutomÃ¡tica |
|:-------------:|:-------------------:|:---------:|:---------------------:|
| LLM erro | Baixa | Alta | Parcial (3 retries) |
| Timeout | MÃ©dia | MÃ©dia | Parcial |
| Ferramenta off | Baixa | Alta | NÃ£o |
| API off | MÃ©dia | Alta | Parcial (fila) |
| AutenticaÃ§Ã£o | Baixa | Alta | NÃ£o |
| Arquivo inexistente | Baixa | MÃ©dia | NÃ£o |
| Contexto invÃ¡lido | Muito baixa | CrÃ­tica | Parcial (checkpoint) |
| Resposta inconsistente | MÃ©dia | MÃ©dia | Sim (re-prompt) |
| InterrupÃ§Ã£o usuÃ¡rio | MÃ©dia | Baixa | Sim (checkpoint) |
| Loop infinito | Baixa | CrÃ­tica | Sim (detector) |
| DependÃªncia circular | Muito baixa | CrÃ­tica | Sim (detector) |
| MemÃ³ria corrompida | Baixa | Alta | NÃ£o |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

