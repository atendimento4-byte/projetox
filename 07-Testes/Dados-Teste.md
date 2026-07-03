---
title: "Dados de Teste"
description: "5 clientes, 5 chamados, 2 transcricoes e equipamentos mock"
status: "novo"
---

# Dados de Teste

> **Dados sintÃ©ticos utilizados nos testes de simulaÃ§Ã£o e sandbox.**

---

## 1. Clientes FictÃ­cios

| ID | Nome | Tipo | Equipamentos | HistÃ³rico |
|:--:|------|:----:|:------------:|:---------:|
| CLI-001 | Empresa ABC Ltda | PJ | MikroTik RB951, Cisco 2960 | 4 atendimentos |
| CLI-002 | JoÃ£o Silva | PF | TP-Link Archer, Intelbras IWR | 2 atendimentos |
| CLI-003 | Prefeitura Municipal XYZ | PJ | Huawei OLT, FiberHome ONU | 8 atendimentos |
| CLI-004 | Maria Oliveira ME | PJ | D-Link DGS, APC UPS | 1 atendimento |
| CLI-005 | Escola Estadual Santo AntÃ´nio | PJ | 3 Comutadores, 2 APs Intelbras | 0 atendimentos |

---

## 2. Chamados Simulados

| ID | Cliente | DescriÃ§Ã£o | Status | Data |
|:--:|:-------:|-----------|:------:|:----:|
| CH-001 | CLI-001 | Roteador reiniciando a cada 30 minutos | Aberto | 02/07/2026 |
| CH-002 | CLI-002 | Sem acesso Ã  internet apÃ³s chuva | Em andamento | 01/07/2026 |
| CH-003 | CLI-003 | OLT com porta fÃ­sica danificada | Aguardando peÃ§a | 28/06/2026 |
| CH-004 | CLI-004 | Servidor de NF-e fora do ar | Resolvido | 25/06/2026 |
| CH-005 | CLI-001 | Troca de switch do setor financeiro | OrÃ§amento | 30/06/2026 |

---

## 3. TranscriÃ§Ãµes SintÃ©ticas

### TranscriÃ§Ã£o 1 â€” Queda de Link (CH-001)
```
InÃ­cio do atendimento: 10:30
Cliente: "O roteador fica reiniciando sozinho, umas 3 vezes por hora"
TÃ©cnico: "Vou verificar o cabo de rede"
--- 5 minutos depois ---
TÃ©cnico: "Identifiquei oxidaÃ§Ã£o no conector RJ45. Vou trocar o cabo"
--- 15 minutos depois ---
TÃ©cnico: "Cabo trocado. Conectividadeæ¢å¤æ­£å¸¸. Vou monitorar"
Cliente: "EstÃ¡ normal agora, obrigado"
Fim: 11:20
DecisÃ£o: Troca de cabo de rede com oxidaÃ§Ã£o
```

### TranscriÃ§Ã£o 2 â€” ConfiguraÃ§Ã£o de VLAN (CH-003)
```
InÃ­cio: 14:00
TÃ©cnico: "Qual switch estÃ¡ com problema?"
Cliente: "O Cisco da sala de servidores"
--- 20 minutos depois ---
TÃ©cnico: "Identifiquei configuraÃ§Ã£o incorreta de VLAN 10. A porta 8 estÃ¡ na VLAN errada"
Cliente: "Isso pode causar a queda?"
TÃ©cnico: "Sim, trÃ¡fego da VLAN 10 estÃ¡ sendo enviado para a porta errada"
--- 10 minutos depois ---
TÃ©cnico: "Corrigido. VLAN 10 agora estÃ¡ apenas na porta 8. Testando..."
Cliente: "Voltou ao normal. Obrigado"
DecisÃ£o: CorreÃ§Ã£o de configuraÃ§Ã£o de VLAN
```

---

## 4. E-mails de Exemplo

### SolicitaÃ§Ã£o de Compra
```
Assunto: SolicitaÃ§Ã£o de Compra - Cabo de Rede CAT6 - Empresa ABC
Cliente: Empresa ABC Ltda
Item: Cabo de Rede CAT6 5m (quantidade: 3)
Justificativa: SubstituiÃ§Ã£o de cabos com oxidaÃ§Ã£o identificados durante atendimento
```

### Comunicado Interno
```
Assunto: Atendimento Realizado - Empresa ABC
TÃ©cnico: JoÃ£o (TÃ©cnico Parceiro)
ServiÃ§o: Troca de cabo de rede com oxidaÃ§Ã£o
Status: Resolvido
ObservaÃ§Ãµes: Cliente satisfeito. ConexÃ£oæ¢å¤æ­£å¸¸.
```

---

## 5. Equipamentos Mock

| ID | Tipo | Modelo | Fabricante | Cliente |
|:--:|:----:|--------|:----------:|:-------:|
| EQ-001 | Roteador | RB951Ui-2HnD | MikroTik | CLI-001 |
| EQ-002 | Switch | Catalyst 2960 | Cisco | CLI-001 |
| EQ-003 | Roteador | Archer C80 | TP-Link | CLI-002 |
| EQ-004 | Roteador | IWR 3000N | Intelbras | CLI-002 |
| EQ-005 | OLT | SmartAX MA5600T | Huawei | CLI-003 |
| EQ-006 | Servidor | PowerEdge R740 | Dell | CLI-004 |

---

## 6. GeraÃ§Ã£o de Dados

Dados de teste sÃ£o gerados por factories no cÃ³digo (`testes/_dados/`):

- `fabrica_cliente.py` â€” gera clientes com dados consistentes
- `fabrica_chamado.py` â€” gera chamados com estados vÃ¡lidos
- `fabrica_transcricao.py` â€” gera transcriÃ§Ãµes sintÃ©ticas
- `fabrica_email.py` â€” gera e-mails conforme templates

---

## 7. Versionamento

Dados de teste ficam em `testes/_dados/` e sÃ£o versionados no git.
Nunca conter dados reais de clientes.
Nunca conter secrets, senhas ou tokens.

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

