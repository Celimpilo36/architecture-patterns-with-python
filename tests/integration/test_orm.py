import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, clear_mappers
from src.adapters.orm import start_mapper, metadata
from src.domain.model import OrderLine

class TestOrm(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        start_mapper()

    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", echo=True)
        metadata.create_all(bind=self.engine)
        self.session = Session(self.engine)
    
    def tearDown(self) -> None:
        self.session.close()
        metadata.drop_all(self.engine)
        self.engine.dispose()

    @classmethod
    def tearDownClass(cls) -> None:
        clear_mappers()

    def test_orderline_mapper_can_load_line(self):
        order1 = OrderLine("order1","RED-CHAIR",12)
        order2 = OrderLine("order1","RED-TABLE",13)
        order3 = OrderLine("order2","BLUE-LIPSTICK",14)
        self.session.add(order1)
        self.session.add(order2)
        self.session.add(order3)
        self.session.commit()

        expected = [
            OrderLine("order1","RED-CHAIR",12),
            OrderLine("order1","RED-TABLE", 13),
            OrderLine("order2","BLUE-LIPSTICK", 14)
        ]

        self.assertEqual(self.session.query(OrderLine).all(), expected)

    def test_orderline_mapper_can_save_line(self):
        new_line = OrderLine("order1", "DECORATIVE-WIDGET", 12)
        self.session.add(new_line)
        self.session.commit()

        rows = list(self.session.execute(text('SELECT orderid, sku, qty FROM order_lines')))
        self.assertEqual(rows, [("order1", "DECORATIVE-WIDGET", 12)])
