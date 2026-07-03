---
title: "Checklist MVP"
description: "10 funcionalidades checkaveis com 39 itens de verificacao"
status: "novo"
---

# Checklist de VerificaÃ§Ã£o do MVP

> **Checklist para verificar o progresso da implementaÃ§Ã£o das funcionalidades previstas para o MVP.**
> Atualizar conforme cada funcionalidade for concluÃ­da.

---

## Funcionalidade 1: Acompanhamento de Chamados

- [ ] CLI `hermes chamado iniciar <id>` cria sessÃ£o ativa
- [ ] CLI `hermes chamado status <id>` exibe status atual
- [ ] CLI `hermes chamado finalizar <id>` encerra sessÃ£o
- [ ] SessÃ£o salva no banco de dados

## Funcionalidade 2: GravaÃ§Ã£o opcional de Ã¡udio

- [ ] Iniciar gravaÃ§Ã£o com `hermes audio start`
- [ ] Parar gravaÃ§Ã£o com `hermes audio stop`
- [ ] Indicador visual de gravaÃ§Ã£o ativa
- [ ] Criptografia do arquivo em repouso

## Funcionalidade 3: TranscriÃ§Ã£o com Whisper

- [ ] Envio do Ã¡udio para API Whisper
- [ ] TranscriÃ§Ã£o retornada em texto
- [ ] TranscriÃ§Ã£o salva no banco de dados vinculada ao chamado
- [ ] Hotkey para iniciar/parar (Ctrl+Shift+R)

## Funcionalidade 4: Resumo inteligente com IA

- [ ] Comando `hermes chamado resumir <id>` gera resumo
- [ ] Resumo estruturado (problema, soluÃ§Ã£o, decisÃµes)
- [ ] UsuÃ¡rio aprova/edita antes de salvar
- [ ] Resumo salvo no Obsidian

## Funcionalidade 5: CriaÃ§Ã£o automÃ¡tica de notas no Obsidian

- [ ] Notas criadas na estrutura de pastas correta
- [ ] Note types: Chamado, Cliente, Equipamento, Procedimento
- [ ] Links entre notas (chamado â†’ cliente â†’ equipamento)
- [ ] Template respeitado (YAML frontmatter, seÃ§Ãµes)

## Funcionalidade 6: Consulta semÃ¢ntica

- [ ] Comando `hermes consultar "texto"` retorna resultados
- [ ] Busca por similaridade via Qdrant
- [ ] Resultados priorizados por relevÃ¢ncia
- [ ] Exibe trechos do histÃ³rico

## Funcionalidade 7: SugestÃ£o de soluÃ§Ãµes

- [ ] Durante acompanhamento, sistema sugere soluÃ§Ãµes baseadas em histÃ³rico
- [ ] SugestÃµes exibidas na CLI
- [ ] UsuÃ¡rio aceita/rejeita sugestÃµes

## Funcionalidade 8: Fechamento de OS no Movidesk

- [ ] GeraÃ§Ã£o de resumo a partir da transcriÃ§Ã£o
- [ ] UsuÃ¡rio aprova/edita o resumo
- [ ] AtualizaÃ§Ã£o do chamado no Movidesk via API
- [ ] Resumo salvo localmente como referÃªncia

## Funcionalidade 9: GeraÃ§Ã£o de e-mails

- [ ] Modelos de e-mail: solicitaÃ§Ã£o de compra, comunicado interno
- [ ] Comando `hermes email gerar <id> --tipo compra`
- [ ] Texto prÃ©-preenchido com dados do atendimento
- [ ] UsuÃ¡rio edita antes de enviar

## Funcionalidade 10: SeguranÃ§a bÃ¡sica

- [ ] Todos os comandos crÃ­ticos exigem confirmaÃ§Ã£o
- [ ] Logs de auditoria registram todas as aÃ§Ãµes
- [ ] Chaves de API armazenadas de forma segura
- [ ] AutenticaÃ§Ã£o Named Pipe com token

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

