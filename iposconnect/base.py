from abc import ABC, abstractmethod

from ibis import Table, BaseBackend
from pandas import DataFrame


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class BaseTable(ABC):
    def __init__(self, backend: BaseBackend = None, table: Table = None):
        self._backend = backend

        self._is_between = False
        self._start_date = None
        self._end_date = None

        if table is not None:
            self.table = table
            self._backend = table.get_backend()

        if self._backend is None:
            raise Exception("Backend do not exist!")

    @abstractmethod
    def extract(self) -> Table:
        pass

    @abstractmethod
    def transform(self) -> Table:
        pass

    @property
    @singleton
    @abstractmethod
    def load(self) -> Table:
        pass

    def between(self, start: str, end: str):
        self._is_between = True
        self._start_date = start
        self._end_date = end
        return self


class BaseBuilder:
    def __init__(self, table: Table):
        self.table = table

    def load(self) -> Table:
        return self.table


class BaseForcast(ABC):
    def __init__(self, df: DataFrame, target=None):
        self.df = df
        self._target = self.df[target] if target else None
        self._forecaster = None

    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self) -> DataFrame:
        pass

    def prepare(self, target):
        # data transformation
        self.transform()

        # set target
        self._target = self.df[target]

        return self

    @abstractmethod
    def fit(self):
        pass

    def predict(self, step) -> DataFrame:
        return DataFrame(
            data=self._forecaster.predict(steps=step, last_window=None)
        )
