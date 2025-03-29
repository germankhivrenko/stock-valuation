import pandas as pd
from collections.abc import Sequence

from stock_valuation.financials_mappers.base_financials_mapper import BaseFinancialsMapper


class RowFinancialsMapper(BaseFinancialsMapper):
    def __init__(self, src_keys: Sequence[str]) -> None:
        self._src_keys = src_keys

    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        for key in self._src_keys:
            if key in financials.index:
                return financials.loc[[key]].reset_index(drop=True).astype(int)
        raise Exception("Key not found")  # TODO: specific error
