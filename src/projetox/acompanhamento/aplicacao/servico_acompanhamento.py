from projetox.acompanhamento.dominio.entidades import SessaoAcompanhamento
from projetox.acompanhamento.dominio.interfaces_repositorio import (
    IRepositorioSessao,
)


class ServicoAcompanhamento:
    def __init__(self, repo: IRepositorioSessao) -> None:
        self.repo = repo

    async def iniciar(
        self,
        chamado: str,
        cliente: str,
        tecnico: str,
        tipo: str,
    ) -> SessaoAcompanhamento:
        ativa = await self.repo.obter_ativa()
        if ativa is not None:
            await self.repo.finalizar(ativa.id)

        sessao = SessaoAcompanhamento(
            chamado=chamado,
            cliente=cliente,
            tecnico=tecnico,
            tipo=tipo,
        )
        return await self.repo.criar(sessao)

    async def finalizar(self) -> SessaoAcompanhamento | None:
        ativa = await self.repo.obter_ativa()
        if ativa is None:
            return None
        return await self.repo.finalizar(ativa.id)

    async def status(self) -> SessaoAcompanhamento | None:
        return await self.repo.obter_ativa()
