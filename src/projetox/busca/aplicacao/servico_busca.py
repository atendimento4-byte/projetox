from __future__ import annotations

from uuid import uuid4

import structlog

from projetox.busca.dominio.interfaces import DocumentoBusca, IRepositorioBusca
from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.aplicacao.servico_llm import ServicoLLM
from projetox.llm.dominio.entidades import ResumoAtendimento

logger = structlog.get_logger(__name__)


class ServicoBusca:
    def __init__(self, repo: IRepositorioBusca, llm: ServicoLLM) -> None:
        self._repo = repo
        self._llm = llm

    async def indexar_atendimento(
        self,
        resumo: ResumoAtendimento,
    ) -> Resultado[int, ErroAplicacao]:
        texto = self._converter_para_texto(resumo)
        metadados = {
            "cliente": resumo.cliente,
            "problema": resumo.problema,
            "solucao": resumo.solucao,
            "tipo_atendimento": resumo.tipo_atendimento,
        }

        resultado_emb = await self._llm.gerar_embedding(texto)
        if resultado_emb.falha():
            return Resultado.falha_com_erro(resultado_emb.erro)

        doc = DocumentoBusca(
            id=str(uuid4()),
            texto=texto,
            metadados=metadados,
        )

        resultado = await self._repo.indexar([doc], [resultado_emb.valor])
        if resultado.falha():
            return Resultado.falha_com_erro(resultado.erro)

        logger.info("atendimento_indexado", cliente=resumo.cliente)
        return resultado

    async def buscar_similares(
        self,
        consulta: str,
        limite: int = 5,
    ) -> list[DocumentoBusca]:
        resultado_emb = await self._llm.gerar_embedding(consulta)
        if resultado_emb.falha():
            logger.error("falha_embedding_busca", erro=resultado_emb.erro.mensagem)
            return []

        return await self._repo.buscar(resultado_emb.valor, limite=limite)

    async def indexar_todos_do_db(self) -> Resultado[int, ErroAplicacao]:
        try:
            from sqlalchemy import select  # noqa: PLC0415

            from projetox.compartilhado.banco.config import get_session  # noqa: PLC0415
            from projetox.compartilhado.banco.modelos import Session  # noqa: PLC0415
        except ImportError as exc:
            return Resultado.falha_com_erro(
                ErroAplicacao(mensagem=f"Erro ao importar modelos do banco: {exc}"),
            )

        total = 0
        async with get_session() as session:
            stmt = select(Session).where(Session.status == "completed")
            resultado = await session.execute(stmt)
            sessoes = resultado.scalars().all()

            logger.info("sessoes_encontradas", quantidade=len(sessoes))

            for sessao in sessoes:
                texto = (
                    f"Atendimento para {sessao.client_name or 'desconhecido'}. "
                    f"Tipo: {sessao.type or 'N/A'}. "
                    f"Ticket: {sessao.ticket_id or 'N/A'}."
                )
                metadados = {
                    "cliente": sessao.client_name or "",
                    "empresa": sessao.client_company or "",
                    "tecnico": sessao.technician or "",
                    "ticket": sessao.ticket_id or "",
                    "tipo": sessao.type or "",
                    "timestamp": sessao.started_at.isoformat() if sessao.started_at else "",
                }

                resultado_emb = await self._llm.gerar_embedding(texto)
                if resultado_emb.falha():
                    logger.warning(
                        "falha_embedding_sessao",
                        sessao_id=str(sessao.id),
                        erro=resultado_emb.erro.mensagem,
                    )
                    continue

                doc = DocumentoBusca(
                    id=str(sessao.id),
                    texto=texto,
                    metadados=metadados,
                )

                resultado_idx = await self._repo.indexar([doc], [resultado_emb.valor])
                if resultado_idx.falha():
                    logger.warning(
                        "falha_indexacao_sessao",
                        sessao_id=str(sessao.id),
                        erro=resultado_idx.erro.mensagem,
                    )
                    continue

                total += 1

        logger.info("indexacao_concluida", total=total)
        return Resultado.sucesso(total)

    @staticmethod
    def _converter_para_texto(resumo: ResumoAtendimento) -> str:
        partes = [
            f"Resumo: {resumo.resumo}",
            f"Problema: {resumo.problema}",
            f"Solucao: {resumo.solucao}",
            f"Cliente: {resumo.cliente}",
            f"Tipo: {resumo.tipo_atendimento}",
            f"Observacoes: {resumo.observacoes}",
        ]
        if resumo.equipamentos:
            partes.append(f"Equipamentos: {', '.join(resumo.equipamentos)}")
        if resumo.acoes_pendentes:
            partes.append(f"Acoes pendentes: {'; '.join(resumo.acoes_pendentes)}")
        return "\n".join(partes)
