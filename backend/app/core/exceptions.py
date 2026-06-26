class RAGBaseException(Exception):
    pass


class DocumentNotFoundError(RAGBaseException):
    pass


class DocumentParsingError(RAGBaseException):
    pass


class UnsupportedFileTypeError(RAGBaseException):
    pass


class EmbeddingError(RAGBaseException):
    pass


class LLMError(RAGBaseException):
    pass


class VectorStoreError(RAGBaseException):
    pass
