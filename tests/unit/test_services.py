from src.domain.model import OrderLine, Batch
from src.adapters.repository import FakeRepository
from src.service_layer import services
import unittest

class FakeSession():
    committed = False

    def commit(self):
        self.committed = True

class TestServices(unittest.TestCase):

    def test_returns_allocation(self):
        line: OrderLine = OrderLine("01", "COMPLICATED-LAMP", 10)
        batch: Batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
        repo = FakeRepository([batch])
        result = services.allocate(line.orderid,line.sku, line.qty, repo, FakeSession())
        
        self.assertEqual(result,"b1")


    def test_error_for_invalid_sku(self):

        line = OrderLine("01", "NONEEXISTINGSKU",10)
        batch = Batch("b1", "AREALSKU", 100, eta=None)
        repo = FakeRepository([batch])

        with self.assertRaises(services.InvalidSku):
            services.allocate(line.orderid, line.sku, line.qty, repo, FakeSession())

    def tesf_commits(self):
        line = OrderLine("01", "OMINOUS-MIRROR",10)
        batch = Batch("b1","OMINOUS-MIRROR", 100, eta=None)
        repo = FakeRepository([batch])

        session = FakeSession()

        services.allocate(line.orderid, line.sku, line.qty, repo, session)
        self.assertTrue(session.committed)

