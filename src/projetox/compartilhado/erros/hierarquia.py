from __future__ import annotations


class ErroAplicacao(Exception):
    def __init__(self, mensagem: str, causa: Exception | None = None) -> None:
        self.mensagem = mensagem
        self.causa = causa
        super().__init__(mensagem)


class ErroDominio(ErroAplicacao):
    pass


class ErroRegraNegocio(ErroDominio):
    pass


class ErroEntidadeNaoEncontrada(ErroDominio):
    pass


class ErroAplicacaoServico(ErroAplicacao):
    pass


class ErroInfraestrutura(ErroAplicacao):
    pass


class ErroPersistencia(ErroInfraestrutura):
    pass


class ErroComunicacao(ErroInfraestrutura):
    pass


class ErroConfiguracao(ErroInfraestrutura):
    pass


class ErroTranscricao(ErroInfraestrutura):
    pass


class ErroLLM(ErroInfraestrutura):
    pass
