import unittest
from fastapi.testclient import TestClient
from src.entrypoints.fastapi_app import app
from sqlalchemy import text
from tests.e2e.helper_functions import get_session, add_stock, random_oderid, random_sku, random_batchref, added_skus, added_batches

class TestApi(unittest.TestCase):
    # ======================== set up =========================

    def setUp(self):
        super().setUp()
        self.session = get_session()
        self.client: TestClient = TestClient(app=app)

    def tearDown(self):
        for batch_id in added_batches:
            self.session.execute(text("DELETE FROM allocations WHERE batch_id = :bid"),{"bid": batch_id})
            self.session.execute(text("DELETE FROM batches WHERE id= :bid"), {"bid": batch_id})

        for sku in added_skus:
            self.session.execute(text("DELETE FROM order_lines WHERE sku = :sku"), {"sku": sku})

        self.session.commit()
        super().tearDown()

    # ========================= Tests ==========================
    def test_api_returns_allocation(self):
        sku, othersku = random_sku(), random_sku('other')
        earlybatch = random_batchref("1")
        laterbatch = random_batchref("2")
        otherbatch = random_batchref("3")


        add_stock([
            (earlybatch, sku, 100, '2011-01-01'),
            (laterbatch, sku, 100, '2011-01-02'),
            (otherbatch, othersku, 100, None)
            ])
        orderid = random_oderid()

        response  = self.client.post(
                "/allocate",
                json={
                    "orderid": orderid,
                    "sku": sku,
                    "qty": 10
                    }
                )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["batchref"], earlybatch)

    def test_allocations_are_persisted(self):
        sku = random_sku()
        batch1, batch2 = random_batchref("1"), random_batchref("2")
        order1, order2 = random_oderid("1"), random_oderid("2")

        add_stock([
            (batch1, sku, 10, '2011-01-01'),
            (batch2, sku, 10, '2011-01-02')
            ])
        line1 = {'orderid': order1, 'sku': sku, 'qty': 10}
        line2 = {'orderid': order2, 'sku': sku, 'qty': 10}
        
        # first order uses up all stock in batch1
        response = self.client.post(
                "/allocate",
                json=line1
                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['batchref'], batch1)

        # second order should go to batch2
        response = self.client.post(
                "/allocate",
                json=line2
                )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['batchref'], batch2)


    def test_400_message_for_out_of_stock(self) -> None:

        sku, small_batch, large_order = random_sku(), random_batchref(), random_oderid()
        add_stock([
            (small_batch, sku, 10, '2011-01-01'),
            ])
        data = {'orderid': large_order, 'sku': sku, 'qty': 20}

        response = self.client.post(
                "/allocate",
                json=data
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], f'{sku} is out of stock')


    def test_400_message_for_invalid_sku(self):
        unknown_sku, orderid = random_sku(), random_oderid()
        data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}
        response = self.client.post(
                "/allocate",
                json=data
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], f'Invalid sku {unknown_sku}')

