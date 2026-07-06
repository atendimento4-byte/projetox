from __future__ import annotations

import hashlib
import json
import os
import random
from dataclasses import asdict

import structlog

from projetox.compartilhado.cache import CacheMemoria
from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.llm.dominio.interfaces import IExtratorLLM

logger = structlog.get_logger(__name__)

_VETOR_DIMS = 1536


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

    def resumir(
        self,
        transcricao: str,
        contexto_recuperado: str | None = None,
    ) -> Resultado[ResumoAtendimento, ErroAplicacao]:
        if not transcricao.strip():
            return Resultado.falha_com_erro(
                ErroAplicacao(mensagem="Transcricao vazia para gerar resumo"),
            )

        texto = transcricao
        if contexto_recuperado:
            texto = (
                "## Contexto de atendimentos anteriores\n"
                f"{contexto_recuperado}\n\n{transcricao}"
            )

        chave: str | None = None
        if self._cache is not None:
            chave = hashlib.sha256(texto.encode()).hexdigest()
            armazenado = self._cache.obter(chave)
            if armazenado is not None:
                self._ultimo_cache_hit = True
                logger.info("cache_hit", chave=chave[:8])
                dados = json.loads(armazenado)
                return Resultado.sucesso(ResumoAtendimento(**dados))
            self._ultimo_cache_hit = False
            logger.info("cache_miss", chave=chave[:8])

        resultado = self._extrator.extrair_resumo(texto)

        if self._cache is not None and resultado.ok() and chave is not None:
            armazenar = json.dumps(asdict(resultado.valor), ensure_ascii=False)
            self._cache.definir(chave, armazenar)

        return resultado

    async def gerar_embedding(self, texto: str) -> Resultado[list[float], ErroAplicacao]:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                from openai import AsyncOpenAI  # noqa: PLC0415

                cliente = AsyncOpenAI(api_key=api_key)
                resposta = await cliente.embeddings.create(
                    model="text-embedding-3-small",
                    input=texto,
                )
                return Resultado.sucesso(resposta.data[0].embedding)
            except Exception as exc:
                return Resultado.falha_com_erro(
                    ErroAplicacao(mensagem=f"Erro ao gerar embedding OpenAI: {exc}", causa=exc),
                )

        logger.warning(
            "openai_nao_configurado",
            mensagem="OPENAI_API_KEY nao definida. Usando embedding dummy.",
        )
        vec = [random.gauss(0, 1) for _ in range(_VETOR_DIMS)]
        norma = sum(x * x for x in vec) ** 0.5
        if norma > 0:
            vec = [x / norma for x in vec]
        return Resultado.sucesso(vec)
