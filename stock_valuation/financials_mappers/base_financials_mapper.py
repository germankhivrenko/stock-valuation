import pandas as pd
from abc import ABC, abstractmethod


class BaseFinancialsMapper(ABC):
    @abstractmethod
    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        ...

    def __add__(self, other: "BaseFinancialsMapper"):
        return _Sum(self, other)

    def __sub__(self, other: "BaseFinancialsMapper"):
        return _Diff(self, other)


class _BinOp(BaseFinancialsMapper):
    def __init__(self, left: BaseFinancialsMapper, right: BaseFinancialsMapper) -> None:
        self._left = left
        self._right = right


class _Sum(_BinOp):
    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        return self._left.map(financials) + self._right.map(financials)


class _Diff(_BinOp):
    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        return self._left.map(financials) - self._right.map(financials)
