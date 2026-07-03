---
title: "Seguranca"
description: "Autenticacao, criptografia, controle de acesso e auditoria"
status: "concluido"
---

# SeguranÃ§a

> **PolÃ­ticas, mecanismos e controles de seguranÃ§a do sistema.**
>
> Ver tambÃ©m [[04-Arquitetura/Privacidade.md|Privacidade]] para questÃµes de LGPD e consentimento, e [[03-Comportamento/Riscos.md|Riscos]] para riscos de seguranÃ§a mapeados.

---

## PrincÃ­pios

1. **Menor privilÃ©gio:** O sistema opera apenas com as permissÃµes necessÃ¡rias.
2. **Defesa em profundidade:** MÃºltiplas camadas de seguranÃ§a.
3. **Zero confianÃ§a:** Nenhuma aÃ§Ã£o Ã© confiÃ¡vel sem verificaÃ§Ã£o.
4. **Auditabilidade:** Toda aÃ§Ã£o relevante Ã© registrada.

---

## 1. AutenticaÃ§Ã£o

### CenÃ¡rios

| CenÃ¡rio | Mecanismo | Quando |
|---------|-----------|--------|
| Uso local (Ãºnico usuÃ¡rio) | Login do Windows | O sistema herda a autenticaÃ§Ã£o do SO |
| Acesso remoto (futuro) | Senha mestra + 2FA | Se exposto em rede |

### ImplementaÃ§Ã£o
- **Local:** O sistema confia no usuÃ¡rio logado no Windows.
- **Se expandido:** AutenticaÃ§Ã£o com senha mestra armazenada em hash (bcrypt/Argon2).

---

## 2. Criptografia

### Em Repouso

| Dado | Algoritmo | Onde |
|------|-----------|------|
| GravaÃ§Ãµes de Ã¡udio | AES-256-GCM | Disco local |
| Chaves de API | AES-256 (via Windows Credential Manager) | Credential Store do SO |
| ConfiguraÃ§Ãµes sensÃ­veis | AES-256-GCM | Arquivo de configuraÃ§Ã£o criptografado |
| Logs de auditoria | Append-only (nÃ£o criptografado, mas imutÃ¡vel) | Disco local |
| Notas do Obsidian | Opcional (criptografia do vault) | Disco local |

### Em TrÃ¢nsito

| ConexÃ£o | Protocolo | Onde |
|---------|-----------|------|
| API Movidesk | TLS 1.3 | Internet |
| LLM API | TLS 1.3 | Internet |
| E-mail (SMTP) | STARTTLS / TLS | Internet |
| Qdrant (local) | Sem TLS (rede local) | Localhost |
| n8n (local) | Sem TLS (rede local) | Localhost |

### Gerenciamento de Chaves

| Chave | Armazenamento | RotaÃ§Ã£o |
|-------|---------------|---------|
| Chave de criptografia local | Windows CNG / DPAPI | A cada 90 dias |
| Token Movidesk | Windows Credential Manager | Conforme polÃ­tica do Movidesk |
| API Key LLM | Windows Credential Manager | A cada 180 dias |
| Senha de e-mail | Windows Credential Manager | Conforme polÃ­tica do provedor |

---

## 3. ProteÃ§Ã£o de Dados SensÃ­veis

### ClassificaÃ§Ã£o dos Dados

| NÃ­vel | Exemplos | Armazenamento |
|-------|----------|---------------|
| **CrÃ­tico** | Chaves de API, tokens de acesso | Windows Credential Manager (criptografado) |
| **SensÃ­vel** | GravaÃ§Ãµes de Ã¡udio, dados pessoais de clientes | Disco criptografado (AES-256) |
| **Interno** | Notas do Obsidian, logs | Disco local (sem criptografia adicional) |
| **PÃºblico** | CÃ³digo-fonte, documentaÃ§Ã£o | RepositÃ³rio git |

### PrÃ¡ticas
- Nunca hardcodar secrets no cÃ³digo-fonte.
- Arquivos `.env` adicionados ao `.gitignore`.
- RevisÃ£o de cÃ³digo para evitar vazamento de credenciais.

---

## 4. Controle de Acesso

### AÃ§Ãµes CrÃ­ticas (requerem aprovaÃ§Ã£o explÃ­cita)

| AÃ§Ã£o | Requisito |
|------|-----------|
| Iniciar gravaÃ§Ã£o de Ã¡udio | Dupla confirmaÃ§Ã£o obrigatÃ³ria |
| Enviar e-mail | RevisÃ£o + aprovaÃ§Ã£o |
| Fechar OS no Movidesk | RevisÃ£o + aprovaÃ§Ã£o |
| Alterar notas no Obsidian | RevisÃ£o + aprovaÃ§Ã£o |
| Excluir gravaÃ§Ã£o | ConfirmaÃ§Ã£o obrigatÃ³ria |

### NÃ­veis de Acesso

| NÃ­vel | AÃ§Ãµes | Quem |
|-------|-------|------|
| **Admin** | Todas as aÃ§Ãµes + configurar sistema | Supervisor (vocÃª) |
| **UsuÃ¡rio** | AÃ§Ãµes operacionais (futuro, se expandir) | TÃ©cnico parceiro (se acesso direto) |

---

## 5. Logs de Auditoria

### Eventos Registrados

| Categoria | Eventos |
|-----------|---------|
| **SessÃ£o** | InÃ­cio/fim de acompanhamento |
| **Ãudio** | InÃ­cio/fim de gravaÃ§Ã£o, exclusÃ£o |
| **TranscriÃ§Ã£o** | SolicitaÃ§Ã£o, sucesso, falha |
| **Obsidian** | CriaÃ§Ã£o/atualizaÃ§Ã£o/exclusÃ£o de notas |
| **E-mail** | GeraÃ§Ã£o, envio, rejeiÃ§Ã£o |
| **Movidesk** | Consulta, atualizaÃ§Ã£o, fechamento |
| **AprovaÃ§Ã£o** | AprovaÃ§Ã£o, rejeiÃ§Ã£o, ediÃ§Ã£o de aÃ§Ã£o pendente |
| **Erro** | Falhas de sistema, APIs, componentes |

### Formato do Log

```json
{
  "timestamp": "2026-07-02T12:30:00Z",
  "event_type": "audio.recording.started",
  "session_id": "SES-001",
  "user": "supervisor",
  "details": { "duration": null, "source": "hotkey" },
  "decision": null,
  "hash": "sha256-do-conteudo-anterior"
}
```

> Logs sÃ£o armazenados conforme modelo em [[05-Dados/Banco-de-Dados.md]].

### Imutabilidade
- Logs em formato append-only (arquivo de log sequencial).
- Hash encadeado (cada entrada contÃ©m hash da anterior) para detectar adulteraÃ§Ã£o.

---

## 6. SeguranÃ§a de Rede

| ServiÃ§o | Porta | Acesso |
|---------|-------|--------|
| CL Interface | N/A (local) | Apenas processo local |
| API Interna (Hermes) | localhost:8790 | Apenas localhost |
| Qdrant | localhost:6333 | Apenas localhost |
| Redis | localhost:6379 | Apenas localhost |
| PostgreSQL | localhost:5432 | Apenas localhost |
| n8n | localhost:5678 | Apenas localhost |

> **Regra:** Nenhum serviÃ§o deve estar exposto para a rede externa.

---

## 7. Backup e RecuperaÃ§Ã£o

### O que Ã© backupado

| Item | FrequÃªncia | Destino |
|------|------------|---------|
| Vault do Obsidian | DiÃ¡rio (automÃ¡tico) | Nuvem + disco externo |
| Banco PostgreSQL | DiÃ¡rio (dump) | Disco local + nuvem |
| ConfiguraÃ§Ãµes sensÃ­veis | A cada alteraÃ§Ã£o | Backup criptografado |
| GravaÃ§Ãµes de Ã¡udio | Semanal | Disco externo (ou conforme polÃ­tica de retenÃ§Ã£o) |

### PolÃ­tica de RetenÃ§Ã£o

| Tipo de Dado | PerÃ­odo | AÃ§Ã£o apÃ³s perÃ­odo |
|--------------|---------|-------------------|
| GravaÃ§Ãµes de Ã¡udio | 90 dias | ExclusÃ£o automÃ¡tica |
| Logs de auditoria | 1 ano | CompactaÃ§Ã£o |
| Notas do Obsidian | Indeterminado | Mantido (backup contÃ­nuo) |
| Dados de clientes (cache) | 30 dias | Limpeza |

---

## 8. Resposta a Incidentes

### Matriz de Incidentes

| Incidente | Gravidade | AÃ§Ã£o Imediata | CorreÃ§Ã£o |
|-----------|-----------|---------------|----------|
| GravaÃ§Ã£o nÃ£o autorizada | CrÃ­tica | Parar gravaÃ§Ã£o, apagar Ã¡udio, notificar | Revisar cÃ³digo, reforÃ§ar controle |
| Vazamento de chave API | Alta | Rotacionar chave, revogar acesso | Remover exposiÃ§Ã£o |
| Perda de dados Obsidian | Alta | Restaurar backup mais recente | Revisar mecanismo de backup |
| Acesso nÃ£o autorizado | CrÃ­tica | Bloquear acesso, revisar logs | ForÃ§ar autenticaÃ§Ã£o |
| Falha de criptografia | MÃ©dia | Revisar implementaÃ§Ã£o | Corrigir e re-criptografar |

---

**Premissas:**
- O sistema roda em mÃ¡quina local do usuÃ¡rio (ambiente controlado).
- Windows Defender ou antivÃ­rus equivalente estÃ¡ ativo.

**Riscos:**
- A criptografia adiciona complexidade e pode impactar performance.
- Gerenciamento de chaves Ã© responsabilidade do usuÃ¡rio.

**DÃºvidas em aberto:**
- Deve haver criptografia no vault do Obsidian? (Obsidian suporta criptografia via plugin.)
- NecessÃ¡rio hardening adicional no Windows?

**PrÃ³ximos passos:**
- Especificar Privacidade (LGPD).
- Detalhar Agentes.

---
> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

