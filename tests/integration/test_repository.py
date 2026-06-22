import unittest
from src.domain.model import Batch, OrderLine
from src.adapters import orm, repository
from sqlalchemy.orm import Session, clear_mappers
from sqlalchemy import create_engine, text
from typing import List


class TestRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        orm.start_mapper()

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", echo=True)
        self.metadata = orm.metadata
        self.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.metadata.drop_all(self.engine)
        self.engine.dispose()

    @classmethod
    def tearDownClass(cls):
        clear_mappers()


    def test_repository_can_save_a_batch(self):

        batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

        repo = repository.SqlAlchemyRepository(self.session)
        repo.add(batch)
        self.session.commit()

        rows = list(
                self.session.execute(
                    text('SELECT reference, sku, _purchased_qty, eta From "batches"')
                    )
                )
        self.assertEqual(rows, [("batch1", "RUSTY-SOAPDISH",100, None)])

    def insert_order_line(self):
        order_line = OrderLine("order1", "GENERIC-SOFA", 12)
        self.session.add(order_line)
        self.session.commit()

        [[orderline_id]] = self.session.execute(
                text('SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku'), dict(orderid="order1", sku="GENERIC-SOFA")
                )
        return orderline_id

    def insert_batch(self, batch_id: str):
        batch = Batch(batch_id, "GENERIC-SOFA", 100, None)
        self.session.add(batch)
        self.session.commit()

        [[batches_id]] = self.session.execute(
                text('SELECT id FROM batches WHERE reference=:reference AND sku=:sku'),
                dict(reference= batch_id, sku= "GENERIC-SOFA")
                )
        return batches_id

    def insert_allocations(self, batch_id, orderline_id):
        self.session.execute(
                text('INSERT INTO allocations (batch_id, orderline_id) VALUES (:batch_id, :orderline_id)'),
                dict(batch_id=batch_id, orderline_id=orderline_id)
                )
        self.session.commit()

    def test_repository_can_retrieve_a_batch_with_allocations(self):
        orderline_id = self.insert_order_line()
        batch_id = self.insert_batch("batch1")
        self.insert_batch("batch2")
        self.insert_allocations(batch_id, orderline_id)

        repo = repository.SqlAlchemyRepository(self.session)
        retrieved: List[Batch] = [repo.get("batch1")]

        expected: List[Batch] = [Batch("batch1", "GENERIC-SOFA", 100, eta=None)]
        self.assertEqual(retrieved, expected)
        self.assertEqual(retrieved[0].sku, expected[0].sku)
        self.assertEqual(retrieved[0]._purchased_qty, expected[0]._purchased_qty)
        self.assertEqual(retrieved[0]._allocations, {OrderLine("order1","GENERIC-SOFA",12),})
