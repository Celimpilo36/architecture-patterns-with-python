from src.domain import model
from src.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    def __init__(self, sku: str) -> None:
        self.sku = sku
        super().__init__(f" Invalid sku {sku}")


def is_invalid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(order_id: str, sku: str, qty: int, repo: AbstractRepository, session)-> str:
    batches = repo.list()
    if not is_invalid_sku(sku, batches):
        raise InvalidSku(sku)

    batchref: str = model.allocate(model.OrderLine(orderid=order_id, sku=sku, qty=qty), batches)
    session.commit()
    return batchref
