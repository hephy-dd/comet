__all__ = ["tsp_print", "tsp_assign"]


def tsp_print(route: str) -> str:
    return rf"^print\({route}\)$"


def tsp_assign(route: str) -> str:
    return rf"^{route}\s*\=\s*(.+)$"


class Error:
    """Generic error message container."""

    def __init__(self, code: int, message: str) -> None:
        self.code: int = code
        self.message: str = message
