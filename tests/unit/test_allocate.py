import unittest
from src.domain.model import allocate, Batch, OrderLine, OutOfStock
from datetime import date, timedelta

class TestAllocation(unittest.TestCase):

    def test_prefers_current_stock_batches_to_shipment(self):
        
        in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
        shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1))
        line = OrderLine("oref", "RETRO-CLOCK", 20)

        allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(in_stock_batch.available_quantity, 80)
        self.assertEqual(shipment_batch.available_quantity, 100)

    def test_prefers_earlier_batches(self):
        earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=date.today())
        medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=date.today()+timedelta(days=5))
        latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=date.today()+timedelta(weeks=4))

        line = OrderLine("order1", "MINIMALIST-SPOON",10)
        allocate(line, [medium, earliest, latest])

        self.assertEqual(earliest.available_quantity, 90)
        self.assertEqual(medium.available_quantity, 100)
        self.assertEqual(latest.available_quantity, 100)

    def test_returns_allocated_batch_ref(self):
        in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER",100, eta=None)
        shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=date.today()+timedelta(days=1))

        line = OrderLine("oref", "HIGHBROW-POSTER", 10)

        allocation = allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(allocation, in_stock_batch.reference)

    def test_raises_out_of_stock_exception_if_cannot_allocate(self):
        batch = Batch('batch1', 'SMALL-FORK', 10, eta=date.today())
        allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

        with self.assertRaises(OutOfStock):
            allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
