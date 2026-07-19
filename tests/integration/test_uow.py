import unittest
from src.service_layer import unit_of_work
from tests.conftest import insert_batch, get_allocated_batch_ref, get_session_factory
from src.domain import model


class TestUOW(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.session_factory = get_session_factory()
        return super().setUpClass()

    def setUp(self) -> None:
        self.session = self.session_factory()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.session.close()
        return super().tearDown()

    def test_uow_retrieve_a_batch_and_allocate_to_it(self):
        insert_batch(self.session, 'batch1', 'HIPSTER-WORKBENCH',100, None)
        self.session.commit()

        uow = unit_of_work.SqlAlchemyUnitOfWork(get_session_factory())
        with uow:
            batch = uow.batches.get(reference='batch1')
            line = model.OrderLine('01','HIPSTER-WORKBENCH',10)
            batch.allocate(line)
            uow.commit()

        batchref = get_allocated_batch_ref(self.session, '01', 'HIPSTER-WORKBENCH')
        self.assertEqual(batchref, 'batch1')