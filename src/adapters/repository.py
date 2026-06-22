import abc
from src.domain.model import Batch
from sqlalchemy.orm import Session
from typing import List


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError
    
    @abc.abstractmethod
    def list(self) -> list[Batch]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> list[Batch]:
        return self.session.query(Batch).all()


class FakeRepository(AbstractRepository):

    def __init__(self, batches) -> None:
        self._batches: set[Batch] = set(batches)

    def add(self, batch) -> None:
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
