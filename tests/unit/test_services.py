from src.adapters.repository import FakeRepository
from src.service_layer import services
from src.service_layer import unit_of_work
import unittest

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self) -> None:
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class TestUOW(unittest.TestCase):

    def test_add_batch(self):
        uow = FakeUnitOfWork()

        services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)

        self.assertNotEqual(uow.batches.get("b1"), None)
        self.assertTrue(uow.committed)

    def test_allocate_returns_allocation(self):
        uow = FakeUnitOfWork()
        services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
        result = services.allocate("01", "COMPLICATED-LAMP", 18, uow)
        self.assertEqual(result, "batch1")

