from model import Batch, OrderLine
from datetime import date


def test_allocation_to_a_batch_reduces_the_available_quantity() -> None:
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


test_allocation_to_a_batch_reduces_the_available_quantity()
