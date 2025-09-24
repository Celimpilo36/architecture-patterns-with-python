from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
            self, ref: str, sku: str, qty: int, eta: Optional[date]
            ) -> None:
        self.reference: str = ref
        self.sku: str = sku
        self.eta: date | None = eta
        self.available_quantity: int = qty

    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty
