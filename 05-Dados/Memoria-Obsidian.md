---
title: "Memoria (Obsidian)"
description: "Estrutura de pastas, 5 tipos de nota, templates YAML"
status: "concluido"
---

# MemÃ³ria (Obsidian)

> **Estrutura do vault do Obsidian como memÃ³ria persistente do sistema.**
> Este documento define a organizaÃ§Ã£o de pastas, tipos de nota, frontmatter, convenÃ§Ãµes de nomenclatura e regras de linking.

---

## Filosofia

O Obsidian Ã© a **memÃ³ria de longo prazo** do sistema. Toda informaÃ§Ã£o relevante aprendida durante os atendimentos deve ser registrada aqui de forma:
- **Organizada:** pastas e tipos de nota predefinidos
- **Linkada:** notas conectadas formando um grafo de conhecimento
- **PesquisÃ¡vel:** conteÃºdo em Markdown + metadados em frontmatter
- **Evolutiva:** notas sÃ£o atualizadas conforme novos atendimentos ocorrem

---

## 1. Estrutura de Pastas

```
ðŸ“ ProjetoX/
â”œâ”€â”€ ðŸ“ 00-Index/
â”‚   â””â”€â”€ SDD-Index.md
â”œâ”€â”€ ðŸ“ Atendimentos/
â”‚   â””â”€â”€ ðŸ“ 2026/
â”‚       â””â”€â”€ Atendimento - 2026-07-02 - Empresa ABC - Troca de Roteador.md
â”œâ”€â”€ ðŸ“ Clientes/
â”‚   â”œâ”€â”€ Empresa ABC.md
â”‚   â””â”€â”€ JoÃ£o Silva (PF).md
â”œâ”€â”€ ðŸ“ Equipamentos/
â”‚   â”œâ”€â”€ ðŸ“ Roteadores/
â”‚   â”‚   â””â”€â”€ MikroTik RB951Ui-2HnD.md
â”‚   â”œâ”€â”€ ðŸ“ Servidores/
â”‚   â”‚   â””â”€â”€ Dell PowerEdge R740.md
â”‚   â””â”€â”€ ðŸ“ Switches/
â”‚       â””â”€â”€ Cisco Catalyst 2960.md
â”œâ”€â”€ ðŸ“ Procedimentos/
â”‚   â”œâ”€â”€ InstalaÃ§Ã£o de Roteador MikroTik.md
â”‚   â””â”€â”€ ConfiguraÃ§Ã£o de VLAN Cisco.md
â”œâ”€â”€ ðŸ“ Solucoes/
â”‚   â”œâ”€â”€ Problema - Queda de Link - Substituir Cabo.md
â”‚   â””â”€â”€ Problema - Senha Perdida - Reset de FÃ¡brica.md
â”œâ”€â”€ ðŸ“ Documentacao-Tecnica/
â”‚   â”œâ”€â”€ Manual MikroTik RB951.md
â”‚   â””â”€â”€ Guia RÃ¡pido - Cisco CLI.md
â”œâ”€â”€ ðŸ“ Modelos/
â”‚   â”œâ”€â”€ Modelo - Nota de Cliente.md
â”‚   â”œâ”€â”€ Modelo - Nota de Equipamento.md
â”‚   â””â”€â”€ Modelo - Nota de Atendimento.md
â”œâ”€â”€ ðŸ“ .sistema/
â”‚   â””â”€â”€ (arquivos de controle do sistema, nÃ£o editar manualmente)
â”œâ”€â”€ init.md
```

---

## 2. Tipos de Nota

### 2.1 â€” Nota de Atendimento

**LocalizaÃ§Ã£o:** `Atendimentos/{Ano}/Atendimento - {Data} - {Cliente} - {Resumo}.md`

**Frontmatter:**
```yaml
---
tipo: atendimento
cliente: "[[Empresa ABC]]"
data: 2026-07-02
chamado: "12345"
status: Resolvido
tecnico: "Carlos (TÃ©cnico Parceiro)"
equipamentos:
  - "[[MikroTik RB951Ui-2HnD]]"
solucao: "[[Problema - Queda de Link - Substituir Cabo]]"
tags:
  - atendimento
  - instalacao
---
```

**ConteÃºdo:**
```markdown
# Atendimento - 2026-07-02 - Empresa ABC - Troca de Roteador

**Cliente:** [[Empresa ABC]]
**Data:** 2026-07-02
**Chamado:** 12345
**Status:** Resolvido

## Resumo
SubstituiÃ§Ã£o de roteador MikroTik com falha de hardware.

## Problema
Cliente relatava quedas frequentes de link a cada 30 minutos.

## SoluÃ§Ã£o
[[Problema - Queda de Link - Substituir Cabo]] aplicada.
SubstituÃ­do [[MikroTik RB951Ui-2HnD]] por novo.

## ConfiguraÃ§Ãµes Realizadas
- IP WAN: 200.x.x.x
- IP LAN: 192.168.1.1/24
- DHCP habilitado (range 192.168.1.100-200)
- DNS: 8.8.8.8, 8.8.4.4
- Firewall: regras bÃ¡sicas habilitadas

## Equipamentos Envolvidos
- [[MikroTik RB951Ui-2HnD]] (substituÃ­do)
- [[MikroTik RB951Ui-2HnD]] (novo)

## ObservaÃ§Ãµes
- Cliente optou por manter mesmo modelo
- Agendado retorno em 30 dias para verificaÃ§Ã£o
```

### 2.2 â€” Nota de Cliente

**LocalizaÃ§Ã£o:** `Clientes/{Nome}.md`

**Frontmatter:**
```yaml
---
tipo: cliente
empresa: "Empresa ABC"
cnpj: "12.345.678/0001-90"
contato: "(11) 99999-8888"
email: "contato@empresaabc.com.br"
endereco: "Rua Exemplo, 123 - SÃ£o Paulo/SP"
ultimo_atendimento: 2026-07-02
tags:
  - cliente
  - empresa
  - sao-paulo
---
```

**ConteÃºdo:**
```markdown
# Empresa ABC

**CNPJ:** 12.345.678/0001-90
**Contato:** (11) 99999-8888
**E-mail:** contato@empresaabc.com.br
**EndereÃ§o:** Rua Exemplo, 123 - SÃ£o Paulo/SP

## Equipamentos
- [[MikroTik RB951Ui-2HnD]]
- [[Cisco Catalyst 2960]]

## HistÃ³rico de Atendimentos
1. [[Atendimento - 2026-07-02 - Empresa ABC - Troca de Roteador]] â€” Resolvido
2. [[Atendimento - 2026-05-15 - Empresa ABC - ConfiguraÃ§Ã£o VLAN]] â€” Resolvido

## ObservaÃ§Ãµes
- Contato principal: Maria (financeiro)
- TÃ©cnico de confianÃ§a: Carlos
- Exige documento assinado para todos os serviÃ§os
```

### 2.3 â€” Nota de Equipamento

**LocalizaÃ§Ã£o:** `Equipamentos/{Tipo}/{Modelo}.md`

**Frontmatter:**
```yaml
---
tipo: equipamento
categoria: Roteador
marca: MikroTik
modelo: RB951Ui-2HnD
fabricante: "MikroTik"
tags:
  - equipamento
  - roteador
  - mikrotik
---
```

**ConteÃºdo:**
```markdown
# MikroTik RB951Ui-2HnD

**Tipo:** Roteador
**Marca:** MikroTik
**Modelo:** RB951Ui-2HnD

## EspecificaÃ§Ãµes
- CPU: Atheros AR9344 600MHz
- RAM: 128MB
- Portas: 5x Gigabit Ethernet
- Wireless: 2.4GHz 802.11b/g/n
- PoE: Sim (porta 1)

## ConfiguraÃ§Ã£o PadrÃ£o
- IP padrÃ£o: 192.168.88.1
- UsuÃ¡rio: admin
- Senha: (definir na instalaÃ§Ã£o)

## Problemas Conhecidos
- Superaquecimento em ambientes sem ventilaÃ§Ã£o
- Queda de link apÃ³s atualizaÃ§Ã£o de firmware v6.48

## Procedimentos Relacionados
- [[InstalaÃ§Ã£o de Roteador MikroTik]]

## Atendimentos com este Equipamento
- [[Atendimento - 2026-07-02 - Empresa ABC - Troca de Roteador]]
- [[Atendimento - 2026-04-10 - Empresa XYZ - InstalaÃ§Ã£o MikroTik]]

## DocumentaÃ§Ã£o TÃ©cnica
- [[Manual MikroTik RB951]]
```

### 2.4 â€” Nota de Procedimento

**LocalizaÃ§Ã£o:** `Procedimentos/{Nome}.md`

**Frontmatter:**
```yaml
---
tipo: procedimento
categoria: InstalaÃ§Ã£o
equipamento: "[[MikroTik RB951Ui-2HnD]]"
tempo_estimado: 45min
dificuldade: FÃ¡cil
tags:
  - procedimento
  - instalacao
  - mikrotik
---
```

**ConteÃºdo:**
```markdown
# InstalaÃ§Ã£o de Roteador MikroTik

**Equipamento:** [[MikroTik RB951Ui-2HnD]]
**Tempo estimado:** 45 minutos
**Dificuldade:** FÃ¡cil

## PrÃ©-requisitos
- Roteador MikroTik novo
- Cabo de rede CAT5e ou superior
- Acesso Ã  internet para testes
- Conhecimento bÃ¡sico de redes

## Passos

### 1. PreparaÃ§Ã£o
- Verificar conteÃºdo da caixa (roteador, fonte, manual)
- Identificar local de instalaÃ§Ã£o (ventilado, longe de umidade)

### 2. ConexÃ£o FÃ­sica
- Conectar fonte de alimentaÃ§Ã£o
- Conectar cabo WAN na porta 1 (ether1)
- Conectar cabo LAN na porta 2 (ether2)

### 3. ConfiguraÃ§Ã£o Inicial
- Acessar 192.168.88.1 no navegador
- UsuÃ¡rio: admin, senha: (em branco)
- Alterar senha do administrador
- Configurar WAN via DHCP ou IP fixo
- Configurar LAN (IP, DHCP, DNS)

### 4. ValidaÃ§Ã£o
- Testar conectividade com a internet
- Verificar DHCP funcionando
- Testar wireless

## Problemas Comuns
- "NÃ£o consigo acessar 192.168.88.1" â†’ Reset de fÃ¡brica (segurar botÃ£o reset por 10s)

## Ver tambÃ©m
- [[Manual MikroTik RB951]]
```

### 2.5 â€” Nota de SoluÃ§Ã£o

**LocalizaÃ§Ã£o:** `Solucoes/{Problema} - {Solucao}.md`

**Frontmatter:**
```yaml
---
tipo: solucao
problema: "Queda de link recorrente"
causa: "Cabo de rede danificado"
solucao: "Substituir cabo por novo"
equipamento: "[[MikroTik RB951Ui-2HnD]]"
frequencia: Alta
tags:
  - solucao
  - rede
  - cabo
---
```

**ConteÃºdo:**
```markdown
# Problema - Queda de Link - Substituir Cabo

**Problema:** Queda de link recorrente a cada 30-60 minutos
**Causa provÃ¡vel:** Cabo de rede danificado (curto, mal contato, kink)
**SoluÃ§Ã£o:** Substituir cabo de rede

## Sintomas
- Link cai e restaura ciclicamente
- Log do equipamento mostra "link down/up"
- Teste de cabo (cable test) aponta falha

## Procedimento
1. Identificar qual cabo estÃ¡ com problema (teste fÃ­sico)
2. Substituir por cabo novo CAT5e ou CAT6
3. Verificar crimpagem correta (padrÃ£o T568B)
4. Testar conectividade apÃ³s substituiÃ§Ã£o

## PrevenÃ§Ã£o
- Utilizar cabos de qualidade (blindados para Ã¡reas com interferÃªncia)
- Evitar dobras acentuadas no cabo
- Fixar cabos para evitar movimentaÃ§Ã£o

## Atendimentos onde esta soluÃ§Ã£o foi aplicada
- [[Atendimento - 2026-07-02 - Empresa ABC - Troca de Roteador]]
```

---

## 3. Regras de Linking

### Links ObrigatÃ³rios

| Nota | Links para |
|------|------------|
| Atendimento | Cliente, Equipamentos, SoluÃ§Ã£o, Procedimento |
| Cliente | Equipamentos, Atendimentos |
| Equipamento | Clientes, Atendimentos, Procedimentos, SoluÃ§Ãµes, DocumentaÃ§Ã£o |
| Procedimento | Equipamento, SoluÃ§Ãµes |
| SoluÃ§Ã£o | Equipamentos, Atendimentos |

### Tags Recomendadas

| Nota | Tags MÃ­nimas |
|------|-------------|
| Atendimento | `atendimento`, `{status}`, `{tipo}` (instalaÃ§Ã£o, manutenÃ§Ã£o...) |
| Cliente | `cliente`, `{cidade}`, `{porte}` (pf, pj, empresa) |
| Equipamento | `equipamento`, `{categoria}`, `{marca}` |
| Procedimento | `procedimento`, `{categoria}` |
| SoluÃ§Ã£o | `solucao`, `{categoria}` |

---

## 4. Modelos (Templates)

Os arquivos em `Modelos/` servem como templates que o sistema utiliza ao criar novas notas. Cada modelo contÃ©m a estrutura base com placeholders.

**Modelos disponÃ­veis:**
- `Modelo - Nota de Cliente.md`
- `Modelo - Nota de Equipamento.md`
- `Modelo - Nota de Atendimento.md`
- `Modelo - Nota de Procedimento.md`
- `Modelo - Nota de SoluÃ§Ã£o.md`

---

## 5. Pasta .sistema (Controle)

A pasta `.sistema/` Ã© reservada para arquivos de controle do Hermes. NÃ£o deve ser editada manualmente.

```
ðŸ“ .sistema/
â”œâ”€â”€ vault_metadata.json     # Metadados do vault (versÃ£o, Ãºltima sincronizaÃ§Ã£o)
â”œâ”€â”€ index_status.json       # Status da indexaÃ§Ã£o no Qdrant
â””â”€â”€ schema_version.txt      # VersÃ£o da estrutura do vault
```

---

## 6. Boas PrÃ¡ticas

- **Nomes de arquivo:** Sempre em portuguÃªs, sem acentos, espaÃ§os substituÃ­dos por hÃ­fen.
- **Data:** Formato ISO (YYYY-MM-DD) para consistÃªncia.
- **Frontmatter:** Sempre incluir campos obrigatÃ³rios.
- **Links:** Usar `[[Nome da Nota]]` sempre que referenciar outra entidade.
- **Tags:** Usar tags para facilitar buscas no Obsidian.
- **Imagens:** Armazenar em `_assets/` dentro da pasta relevante.

---

**Premissas:**
- A estrutura pode ser expandida conforme novas necessidades surgirem.
- O sistema respeita a estrutura existente e nÃ£o sobrescreve ediÃ§Ãµes manuais do usuÃ¡rio.

**Riscos:**
- UsuÃ¡rio pode renomear/mover notas manualmente, quebrando links.
- Estrutura muito rÃ­gida pode ser difÃ­cil de manter.

**DÃºvidas em aberto:**
- O sistema deve monitorar alteraÃ§Ãµes manuais no vault para manter consistÃªncia?
- Deve haver uma nota de "Dashboard" com visÃ£o geral do conhecimento?

**PrÃ³ximos passos:**
- Definir MVP (escopo mÃ­nimo viÃ¡vel).
- Priorizar Backlog.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

