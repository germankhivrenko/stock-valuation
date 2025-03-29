import pandas as pd
from stock_valuation.financials_mappers.base_financials_mapper import BaseFinancialsMapper


class CompositeFinancialsMapper(BaseFinancialsMapper):
    def __init__(self, config: dict[str, BaseFinancialsMapper]) -> None:
        self._config = config

    def map(self, financials: pd.DataFrame) -> pd.DataFrame:
        result = pd.concat(
            (mapper.map(financials).rename(index={0: key}) for key, mapper in self._config.items()),
        )
        result.index.name = None
        return result
