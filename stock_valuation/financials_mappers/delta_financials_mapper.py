import pandas as pd
from stock_valuation.financials_mappers.base_financials_mapper import BaseFinancialsMapper


class DeltaFinancialsMapper(BaseFinancialsMapper):
    def __init__(self, reference_mapper: BaseFinancialsMapper) -> None:
        self._reference_mapper = reference_mapper

    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        return self._reference_mapper.map(financials).diff(axis=1)
