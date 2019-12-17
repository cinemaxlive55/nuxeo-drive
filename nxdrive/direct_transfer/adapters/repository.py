import abc
from typing import Set

from ..adapters import orm
from ..domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[model.Transfer] = set()

    def add(self, transfer: model.Transfer):
        self._add(transfer)
        self.seen.add(transfer)

    def get(self, uid) -> model.Transfer:
        transfer = self._get(uid)
        if transfer:
            self.seen.add(transfer)
        return transfer

    def get_by_batchref(self, batchref) -> model.Transfer:
        transfer = self._get_by_batchref(batchref)
        if transfer:
            self.seen.add(transfer)
        return transfer

    @abc.abstractmethod
    def _add(self, transfer: model.Transfer):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, uid) -> model.Transfer:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> model.Transfer:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, transfer):
        self.session.add(transfer)

    def _get(self, uid: int):
        return self.session.query(model.Transfer).filter_by(uid=uid).first()

    def _get_by_batchref(self, batchref):
        return (
            self.session.query(model.Transfer)
            .join(model.Batch)
            .filter(orm.batches.c.reference == batchref,)
            .first()
        )
