from dataclasses import dataclass

__all__ = ["tsp_print", "tsp_assign"]


def tsp_print(route: str) -> str:
    return rf"^print\({route}\)$"


def tsp_assign(route: str) -> str:
    return rf"^{route}\s*\=\s*(.+)$"


@dataclass
class Error:
    """Generic error message container."""
    code: int
    message: str
