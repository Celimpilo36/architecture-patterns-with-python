from src.domain import model
from src.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_invalid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: OrderLine, repo: AbstractRepository, session)-> str:
    batches = repo.list()
    if not is_invalid_sku(line.sku, batches):
        raise InvalidSku(line.sku, batches)

    batchref: str = model.allocate(line, batches)
    session.commt()
    return batchref
