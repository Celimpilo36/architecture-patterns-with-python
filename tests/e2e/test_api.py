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
    def test_happy_path_returns_201_and_allocated_batch(self):
        sku, othersku = random_sku(), random_sku('other')
        earlybatch = random_batchref("1")
        laterbatch = random_batchref("2")
        otherbatch = random_batchref("3")


        add_stock([
            (earlybatch, sku, 100, '2011-01-01'),
            (laterbatch, sku, 100, '2011-01-02'),
            (otherbatch, othersku, 100, None)
            ])
        payload = {'orderid': random_oderid(), 'sku': sku, 'qty': 3}

        response  = self.client.post(
                "/allocate",
                json=payload
                )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["batch_ref"], earlybatch)

    def test_unhappy_path_returns_400_and_error_message(self):
        unknown_sku, orderid = random_sku(), random_oderid()
        payload = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}
        response = self.client.post(
                "/allocate",
                json=payload
                )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(f'Invalid sku {unknown_sku}' in response.json()["detail"])



