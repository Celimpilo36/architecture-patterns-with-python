from src.domain.model import OrderLine, Batch
from src.adapters.repository import FakeRepository
from src.service_layer import services
import unittest

class Fake_Repository(set):

    @staticmethod
    def for_batch(ref: str, sku: str, qty: int, eta=None):
        return FakeRepository([Batch(ref,sku,qty,eta)])
class FakeSession():
    committed = False

    def commit(self):
        self.committed = True

class TestServices(unittest.TestCase):

    def test_returns_allocation(self):
       
        repo = Fake_Repository.for_batch("b1", "COMPLICATED-LAMP", 100, eta=None)
        result: str = services.allocate("01", "COMPLICATED-LAMP", 10, repo, FakeSession())
        
        self.assertEqual(result,"b1")


    def test_error_for_invalid_sku(self):

        repo = Fake_Repository.for_batch("b1", "AREALSKU", 100, eta=None)

        with self.assertRaises(services.InvalidSku):
            services.allocate("01", "NONEEXISTINGSKU",10, repo, FakeSession())

    def tesf_commits(self):
        
        repo = Fake_Repository.for_batch("b1","OMINOUS-MIRROR", 100, eta=None)

        session = FakeSession()

        services.allocate("01", "OMINOUS-MIRROR", 10, repo, session)
        self.assertTrue(session.committed)

