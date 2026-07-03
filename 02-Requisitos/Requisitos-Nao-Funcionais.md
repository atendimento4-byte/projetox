---
title: "Requisitos Nao Funcionais"
description: "23 requisitos nao funcionais em 7 categorias"
status: "concluido"
---

# Requisitos NÃ£o Funcionais

> **RestriÃ§Ãµes e qualidades do sistema (performance, seguranÃ§a, disponibilidade, usabilidade, etc.).**
> Organizados por categoria com critÃ©rios de aceitaÃ§Ã£o mensurÃ¡veis.

---

## 1. Desempenho (Performance)

### RNF-DES-001 â€” Tempo de TranscriÃ§Ã£o
**DescriÃ§Ã£o:** A transcriÃ§Ã£o de Ã¡udio deve ser processada em tempo prÃ³ximo ao real para Ã¡udios de atÃ© 5 minutos.
**CritÃ©rio:** Ãudio de 5 minutos deve ser transcrito em no mÃ¡ximo 30 segundos.
**Prioridade:** Alta

### RNF-DES-002 â€” Tempo de Resposta da IA
**DescriÃ§Ã£o:** As sugestÃµes e respostas da IA devem ser geradas em tempo hÃ¡bil para nÃ£o interromper o fluxo do atendimento.
**CritÃ©rio:** Resposta da IA em atÃ© 10 segundos para consultas ao histÃ³rico.
**Prioridade:** Alta

### RNF-DES-003 â€” Tempo de Consulta ao Banco Vetorial
**DescriÃ§Ã£o:** A busca semÃ¢ntica na base de conhecimento deve ser rÃ¡pida o suficiente para ser usada durante o atendimento.
**CritÃ©rio:** Consulta vetorial com resultado em atÃ© 3 segundos.
**Prioridade:** Alta

### RNF-DES-004 â€” Consumo de Recursos
**DescriÃ§Ã£o:** O sistema nÃ£o deve comprometer o desempenho da mÃ¡quina do usuÃ¡rio durante o uso.
**CritÃ©rio:** Uso de CPU e memÃ³ria deve ser inferior a 30% em mÃ¡quina de configuraÃ§Ã£o mediana (16GB RAM, i7 ou equivalente).
**Prioridade:** MÃ©dia

---

## 2. Disponibilidade e Confiabilidade

### RNF-DISP-001 â€” Disponibilidade em HorÃ¡rio Comercial
**DescriÃ§Ã£o:** O sistema deve estar disponÃ­vel durante o horÃ¡rio de trabalho do usuÃ¡rio (08h-18h, dias Ãºteis).
**CritÃ©rio:** 99% de uptime neste perÃ­odo.
**Prioridade:** Alta

### RNF-DISP-002 â€” TolerÃ¢ncia a Falhas de Rede
**DescriÃ§Ã£o:** O sistema deve funcionar de forma degradada quando sem internet, mantendo funcionalidades locais (Obsidian, transcriÃ§Ã£o local).
**CritÃ©rio:** Funcionalidades offline devem ser identificadas e o usuÃ¡rio notificado sobre a indisponibilidade de serviÃ§os externos.
**Prioridade:** MÃ©dia

### RNF-DISP-003 â€” RecuperaÃ§Ã£o de Falhas
**DescriÃ§Ã£o:** Em caso de falha (crash, queda de energia), o sistema deve recuperar o estado do acompanhamento sem perda significativa de dados.
**CritÃ©rio:** Perda mÃ¡xima de dados de 30 segundos de Ã¡udio nÃ£o salvo.
**Prioridade:** Alta

---

## 3. SeguranÃ§a

### RNF-SEG-001 â€” Criptografia em Repouso
**DescriÃ§Ã£o:** Dados sensÃ­veis (gravaÃ§Ãµes de Ã¡udio, dados de clientes) devem ser armazenados com criptografia.
**CritÃ©rio:** AES-256 para arquivos em disco.
**Prioridade:** Alta

### RNF-SEG-002 â€” Criptografia em TrÃ¢nsito
**DescriÃ§Ã£o:** Toda comunicaÃ§Ã£o com serviÃ§os externos (API Movidesk, LLM, e-mail) deve ser criptografada.
**CritÃ©rio:** TLS 1.3 ou superior.
**Prioridade:** Alta

### RNF-SEG-003 â€” AutenticaÃ§Ã£o do UsuÃ¡rio
**DescriÃ§Ã£o:** O sistema deve exigir autenticaÃ§Ã£o do usuÃ¡rio para acesso (especialmente se exposto em rede).
**CritÃ©rio:** AutenticaÃ§Ã£o local ou SSO. Bloqueio apÃ³s 5 tentativas falhas.
**Prioridade:** MÃ©dia

### RNF-SEG-004 â€” Log de Auditoria
**DescriÃ§Ã£o:** Todas as aÃ§Ãµes crÃ­ticas (gravaÃ§Ã£o, envio de e-mail, fechamento de OS) devem ser registradas com timestamp, aÃ§Ã£o e decisÃ£o do usuÃ¡rio.
**CritÃ©rio:** Log imutÃ¡vel (append-only) armazenado localmente.
**Prioridade:** Alta

---

## 4. Privacidade e Conformidade

### RNF-PRIV-001 â€” Consentimento para GravaÃ§Ã£o
**DescriÃ§Ã£o:** Nenhuma gravaÃ§Ã£o de Ã¡udio pode iniciar sem comando explÃ­cito do usuÃ¡rio.
**CritÃ©rio:** Indicador visual obrigatÃ³rio durante gravaÃ§Ã£o. Log de inÃ­cio/fim.
**Prioridade:** CrÃ­tica

### RNF-PRIV-002 â€” LGPD
**DescriÃ§Ã£o:** O sistema deve estar em conformidade com a LGPD no tratamento de dados pessoais dos clientes.
**CritÃ©rio:** Dados pessoais devem ser armazenados com finalidade especÃ­fica e passÃ­veis de exclusÃ£o mediante solicitaÃ§Ã£o.
**Prioridade:** Alta

### RNF-PRIV-003 â€” RetenÃ§Ã£o de Dados
**DescriÃ§Ã£o:** O sistema deve permitir configurar polÃ­tica de retenÃ§Ã£o para gravaÃ§Ãµes de Ã¡udio (ex.: apagar apÃ³s 90 dias).
**CritÃ©rio:** ConfiguraÃ§Ã£o de perÃ­odo de retenÃ§Ã£o por tipo de dado.
**Prioridade:** MÃ©dia

---

## 5. Usabilidade

### RNF-USA-001 â€” Curva de Aprendizado
**DescriÃ§Ã£o:** O sistema deve ser intuitivo para o usuÃ¡rio, que jÃ¡ conhece o fluxo de trabalho.
**CritÃ©rio:** UsuÃ¡rio deve ser capaz de realizar as tarefas principais (iniciar atendimento, gravar Ã¡udio, registrar conhecimento) em menos de 30 minutos de uso.
**Prioridade:** Alta

### RNF-USA-002 â€” Feedback Imediato
**DescriÃ§Ã£o:** O sistema deve fornecer feedback imediato para cada aÃ§Ã£o do usuÃ¡rio.
**CritÃ©rio:** ConfirmaÃ§Ã£o visual ou textual em atÃ© 1 segundo apÃ³s comando.
**Prioridade:** Alta

### RNF-USA-003 â€” MÃ­nimo de Cliques/Comandos
**DescriÃ§Ã£o:** As aÃ§Ãµes mais frequentes (iniciar/parar gravaÃ§Ã£o, pedir resumo) devem ser acessÃ­veis com mÃ­nimo de interaÃ§Ãµes.
**CritÃ©rio:** MÃ¡ximo de 2 cliques ou comandos para aÃ§Ãµes principais.
**Prioridade:** MÃ©dia

### RNF-USA-004 â€” Temas e PersonalizaÃ§Ã£o
**DescriÃ§Ã£o:** O sistema deve oferecer modo claro e escuro, e permitir personalizaÃ§Ã£o de atalhos.
**Prioridade:** Baixa

---

## 6. Manutenibilidade

### RNF-MAN-001 â€” Modularidade
**DescriÃ§Ã£o:** O sistema deve ser modular, permitindo a substituiÃ§Ã£o de componentes individuais (ex.: trocar Whisper por outro transcriÃ§Ã£o) sem impacto nos demais mÃ³dulos.
**CritÃ©rio:** Componentes com interfaces bem definidas (ports/adapters).
**Prioridade:** Alta

### RNF-MAN-002 â€” Testabilidade
**DescriÃ§Ã£o:** O sistema deve ser projetado para permitir testes automatizados em todos os mÃ³dulos.
**CritÃ©rio:** Cobertura de testes >= 70% no cÃ³digo.
**Prioridade:** Alta

### RNF-MAN-003 â€” DocumentaÃ§Ã£o
**DescriÃ§Ã£o:** A arquitetura e os componentes devem ser documentados para facilitar manutenÃ§Ã£o futura.
**CritÃ©rio:** README por mÃ³dulo, diagramas de arquitetura, [[04-Arquitetura/ADRs.md|ADRs]].
**Prioridade:** MÃ©dia

---

## 7. Portabilidade

### RNF-PORT-001 â€” Suporte a Windows
**DescriÃ§Ã£o:** O sistema deve funcionar no Windows (plataforma primÃ¡ria do usuÃ¡rio).
**CritÃ©rio:** Todos os mÃ³dulos devem ser compatÃ­veis com Windows 10/11.
**Prioridade:** Alta

### RNF-PORT-002 â€” ExecuÃ§Ã£o Local
**DescriÃ§Ã£o:** O sistema deve executar predominantemente na mÃ¡quina local do usuÃ¡rio.
**CritÃ©rio:** NÃ£o deve exigir servidor remoto para funcionamento bÃ¡sico.
**Prioridade:** Alta

---

## Matriz de Prioridades por Categoria

| Categoria | Total | CrÃ­tica | Alta | MÃ©dia | Baixa |
|-----------|-------|:-------:|:----:|:-----:|:-----:|
| Desempenho | 4 | â€” | 3 | 1 | â€” |
| Disponibilidade | 3 | â€” | 2 | 1 | â€” |
| SeguranÃ§a | 4 | â€” | 3 | 1 | â€” |
| Privacidade | 3 | 1 | 1 | 1 | â€” |
| Usabilidade | 4 | â€” | 2 | 1 | 1 |
| Manutenibilidade | 3 | â€” | 2 | 1 | â€” |
| Portabilidade | 2 | â€” | 2 | â€” | â€” |
| **Total** | **23** | **1** | **15** | **6** | **1** |

---

**Premissas:**
- Os RNFs podem ser ajustados conforme descobertas tÃ©cnicas durante a implementaÃ§Ã£o.
- A mÃ¡quina do usuÃ¡rio tem Windows 10/11 com pelo menos 16GB RAM e conexÃ£o com internet.

**Riscos:**
- Funcionalidades offline (RNF-DISP-002) podem ser complexas de implementar dependendo da dependÃªncia de LLM externo.
- Criptografia (RNF-SEG-001) adiciona complexidade ao desenvolvimento.

**DÃºvidas em aberto:**
- O sistema deve suportar Linux/Mac tambÃ©m ou apenas Windows?
- A transcriÃ§Ã£o serÃ¡ local (Whisper local) ou via API (Whisper API)?

**PrÃ³ximos passos:**
- Detalhar [[02-Requisitos/Casos-de-Uso.md|Casos de Uso]].

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

