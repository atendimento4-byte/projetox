from __future__ import annotations

import hashlib
import json
from dataclasses import asdict

import structlog

from projetox.compartilhado.cache import CacheMemoria
from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.llm.dominio.interfaces import IExtratorLLM

logger = structlog.get_logger(__name__)


class ServicoLLM:
    def __init__(
        self,
        extrator: IExtratorLLM,
        cache: CacheMemoria | None = None,
    ) -> None:
        self._extrator = extrator
        self._cache = cache
        self._ultimo_cache_hit = False

    @property
    def ultimo_cache_hit(self) -> bool:
        return self._ultimo_cache_hit

    def resumir(self, transcricao: str) -> Resultado[ResumoAtendimento, ErroAplicacao]:
        if not transcricao.strip():
            return Resultado.falha_com_erro(
                ErroAplicacao(mensagem="Transcricao vazia para gerar resumo"),
            )

        chave: str | None = None
        if self._cache is not None:
            chave = hashlib.sha256(transcricao.encode()).hexdigest()
            armazenado = self._cache.obter(chave)
            if armazenado is not None:
                self._ultimo_cache_hit = True
                logger.info("cache_hit", chave=chave[:8])
                dados = json.loads(armazenado)
                return Resultado.sucesso(ResumoAtendimento(**dados))
            self._ultimo_cache_hit = False
            logger.info("cache_miss", chave=chave[:8])

        resultado = self._extrator.extrair_resumo(transcricao)

        if self._cache is not None and resultado.ok() and chave is not None:
            armazenar = json.dumps(asdict(resultado.valor), ensure_ascii=False)
            self._cache.definir(chave, armazenar)

        return resultado
