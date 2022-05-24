__all__ = ['tsp_print', 'tsp_assign']


def tsp_print(route: str) -> str:
    return fr'^print\({route}\)$'


def tsp_assign(route: str) -> str:
    return fr'^{route}\s*\=\s*(.+)$'
