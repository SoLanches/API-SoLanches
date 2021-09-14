class SolanchesException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class SolanchesComercioNaoEncontrado(SolanchesException):
    def __init__(self, message):
        super().__init__(message)


class SolanchesDuplicateKey(SolanchesException):
    def __init__(self, message):
        super().__init__(message)


class SolanchesProdutoNaoEncontrado(SolanchesException):
    def __init__(self, message):
        super().__init__(message)

class SolanchesProdutoNaoEstaNoCardapio(SolanchesException):
    def __init__(self, message):
        super().__init__(message)

class SolanchesProdutoEstaNosDestaques(SolanchesException):
    def __init__(self, message):
        super().__init__(message)
