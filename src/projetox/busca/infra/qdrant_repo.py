"""Repositorio de busca usando Qdrant."""
from __future__ import annotations

from uuid import NAMESPACE_DNS, uuid4, uuid5

import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from projetox.busca.dominio.interfaces import DocumentoBusca, IRepositorioBusca
from projetox.compartilhado.erros import ErroInfraestrutura, Resultado

logger = structlog.get_logger(__name__)

_COLECAO = "projetox_atendimentos"
_VECTOR_SIZE = 1536


def _string_para_uuid(id_str: str) -> str:
    """Converte uma string qualquer em UUID para uso como point ID."""
    return str(uuid5(NAMESPACE_DNS, id_str))


class QdrantRepositorioBusca(IRepositorioBusca):
    def __init__(self, host: str = "localhost", port: int = 6333) -> None:
        self._cliente = AsyncQdrantClient(host=host, port=port)

    async def _garantir_colecao(self) -> None:
        colecoes = await self._cliente.get_collections()
        nomes = {c.name for c in colecoes.collections}
        if _COLECAO not in nomes:
            await self._cliente.create_collection(
                collection_name=_COLECAO,
                vectors_config=VectorParams(
                    size=_VECTOR_SIZE,
                    distance=Distance.COSINE,
                    on_disk=True,
                ),
            )
            logger.info("colecao_criada", colecao=_COLECAO)

    async def indexar(
        self, docs: list[DocumentoBusca], embeddings: list[list[float]],
    ) -> Resultado[int, ErroInfraestrutura]:
        if len(docs) != len(embeddings):
            msg = f"Quantidade de docs ({len(docs)}) difere de embeddings ({len(embeddings)})"
            return Resultado.falha_com_erro(ErroInfraestrutura(mensagem=msg))

        try:
            await self._garantir_colecao()

            pontos = [
                PointStruct(
                    id=_string_para_uuid(doc.id) if doc.id else str(uuid4()),
                    vector=emb,
                    payload={
                        "texto_original": doc.texto,
                        **doc.metadados,
                    },
                )
                for doc, emb in zip(docs, embeddings, strict=True)
            ]

            await self._cliente.upsert(
                collection_name=_COLECAO,
                points=pontos,
                wait=True,
            )
            logger.info("documentos_indexados", quantidade=len(pontos))
            return Resultado.sucesso(len(pontos))
        except Exception as exc:
            return Resultado.falha_com_erro(
                ErroInfraestrutura(mensagem=f"Erro ao indexar documentos: {exc}", causa=exc),
            )

    async def buscar(self, vetor_consulta: list[float], limite: int = 5) -> list[DocumentoBusca]:
        try:
            await self._garantir_colecao()

            resposta = await self._cliente.query_points(
                collection_name=_COLECAO,
                query=vetor_consulta,
                limit=limite,
                with_payload=True,
            )

            return [
                DocumentoBusca(
                    id=str(ponto.id),
                    texto=ponto.payload.get("texto_original", ""),
                    metadados={k: v for k, v in ponto.payload.items() if k != "texto_original"},
                    pontuacao=ponto.score,
                )
                for ponto in resposta.points
            ]
        except Exception as exc:
            logger.exception("erro_busca", erro=str(exc))
            return []

    async def remover(self, id: str) -> bool:
        try:
            await self._cliente.delete(
                collection_name=_COLECAO,
                points_selector=[_string_para_uuid(id)],
                wait=True,
            )
        except Exception as exc:
            logger.exception("erro_remover", id=id, erro=str(exc))
            return False
        else:
            return True

    async def limpar(self) -> None:
        try:
            await self._cliente.delete_collection(collection_name=_COLECAO)
            logger.info("colecao_removida", colecao=_COLECAO)
        except Exception as exc:
            logger.exception("erro_limpar", erro=str(exc))
