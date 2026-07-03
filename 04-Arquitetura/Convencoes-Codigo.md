---
title: "Convencoes de Codigo"
description: "DDD Tattico, Result[T,E], logging JSON, DI, testes por camada"
status: "concluido"
---

# ConvenÃ§Ãµes de CÃ³digo

> **PadrÃµes de estilo, nomenclatura, arquitetura DDD, tratamento de erros, logging, testes, dependÃªncias e pipeline de qualidade.**
> Todo cÃ³digo do Hermes deve seguir estas convenÃ§Ãµes para garantir consistÃªncia, manutenibilidade e escalabilidade.

---

## 1. Linguagem e Runtime

- **Python 3.12+** â€” versÃ£o mÃ­nima obrigatÃ³ria (conforme [[04-Arquitetura/ADRs.md|ADR-008]])
- **Type hints obrigatÃ³rios** em todo cÃ³digo, inclusive privado
- **PEP 604** para uniÃ£o de tipos: `str | None` em vez de `Optional[str]`
- **PEP 585** para tipos genÃ©ricos: `list[str]` em vez de `List[str]`
- **`@dataclass`** como padrÃ£o para classes de dados; `NamedTuple` apenas para imutÃ¡veis simples
- **`Enum`** como `class MeuEnum(str, Enum)` para compatibilidade com serializaÃ§Ã£o

---

## 2. Estilo e FormataÃ§Ã£o

| Ferramenta | FunÃ§Ã£o | ConfiguraÃ§Ã£o |
|-----------|--------|-------------|
| **Ruff** | Formatador + Linter | Linha com 100 caracteres. Regras: `E`, `F`, `I`, `N`, `W`, `UP`, `B`, `SIM`, `ARG`, `COM`, `C4`, `T10`, `RUF`, `PL`, `PT`, `RET`, `TRY`, `EM`, `C90` |
| **mypy** | Verificador de tipos | Modo `strict`. Desabilitar `explicit_override` e `explicit_package_bases` se necessÃ¡rio |

**PrÃ©-commit obrigatÃ³rio:**
1. `ruff format .` â€” formataÃ§Ã£o automÃ¡tica
2. `ruff check . --fix` â€” lint + correÃ§Ãµes automÃ¡ticas
3. `mypy src/` â€” verificaÃ§Ã£o de tipos
4. `pytest --cov=src` â€” testes com cobertura

---

## 3. Nomenclatura

**Idioma:** portuguÃªs (PTBR) para pastas, arquivos, mÃ³dulos, classes, funÃ§Ãµes, variÃ¡veis, constantes, enums, interfaces e comentÃ¡rios.
ExceÃ§Ã£o: APIs externas (Movidesk, Whisper) mantÃªm nomes originais.

| Elemento | PadrÃ£o | Exemplo |
|----------|--------|---------|
| Pacotes | `maiusculo_minusculo` | `contexto.acompanhamento` |
| MÃ³dulos | `maiusculo_minusculo` | `servico_chamado.py` |
| Pastas | `maiusculo_minusculo` | `contexto/audio/infra/gravador/` |
| Classes | `PascalCase` | `ServicoChamado` |
| FunÃ§Ãµes/MÃ©todos | `maiusculo_minusculo` | `iniciar_chamado()` |
| VariÃ¡veis | `maiusculo_minusculo` | `chamado_ativo` |
| Constantes | `UPPER_SNAKE_CASE` | `TEMPO_MAXIMO_RETRY` |
| Enum | `PascalCase` | `class StatusChamado(str, Enum)` |
| Interfaces/ABC | Prefixo `I` | `IRepositorioChamado` |
| Tipos (TypeAlias) | `PascalCase` | `tipo IdChamado = int` |
| ExceÃ§Ãµes | Sufixo `Erro` | `ChamadoNaoEncontradoErro` |
| Privado | Prefixo `_` | `_processar_audio()` |
| Dunder | Apenas protocolos | `__enter__`, `__exit__` |

**Regras de nomenclatura:**
- Nomes devem ser **auto-explicativos**: `calcular_valor_total()` em vez de `calc()`
- Evitar abreviaÃ§Ãµes: `repositorio` em vez de `repo`
- Booleanos usar prefixo: `ativo`, `visivel`, `autorizado`
- MÃ³dulos no singular: `servico.py`, `entidade.py`, `repositorio.py`

---

## 4. DDD TÃ¡tico

### 4.1 â€” Entidade

Objeto com identidade Ãºnica (UUID) que persiste ao longo do tempo e do estado.

```python
@dataclass
class Chamado:
    id: IdChamado
    cliente_id: IdCliente
    status: StatusChamado
    data_abertura: datetime
```

**Onde colocar:** `contexto/acompanhamento/dominio/entidades/chamado.py`

### 4.2 â€” Value Object

Objeto imutÃ¡vel sem identidade. Define atributos do domÃ­nio.

```python
@dataclass(frozen=True)
class EmailCliente:
    endereco: str

    def validar(self) -> bool:
        return "@" in self.endereco
```

**Onde colocar:** `contexto/acompanhamento/dominio/objetos_valor/email_cliente.py`

### 4.3 â€” Aggregate

Grupo de entidades e VOs tratados como unidade. Uma entidade raiz (Aggregate Root) garante consistÃªncia.

**Regras:**
- Aggregate Root Ã© a Ãºnica entrada para o aggregate
- ReferÃªncias externas apenas por ID
- TransaÃ§Ãµes atÃ´micas dentro do aggregate

### 4.4 â€” Domain Event

Evento que representa algo relevante que aconteceu no domÃ­nio.

```python
@dataclass
class ChamadoFinalizado:
    chamado_id: IdChamado
    data_hora: datetime
    usuario_id: IdUsuario
```

**Onde colocar:** `contexto/acompanhamento/dominio/eventos/chamado_finalizado.py`

### 4.5 â€” Repository (Interface)

Interface de persistÃªncia definida no domÃ­nio. ImplementaÃ§Ã£o na infraestrutura.

```python
class IRepositorioChamado(ABC):
    @abstractmethod
    def obter_por_id(self, id: IdChamado) -> Chamado | None: ...
    @abstractmethod
    def salvar(self, chamado: Chamado) -> Chamado: ...
```

**Onde colocar:** `contexto/acompanhamento/dominio/repositorios/repositorio_chamado.py`

### 4.6 â€” Use Case (Application Service)

Orquestra o fluxo de uma operaÃ§Ã£o. Depende de interfaces, nÃ£o de implementaÃ§Ãµes.

```python
class IniciarChamado:
    def __init__(self, repo: IRepositorioChamado, ...): ...
    def executar(self, comando: IniciarChamadoComando) -> Resultado[Chamado]: ...
```

**Onde colocar:** `contexto/acompanhamento/aplicacao/casos_uso/iniciar_chamado.py`

### 4.7 â€” Domain Service

LÃ³gica de negÃ³cio que nÃ£o se encaixa naturalmente em uma entidade ou VO.

**Onde colocar:** `contexto/acompanhamento/dominio/servicos/`

### 4.8 â€” Factory

Encapsula lÃ³gica de criaÃ§Ã£o de objetos complexos.

### 4.9 â€” Specification

Encapsula regras de negÃ³cio reutilizÃ¡veis em objetos.

---

## 5. Tratamento de Erros

Usar **Resultado[T, Erro]** para operaÃ§Ãµes que podem falhar + **exceÃ§Ãµes** para erros inesperados.

### 5.1 â€” Resultado Pattern

```python
@dataclass
class Resultado[T, E]:
    sucesso: bool
    valor: T | None = None
    erro: E | None = None

    @classmethod
    def ok(cls, valor: T) -> Resultado[T, E]:
        return cls(sucesso=True, valor=valor)

    @classmethod
    def falha(cls, erro: E) -> Resultado[T, E]:
        return cls(sucesso=False, erro=erro)

    def is_ok(self) -> bool:
        return self.sucesso

    def is_falha(self) -> bool:
        return not self.sucesso

    def obter_valor(self) -> T:
        if not self.sucesso:
            raise ErroAcessoResultado("Resultado nÃ£o contÃ©m valor")
        return self.valor

    def obter_erro(self) -> E:
        if self.sucesso:
            raise ErroAcessoResultado("Resultado nÃ£o contÃ©m erro")
        return self.erro
```

**Onde colocar:** `compartilhado/erros/resultado.py`

### 5.2 â€” Hierarquia de Erros

```
ErroAplicacao (base abstrata)
â”œâ”€â”€ ErroDominio
â”‚   â”œâ”€â”€ ErroRegraNegocio           # Regra de negÃ³cio violada
â”‚   â””â”€â”€ ErroEntidadeNaoEncontrada  # Entidade nÃ£o existe
â”œâ”€â”€ ErroAplicacaoServico           # Erro em use case
â””â”€â”€ ErroInfraestrutura
    â”œâ”€â”€ ErroPersistencia           # Banco de dados, Qdrant
    â”œâ”€â”€ ErroComunicacao            # API externa, rede
    â”œâ”€â”€ ErroConfiguracao           # Config ausente ou invÃ¡lida
    â””â”€â”€ ErroTranscricao            # Whisper/Ia falhou
```

**Onde colocar:** `compartilhado/erros/`

### 5.3 â€” Regras de Uso

| SituaÃ§Ã£o | Usar |
|----------|------|
| ValidaÃ§Ã£o de regra de negÃ³cio | `Resultado.falha(ErroRegraNegocio(...))` |
| Entidade nÃ£o encontrada | `Resultado.falha(ErroEntidadeNaoEncontrada(...))` |
| Argumento invÃ¡lido | `Resultado.falha(ErroDominio(...))` |
| Falha de infraestrutura | LanÃ§ar `ErroPersistencia` |
| Bug/assertiva | `assert` ou `ValueError` |
| Erro externo inesperado | Capturar e relanÃ§ar como `ErroComunicacao` |

---

## 6. Logging e Observabilidade

### 6.1 â€” Estrutura

Formato **JSON estruturado** para permitir ingestÃ£o por ferramentas de log:

```json
{
  "timestamp": "2026-07-02T10:30:00.123Z",
  "nivel": "INFO",
  "logger": "contexto.acompanhamento",
  "mensagem": "Chamado iniciado",
  "id_correlacao": "abc-123-def",
  "contexto": {
    "chamado_id": "ch_001",
    "usuario_id": "usr_01"
  },
  "duracao_ms": 150
}
```

### 6.2 â€” NÃ­veis

| NÃ­vel | Uso |
|-------|-----|
| `DEBUG` | DiagnÃ³stico detalhado, apenas durante desenvolvimento |
| `INFO` | Eventos normais: "chamado iniciado", "transcriÃ§Ã£o concluÃ­da" |
| `WARNING` | SituaÃ§Ãµes anormais nÃ£o crÃ­ticas: retry, timeout |
| `ERROR` | Erro operacional que exige atenÃ§Ã£o |
| `CRITICAL` | Falha catastrÃ³fica: serviÃ§o nÃ£o inicia |

### 6.3 â€” Regras

- Toda requisiÃ§Ã£o (comando CLI ou evento interno) recebe um `id_correlacao` Ãºnico
- O correlation ID Ã© propagado em toda a cadeia de chamadas
- Objetos de domÃ­nio nÃ£o fazem logging â€” logging Ã© responsabilidade da aplicaÃ§Ã£o/infra
- Log em JSON (biblioteca `structlog` ou `python-json-logger`)
- Dados sensÃ­veis (senhas, tokens, CPF) nunca sÃ£o logados

---

## 7. Testes

### 7.1 â€” PirÃ¢mide

```
        â•±â•²
       â•± E2E â•²          ~10% â€” fluxos completos
      â•±â”€â”€â”€â”€â”€â”€â”€â”€â•²
     â•± IntegraÃ§Ã£o â•²      ~20% â€” repositÃ³rios, adaptadores, IPC
    â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
   â•±   UnitÃ¡rios     â•²   ~70% â€” domÃ­nio, VOs, use cases, serviÃ§os
  â•±â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•²
```

### 7.2 â€” PadrÃµes

| PadrÃ£o | Uso |
|--------|-----|
| **Factory** | Criar entidades e VOs para testes com dados consistentes |
| **Fixture** | Dados prÃ©-definidos para cenÃ¡rios recorrentes |
| **Mock** | Simular interfaces externas (API, banco, arquivos) |
| **Stub** | Fornecer respostas fixas para dependÃªncias |
| **Fake** | ImplementaÃ§Ã£o simplificada (ex: `RepositorioChamadoEmMemoria`) |

### 7.3 â€” Cobertura MÃ­nima

| Camada | Cobertura | O que testar |
|--------|:---------:|-------------|
| DomÃ­nio (entidades, VOs) | 95% | Regras de negÃ³cio, validaÃ§Ãµes, invariantes |
| Casos de Uso | 90% | Fluxo principal, alternativos, exceÃ§Ãµes |
| Agentes IA | 80% | Parsing de entrada/saÃ­da, fluxos |
| Infraestrutura | 70% | IntegraÃ§Ã£o real com banco, API |
| CLI (E2E) | 60% | Comandos completos, fluxo ponta a ponta |

### 7.4 â€” ConvenÃ§Ãµes

- Nomes: `test_<funcao>_<cenario>` â€” ex: `test_iniciar_chamado_com_sucesso()`
- Classes de teste: `Test<NomeClasse>` â€” ex: `class TestServicoChamado`
- Fixtures no arquivo `conftest.py` do mÃ³dulo
- Testes unitÃ¡rios sem acesso a banco, rede ou sistema de arquivos

### 7.5 â€” Estrutura de Testes

```
tests/
â”œâ”€â”€ unitario/
â”‚   â””â”€â”€ contexto/
â”‚       â”œâ”€â”€ acompanhamento/
â”‚       â”‚   â”œâ”€â”€ test_iniciar_chamado.py
â”‚       â”‚   â”œâ”€â”€ test_finalizar_chamado.py
â”‚       â”‚   â””â”€â”€ ...
â”‚       â”œâ”€â”€ audio/
â”‚       â””â”€â”€ ...
â”œâ”€â”€ integracao/
â”‚   â”œâ”€â”€ persistencia/
â”‚   â””â”€â”€ ipc/
â””â”€â”€ e2e/
    â””â”€â”€ fluxos/
```

---

## 8. InjeÃ§Ã£o de DependÃªncia

### 8.1 â€” Composition Root

Ãšnico local no sistema onde as dependÃªncias sÃ£o resolvidas e injetadas.

**LocalizaÃ§Ã£o:** `src/hermes/_app.py`

### 8.2 â€” Lifetime

| Lifetime | Uso | Exemplo |
|----------|-----|---------|
| **Singleton** | Uma instÃ¢ncia para toda a vida do processo | Pool de conexÃ£o DB, config, Event Bus |
| **Escopo** | Uma instÃ¢ncia por requisiÃ§Ã£o CLI | Unit of Work, repositÃ³rios |
| **Transiente** | Nova instÃ¢ncia a cada injeÃ§Ã£o | Casos de uso, validadores |

### 8.3 â€” MÃ³dulos de DI

Cada bounded context expÃµe um mÃ³dulo de DI com suas dependÃªncias:

```python
# contexto/acompanhamento/di.py
def registrar_modulo(container: Container) -> None:
    container.register(IRepositorioChamado, RepositorioChamadoPostgres)
    container.register(IniciarChamado, IniciarChamado)
    container.register(FinalizarChamado, FinalizarChamado)
```

### 8.4 â€” ProibiÃ§Ãµes

- Service Locator proibido
- InjeÃ§Ã£o manual de dependÃªncias proibida (exceto em testes)
- DependÃªncia cÃ­clica proibida (detectar em tempo de inicializaÃ§Ã£o)

---

## 9. Pipeline de Qualidade

### 9.1 â€” Gatilhos

| Evento | AÃ§Ãµes |
|--------|-------|
| **Push para `main`** | lint â†’ typecheck â†’ unit â†’ integration â†’ e2e |
| **Pull Request** | lint â†’ typecheck â†’ unit |
| **DiÃ¡rio (agendado)** | e2e completo + relatÃ³rio de cobertura |

### 9.2 â€” EstÃ¡gios

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”
â”‚  lint  â”‚ â†’ â”‚ typecheck â”‚ â†’ â”‚ unit â”‚ â†’ â”‚ integration â”‚ â†’ â”‚ e2e â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”˜
```

### 9.3 â€” CritÃ©rios de AprovaÃ§Ã£o

| EstÃ¡gio | CritÃ©rio | Tempo MÃ¡ximo |
|---------|----------|:------------:|
| lint | Zero erros, zero warnings | 30s |
| typecheck | Zero erros mypy strict | 60s |
| unit | 100% passou, cobertura >= 80% | 2min |
| integration | 100% passou | 5min |
| e2e | 100% passou | 10min |

---

## 10. DependÃªncias do Projeto

> **DI:** O projeto usa Composition Root manual (sem framework), conforme [[04-Arquitetura/ADRs.md|ADR-013]].

### 10.1 â€” ProduÃ§Ã£o

| Pacote | VersÃ£o | Motivo |
|--------|--------|--------|
| `typer` | >=0.12 | CLI principal |
| `rich` | >=13 | Terminal formatado |
| `pydantic` | >=2 | Settings, validaÃ§Ã£o, schemas |
| `sqlalchemy` | >=2 | ORM PostgreSQL (assÃ­ncrono) |
| `asyncpg` | >=0.29 | Driver PostgreSQL assÃ­ncrono |
| `redis` | >=5 | Cache e pub/sub |
| `anthropic` | >=0.30 | API Claude |
| `openai` | >=1 | API Whisper |
| `httpx` | >=0.27 | HTTP client assÃ­ncrono |
| `structlog` | >=24 | Logging estruturado |

### 10.2 â€” Desenvolvimento

| Pacote | VersÃ£o | Motivo |
|--------|--------|--------|
| `ruff` | >=0.5 | Linter + formatador |
| `mypy` | >=1.10 | Type checker |
| `pytest` | >=8 | Testes |
| `pytest-asyncio` | >=0.24 | Testes assÃ­ncronos |
| `pytest-cov` | >=5 | Cobertura |
| `pytest-mock` | >=3 | Mocking |
| `factory-boy` | >=3 | Factories para testes |

---

> [[00-Index/SDD-Index.md|Voltar ao Ã­ndice]]

