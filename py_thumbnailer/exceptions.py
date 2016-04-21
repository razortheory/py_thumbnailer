class PyThumbnailerException(Exception):
    pass


class MimeTypeNotFoundException(PyThumbnailerException):
    pass


class ThumbnailerNotFoundException(PyThumbnailerException):
    pass


class ThumbnailerNotReadyException(PyThumbnailerException):
    pass
