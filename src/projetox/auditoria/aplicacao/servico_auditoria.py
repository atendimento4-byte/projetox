from projetox.auditoria.dominio.entidades import RegistroAuditoria
from projetox.auditoria.infra.repositorio_memoria import (
    RepositorioAuditoriaMemoria,
)


class ServicoAuditoria:
    _instancia: "ServicoAuditoria | None" = None

    def __new__(cls) -> "ServicoAuditoria":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.repo = RepositorioAuditoriaMemoria()
        return cls._instancia

    def registrar_acao(
        self,
        tipo: str,
        sessao_id: str | None = None,
        detalhes: dict | None = None,
    ) -> None:
        registro = RegistroAuditoria(
            acao=tipo,
            usuario="sistema",
            sessao_id=sessao_id,
            detalhes=detalhes or {},
        )
        self.repo.registrar(registro)

    def listar(self, limite: int = 50) -> list[RegistroAuditoria]:
        return self.repo.listar(limite=limite)
