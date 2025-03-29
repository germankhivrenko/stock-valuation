
import pandas as pd
from stock_valuation.financials_forecasters.forecast_methods.base_forecast_method import BaseForecastMethod


class FinancialsForecaster:
    def __init__(self, historical: pd.DataFrame, config: dict[str, BaseForecastMethod]) -> None:
        self._historical = historical
        self._combined = historical.copy()
        self._forecasted = pd.DataFrame(index=historical.index)
        self._config = config  # TODO: add validation (check if keys in df match keys in config)

    # TODO: check df.apppy
    def forecast_next(self, periods: int = 1) -> None:
        for _ in range(periods):
            next_period_label = str(int(self._combined.columns[-1]) + 1)  # FIXME: works only for numbers
            next_period_values = []
            for key in self._combined.index:
                method = self._config[key]
                next_period_values.append(method.forecast(self._combined))
            next_period = pd.DataFrame(next_period_values, index=self._combined.index, columns=[next_period_label])

            self._forecasted = pd.concat([self._forecasted, next_period], axis=1)
            self._combined = pd.concat([self._combined, next_period], axis=1)

    def get_forecasted(self) -> pd.DataFrame:
        return self._forecasted

    def get_combined(self) -> pd.DataFrame:
        return self._combined
