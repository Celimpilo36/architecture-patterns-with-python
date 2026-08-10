from src.domain import model
from typing import Optional
from datetime import date

from src.service_layer import unit_of_work


class InvalidSku(Exception):
    def __init__(self, sku: str) -> None:
        self.sku = sku
        super().__init__(f" Invalid sku {sku}")


def is_invalid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
        ref:str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork
              ) -> None:
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:

    line = model.OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()

        if not is_invalid_sku(sku, batches):
            raise InvalidSku(sku)
        
        batchref = model.allocate(line, batches)
        uow.commit()
        return batchref