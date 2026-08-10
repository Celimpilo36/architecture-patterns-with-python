import unittest
from src.service_layer import unit_of_work
from tests.conftest import insert_batch, get_allocated_batch_ref, get_session_factory
from src.domain import model
from sqlalchemy import text


class TestUOW(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.session_factory = get_session_factory()
        return super().setUpClass()

    def setUp(self) -> None:
        self.session = self.session_factory()
        return super().setUp()
    

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

    def test_rolls_back_uncommitted_work_by_defaulf(self):
        uow = unit_of_work.SqlAlchemyUnitOfWork(get_session_factory())

        with uow:
            insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

        new_session = get_session_factory()
        rows = list(new_session().execute(text('SELECT * FROM "bathces"')))
        self.assertTrue(rows, [])


    def test_rolls_back_on_error(self):
        class MyException(Exception):
            pass
        uow = unit_of_work.SqlAlchemyUnitOfWork(get_session_factory())
        with self.assertRaises(MyException):
            with uow:
                insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
                self.assertRaises(MyException)

        new_session = get_session_factory()
        rows = list(new_session().execute(text('SELECT * FROM "batches"')))
        self.assertEqual(rows, [])