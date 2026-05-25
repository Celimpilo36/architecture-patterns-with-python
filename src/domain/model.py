from dataclasses import dataclass
from typing import Optional, List
from datetime import date

@dataclass
class OrderLine:
    orderid: str
    sku: str
    qty: int

    def __eq__(self,other):
        if not isinstance(other, OrderLine):
            return False
        return self.orderid == other.orderid and self.sku == other.sku

    def __hash__(self):
        return hash((self.orderid, self.sku))


class Batch:
    def __init__(self, reference: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine)-> None:
        if line in self._allocations:
            self._allocations.add(line)
    

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
    
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
    
class OutOfStock(Exception):
    def __init__(self, sku):
        self.sku = sku
        super().__init__(f"{self.sku} is out of stock")
    

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
            )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(line.sku)
