---
tags:
  - api
  - movidesk
  - integracao
  - referencia
---

# API de Tickets — Movidesk

> Documentação de referência completa da API pública de Tickets do Movidesk.
>
> **Base URL:** `https://api.movidesk.com/public/v1`
> **Documentação oficial:** `https://atendimento.movidesk.com/api/v1/docs`
>
> Integração gerenciada pelo componente [[04-Arquitetura/Componentes.md#C08---movidesk-client|C08 — Movidesk Client]].

---

## Autenticação

O token é passado como **query parameter** em todas as requisições:

```
?token=52ee6ca5-8639-422b-bafe-470013c11176
```

**Geração:** Movidesk → Configurações → Conta → Parâmetros → Ambiente → "Gerar nova chave"

> ⚠️ Gerar nova chave invalida a anterior imediatamente.

---

## Rate Limits

| Limite | Consequência |
|--------|-------------|
| 10 requisições/minuto | Limite padrão de taxa |
| 3 requisições com erro | Bloqueio de **60s** (`429 Too Many Failed Requests`) |
| +3 erros após reativação | Bloqueio de **120s** |
| +3 erros após reativação | Bloqueio de **300s** |

O header `retry-after` na resposta informa o tempo restante de bloqueio em segundos.

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/tickets?id={id}` | Obtém um ticket por ID |
| `GET` | `/tickets?protocol={protocol}` | Obtém um ticket por protocolo |
| `GET` | `/tickets?$select=...` | Lista tickets (obrigatório `$select`) |
| `GET` | `/tickets/past?$select=...` | Tickets com `lastUpdate` > 90 dias |
| `GET` | `/tickets/htmldescription?id={id}` | HTML formatado das ações |
| `POST` | `/tickets` | Cria novo ticket |
| `PATCH` | `/tickets?id={id}` | Atualização parcial de ticket |
| `POST` | `/ticketFileUpload?id={id}&actionId={id}` | Upload de anexo (multipart) |

### Parâmetros Comuns

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `token` | string | ✓ | Token de autenticação |
| `id` | int | variável | ID do ticket |
| `protocol` | string | variável | Protocolo do ticket |
| `includeDeletedItems` | bool | opcional | `true` para incluir itens deletados (default: `false`) |
| `returnAllProperties` | bool | opcional | `true` para retornar todas as propriedades no POST (default: `false`) |

> **Atenção:** A API pode levar alguns minutos para replicar tickets novos ou modificados. Eles podem não aparecer em consultas imediatamente.

---

## Schema do Ticket

### Propriedades Principais

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | string | 10 | — | Número do ticket (somente leitura) |
| `protocol` | string | 30 | — | Protocolo do ticket (somente leitura) |
| `type` | int | 1 | ✓ | 1 = Interno, 2 = Público |
| `subject` | string | 350 | — | Assunto do ticket |
| `category` | string | 128 | — | Nome da categoria (deve existir e estar relacionada ao tipo/serviço) |
| `urgency` | string | 128 | — | Nome da urgência (deve existir) |
| `status` | string | 128 | * | Nome do status. Para alterar, `justification` também deve ser informada. Default: "Novo" |
| `baseStatus` | string | 128 | — | `New`, `InAttendance`, `Stopped`, `Canceled`, `Resolved`, `Closed` (somente leitura) |
| `justification` | string | 128 | — | Justificativa (obrigatória quando o status exigir) |
| `origin` | int | 1 | — | Canal de abertura (somente leitura). Ver tabela abaixo |
| `createdDate` | datetime UTC | 7 | * | Data de abertura. Default: data atual. Leitura após criação |
| `originEmailAccount` | string | 128 | — | Conta de e-mail que recebeu o ticket (somente leitura) |
| `owner` | person | — | — | Responsável. Para alterar, `ownerTeam` também deve ser informada |
| `ownerTeam` | string | 128 | — | Equipe do responsável (deve estar associada ao responsável) |
| `createdBy` | person | — | ✓ | Gerador do ticket |
| `serviceFull` | array | 1024 | — | Lista com nomes dos níveis do serviço (somente leitura) |
| `serviceFirstLevelId` | int | 10 | — | ID do serviço selecionado |
| `serviceFirstLevel` | string | 1024 | — | Nome do primeiro nível do serviço |
| `serviceSecondLevel` | string | 1024 | — | Nome do segundo nível do serviço |
| `serviceThirdLevel` | string | 1024 | — | Nome do terceiro nível do serviço |
| `contactForm` | string | 128 | — | Formulário de contato (somente leitura) |
| `tags` | array | — | — | Lista de strings. Tags inexistentes são criadas |
| `cc` | string | 1024 | — | E-mails do Cc separados por vírgula (somente leitura) |
| `resolvedIn` | datetime UTC | — | — | Data que foi resolvido |
| `reopenedIn` | datetime UTC | — | — | Data da última reabertura (somente leitura) |
| `closedIn` | datetime UTC | — | — | Data que foi fechado |
| `lastActionDate` | datetime UTC | — | — | Data da última ação (somente leitura) |
| `actionCount` | int | — | — | Quantidade de ações (somente leitura) |
| `lastUpdate` | datetime UTC | — | — | Data da última alteração (somente leitura) |
| `lifeTimeWorkingTime` | int | — | — | Tempo de vida em minutos em horas úteis (somente leitura) |
| `stoppedTime` | int | — | — | Tempo parado em minutos corridos (somente leitura) |
| `stoppedTimeWorkingTime` | int | — | — | Tempo parado em minutos úteis (somente leitura) |
| `resolvedInFirstCall` | bool | — | — | Resolvido no primeiro atendimento (chat/telefonia) |
| `chatWidget` | string | 128 | — | App de chat (somente leitura) |
| `chatGroup` | string | 128 | — | Grupo de chat (somente leitura) |
| `chatTalkTime` | int | — | — | Duração do chat em segundos (somente leitura) |
| `chatWaitingTime` | int | — | — | Tempo de espera em segundos (somente leitura) |
| `sequence` | int | — | — | Número de sequência |
| `slaAgreement` | string | 128 | — | Contrato SLA (somente leitura) |
| `slaAgreementRule` | string | 128 | — | Regra do SLA (somente leitura) |
| `slaSolutionTime` | int | — | — | Tempo de solução do SLA (somente leitura) |
| `slaResponseTime` | int | — | — | Tempo de resposta do SLA (somente leitura) |
| `slaSolutionChangedByUser` | bool | — | — | SLA alterado manualmente (somente leitura) |
| `slaSolutionChangedBy` | person | — | — | Pessoa que alterou o SLA (somente leitura) |
| `slaSolutionDate` | datetime UTC | — | — | Data de solução do SLA |
| `slaSolutionDateIsPaused` | bool | — | — | SLA pausado (somente leitura) |
| `slaResponseDate` | datetime UTC | — | — | Data de resposta do SLA (somente leitura) |
| `slaRealResponseDate` | datetime UTC | — | — | Data real de resposta do SLA (somente leitura) |
| `jiraIssueKey` | string | 64 | — | Issue do Jira associada (somente leitura) |
| `redmineIssueId` | int | — | — | Issue do Redmine associada (somente leitura) |

### Campos de Origem (`origin`)

| Valor | Descrição |
|-------|-----------|
| 1 | Via web pelo cliente |
| 2 | Via web pelo agente |
| 3 | Recebido via email |
| 4 | Gatilho do sistema |
| 5 | Chat (online) |
| 7 | Email enviado pelo sistema |
| 8 | Formulário de contato |
| 9 | Via web API |
| 10 | Agendamento automático |
| 11 | Jira Issue |
| 12 | Redmine Issue |
| 13 | ReceivedCall |
| 14 | MadeCall |
| 15 | LostCall |
| 16 | DropoutCall |
| 17 | Acesso remoto (descontinuado) |
| 18 | WhatsApp |
| 19 | Movidesk Integration |
| 20 | Zenvia Chat |
| 21 | NotAnsweredCall |
| 22 | Facebook Messenger |
| 23 | WhatsApp Business Movidesk |
| 24 | Altu |
| 25 | WhatsApp Ativo |

---

## Sub-recursos

### Clients — `ticket.clients[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | string | 64 | ✓ | Cod. ref. da empresa/departamento/pessoa (leitura) |
| `businessName` | string | 128 | — | Nome do cliente (leitura) |
| `email` | string | 128 | — | E-mail principal (leitura) |
| `phone` | string | 128 | — | Telefone principal (leitura) |
| `personType` | int | 1 | ✓ | 1=Pessoa, 2=Empresa, 4=Departamento (leitura) |
| `profileType` | int | 1 | ✓ | 1=Agente, 2=Cliente, 3=Ambos (leitura) |
| `isDeleted` | bool | — | — | Se foi deletado (leitura) |
| `organization` | person | — | — | Organização do cliente (leitura) |

### Actions — `ticket.actions[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | int | 10 | * | Número da ação (leitura). *Obrig. para alterar ação existente |
| `type` | int | 1 | ✓ | 1=Interna, 2=Pública |
| `origin` | int | 1 | — | Origem da ação (leitura). Mesmos valores de `origin` do ticket |
| `description` | string | max | ✓ | Descrição. Em escrita: HTML formatado. Em leitura: texto puro |
| `htmlDescription` | string | max | — | Descrição em HTML (leitura). Só retornado na busca por ID |
| `status` | string | 128 | — | Status da ação (leitura) |
| `justification` | string | 128 | — | Justificativa da ação (leitura) |
| `createdDate` | datetime UTC | — | * | Data de criação. Default: data atual |
| `createdBy` | person | — | * | Gerador da ação. *Obrig. se houver apontamentos |
| `isDeleted` | bool | — | — | Se foi deletada (leitura) |
| `timeAppointments` | array | — | — | Apontamentos de hora |
| `expenses` | array | — | — | Despesas |
| `attachments` | array | — | — | Anexos (leitura) |
| `tags` | array | — | — | Tags da ação |

#### TimeAppointments — `ticket.actions[n].timeAppointments[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | int | — | * | Código do apontamento (leitura). *Obrig. para alterar |
| `activity` | string | 128 | ✓ | Atividade cadastrada |
| `date` | datetime | — | ✓ | Data com horas zeradas. Ex: `2016-08-24T00:00:00` |
| `periodStart` | time | — | * | Período inicial. Ex: `08:00:00` |
| `periodEnd` | time | — | * | Período final. Ex: `12:00:00` |
| `workTime` | time | — | * | Tempo total. Ex: `04:00:00` |
| `accountedTime` | decimal | — | — | Tempo contabilizado em decimal (leitura) |
| `workTypeName` | string | — | ✓ | Tipo do horário |
| `createdBy` | person | — | ✓ | Gerador do apontamento |
| `createdByTeam` | team | — | * | Time do gerador |

#### Expenses — `ticket.actions[n].expenses[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | int | 1 | — | Identificador único |
| `type` | string | 128 | ✓ | Tipo de despesa |
| `serviceReport` | string | 128 | — | Nº do relatório de serviço (leitura) |
| `createdBy` | person | 128 | ✓ | Pessoa que apontou |
| `createdByTeam` | team | 128 | — | Equipe da pessoa |
| `date` | datetime UTC | — | ✓ | Data (<= data atual) |
| `quantity` | int | 1 | — | Quantidade (obrigatório se `value` não informado) |
| `value` | decimal | 18,2 | — | Valor monetário (obrigatório se `quantity` não informado) |

#### Attachments — `ticket.actions[n].attachments[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `fileName` | string | 255 | ✓ | Nome do arquivo (leitura) |
| `path` | string | 255 | ✓ | Hash do arquivo (leitura) |
| `createdBy` | person | — | — | Pessoa que enviou (leitura) |
| `createdDate` | datetime UTC | — | — | Data de envio (leitura) |

### Parent / Children Tickets

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | int | — | ✓ | Número do ticket |
| `subject` | string | 128 | — | Assunto (leitura) |
| `isDeleted` | bool | — | — | Se foi deletado (leitura) |

### Owner Histories — `ticket.ownerHistories[n]`

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `ownerTeam` | string | Equipe do responsável (leitura) |
| `owner` | person | Responsável (leitura) |
| `permanencyTimeFullTime` | double | Tempo de permanência em segundos (leitura) |
| `permanencyTimeWorkingTime` | double | Tempo útil de permanência (leitura) |
| `changedBy` | person | Quem alterou (leitura) |
| `changedDate` | datetime UTC | Data da alteração (leitura) |

### Status Histories — `ticket.statusHistories[n]`

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `status` | string | Status (leitura) |
| `justification` | string | Justificativa (leitura) |
| `permanencyTimeFullTime` | double | Tempo no status em segundos (leitura) |
| `permanencyTimeWorkingTime` | double | Tempo útil no status (leitura) |
| `changedBy` | person | Quem alterou (leitura) |
| `changedDate` | datetime UTC | Data da alteração (leitura) |

### Custom Field Values — `ticket.customFieldValues[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `customFieldId` | int | 64 | ✓ | ID do campo adicional |
| `customFieldRuleId` | int | 64 | ✓ | ID da regra de exibição |
| `line` | int | 64 | ✓ | Número da linha. Usar `1` se regra não permitir novas linhas |
| `value` | string | max | * | Valor texto. Obrig. para: texto, numérico, data, hora, email, telefone, URL |
| `items` | array | — | * | Lista de itens. Obrig. para: lista de valores, pessoas, clientes, agentes, seleção |

> Datas em UTC no formato `YYYY-MM-DDThh:MM:ss.000Z`. Hora deve usar data fixa `1991-01-01`. Numérico em formato brasileiro (`1.530,75`).

#### Items — `ticket.customFieldValues.items[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `personId` | int | 64 | * | Para campo tipo "lista de pessoas" |
| `clientId` | int | 64 | * | Para campo tipo "lista de clientes" |
| `team` | string | 128 | * | Para campo tipo "lista de agentes" |
| `customFieldItem` | string | 256 | * | Para campo tipo: lista de valores, seleção múltipla/única |

### Assets — `ticket.assets[n]`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | string | 64 | ✓ | Cod. ref. do ativo (leitura) |
| `name` | string | 128 | ✓ | Nome do ativo (leitura) |
| `label` | string | 128 | — | Etiqueta única (leitura) |
| `serialNumber` | string | 128 | — | Número de série (leitura) |
| `categoryFull` | array | — | — | Níveis da categoria (leitura) |
| `categoryFirstLevel` | string | 128 | — | Categoria nível 1 (leitura) |
| `categorySecondLevel` | string | 128 | — | Categoria nível 2 (leitura) |
| `categoryThirdLevel` | string | 128 | — | Categoria nível 3 (leitura) |
| `isDeleted` | bool | — | — | Se foi deletado do ticket (leitura) |

---

## Person & Team

### Person

Usado em: `owner`, `createdBy`, `clients[].organization`, `actions[].createdBy`, `slaSolutionChangedBy`, etc.

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | string | 64 | ✓ | Cod. ref. (leitura; configurável em `clients[].organization`) |
| `businessName` | string | 128 | — | Nome |
| `email` | string | 128 | — | E-mail |
| `phone` | string | 128 | — | Telefone |
| `personType` | int | 1 | — | 1=Pessoa, 2=Empresa, 4=Departamento (leitura) |
| `profileType` | int | 1 | — | 1=Agente, 2=Cliente, 3=Ambos (leitura) |

### Team

Usado em: `timeAppointments[].createdByTeam`

| Propriedade | Tipo | Tam. | Obrig. | Descrição |
|-------------|------|------|--------|-----------|
| `id` | int | — | ✓ | Cod. ref. do time (leitura) |
| `name` | string | 128 | — | Nome do time (leitura) |

---

## Filtros OData

A API utiliza o protocolo OData para consultas. Palavras-chave suportadas:

| Cláusula | Descrição |
|----------|-----------|
| `$filter` | Expressão avaliada para cada item. Ex: `createdDate gt 2016-09-01T00:00:00.00z` |
| `$orderby` | Ordenação: `asc` ou `desc`. Ex: `id desc` |
| `$top` | Número de itens. Ex: `$top=100` |
| `$skip` | Itens para pular (paginação). Ex: `$skip=100` |
| `$select` | Propriedades a retornar. Ex: `$select=id,subject,status` |
| `$expand` | Expandir coleções filhas. Ex: `$expand=owner,actions($select=origin,id)` |

> `$count` **não** está disponível.

### Operadores de Filtro

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `gt` | Maior que | `createdDate gt 2016-09-01T00:00:00.00z` |
| `ge` | Maior ou igual | `createdDate ge 2016-10-10T00:00:00.00z` |
| `lt` | Menor que | — |
| `le` | Menor ou igual | `createdDate le 2016-10-17T00:00:00.00z` |
| `eq` | Igual | `status eq 'Resolved'` |
| `and` | E | `createdDate ge ... and createdDate le ...` |
| `any` | Em coleções | `clients/any(client: client/id eq '1')` |

---

## Exemplos Completos

### GET — Ticket por ID

```
GET https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&id=1
```

```json
{
  "id": 1,
  "protocol": "MOVI202109000001",
  "type": 2,
  "origin": 0,
  "status": "Novo",
  ...
}
```

### GET — Ticket por Protocolo

```
GET https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&protocol=MOVI202109000001
```

### GET — Lista com Filtros e Paginação

```
GET https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&$select=id,subject,createdDate&$filter=createdDate gt 2016-09-01T00:00:00.00z&$orderby=id desc&$top=100&$skip=100
```

### GET — Expansão de Sub-recursos

```
GET https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&$select=id,subject,createdDate&$filter=createdDate ge 2016-10-10T00:00:00.00z and createdDate le 2016-10-17T00:00:00.00z&$expand=owner,actions($select=origin,id),actions($expand=timeAppointments($expand=createdBy))
```

### GET — Filtro por Cliente

```
GET https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&$filter=clients/any(client: client/id eq '1')&$select=id&$expand=clients
```

### GET — HTML das Ações

```
GET https://api.movidesk.com/public/v1/tickets/htmldescription?token=MEU_TOKEN&id=1&actionId=1
```

```json
{
  "id": 1,
  "description": "<h1>title</h1></br><p>some text from action</p>"
}
```

### POST — Criar Ticket

```
POST https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&returnAllProperties=false
Content-Type: application/json
```

```json
{
  "type": 2,
  "subject": "Assunto do chamado",
  "category": "Categoria",
  "urgency": "Urgência",
  "status": "Status",
  "justification": "Justificativa",
  "createdDate": "2016-11-18T14:25:07.1920886",
  "clients": [
    {
      "id": "CodRefDoCliente"
    }
  ],
  "actions": [
    {
      "type": 2,
      "description": "<p>Descrição da ação em HTML</p>"
    }
  ]
}
```

**Retorno:** Status `200` + `{ "id": 123 }`

### PATCH — Atualizar Ticket (Parcial)

```
PATCH https://api.movidesk.com/public/v1/tickets?token=MEU_TOKEN&id=1
Content-Type: application/json
```

```json
{
  "subject": "Novo assunto"
}
```

> **Importante:** Listas (`actions[]`, `tags[]`, `clients[]`) sempre **substituem** todo o conteúdo. Itens não informados são removidos. Para alterar uma ação já existente, o `id` da ação deve ser informado.

### POST — Upload de Anexo

```
POST https://api.movidesk.com/public/v1/ticketFileUpload?token=MEU_TOKEN&id=1452&actionId=1
Content-Type: multipart/form-data
```

**Body:** Arquivo binário (multipart form-data)

**Retorno:** Status `200` + detalhes dos arquivos inseridos (nome, hash, possíveis erros).

---

## Tratamento de Erros

| Código | Significado | Ação |
|--------|-------------|------|
| 200 | Sucesso | Processar retorno |
| 401 | Token inválido | Notificar usuário |
| 429 | Too Many Failed Requests | Ler `retry-after`, aguardar e tentar novamente |
| 5xx | Erro interno do servidor | Retry 3x com backoff exponencial |

### Estratégia de Retry (C08)

```python
# Comportamento esperado do Movidesk Client:
- Timeout por requisição: 15s
- Máximo de retries: 3
- Backoff: exponencial (1s, 2s, 4s)
- Em 429: ler header retry-after e aguardar o tempo informado
- Se exceder retries: registrar em fila de sincronização offline
```

---

## Mapeamento para o Hermes (C08)

| Operação do Sistema | Endpoint | Frequência | Uso |
|---------------------|----------|------------|-----|
| Buscar chamado por ID do Hermes | `GET /tickets?id={id}` | Sob demanda | Identificar chamado a ser processado |
| Buscar chamados abertos do cliente | `GET /tickets?$select=...&$filter=clients/any(...)` | Periódico | Listar chamados pendentes do cliente |
| Buscar chamados recentes (cache) | `GET /tickets?$select=...&$filter=lastUpdate gt ...` | A cada 5 min | Sincronizar chamados atualizados |
| Buscar chamados antigos | `GET /tickets/past?$select=...` | Sob demanda | Histórico completo |
| Criar chamado técnico | `POST /tickets` | Sob demanda | Abrir chamado interno para análise |
| Atualizar status/resposta | `PATCH /tickets?id={id}` | Sob demanda | Mover fluxo do chamado |
| Anexar evidência | `POST /ticketFileUpload` | Sob demanda | Fotos, logs, prints |
| Obter descrição formatada | `GET /tickets/htmldescription` | Sob demanda | Renderizar ação em HTML |

> Ver [[04-Arquitetura/Componentes.md#C08---movidesk-client|C08 — Movidesk Client]] para a implementação da interface `IMovidesk`.
