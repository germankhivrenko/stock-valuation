import numpy as np
import pandas as pd
from stock_valuation.financials_forecasters.financials_forecaster import FinancialsForecaster
from stock_valuation.financials_forecasters.forecast_methods.recent_forecast_method import RecentForecastMethod
from stock_valuation.financials_forecasters.forecast_methods.average_forecast_method import AverageForecastMethod
from stock_valuation.financials_forecasters.forecast_methods.cagr_forecast_method import CAGRForecastMethod
from stock_valuation.financials_forecasters.forecast_methods.poly_fit_forecast_method import PolyFitForecastMethod
from stock_valuation.financials_forecasters.forecast_methods.percentage_of_forecast_method import PercentageOfForecastMethod
from stock_valuation.constants.financial_keys import REVENUE
from stock_valuation.constants.financial_keys import COST_OF_REVENUE
from stock_valuation.constants.financial_keys import OPERATING_EXPENSE
from stock_valuation.constants.financial_keys import DEPRECIATION
from stock_valuation.constants.financial_keys import PROVISION_FOR_TAXES
from stock_valuation.constants.financial_keys import CAPITAL_EXPENDITURE
from stock_valuation.constants.financial_keys import WORKING_CAPITAL
from tests.unit.fixtures import dcf_financials


def test_forecast(dcf_financials):
    revenue = PolyFitForecastMethod(REVENUE)

    forecaster = FinancialsForecaster(dcf_financials, {
        REVENUE: revenue,
        COST_OF_REVENUE: PercentageOfForecastMethod(revenue, 0.7),
        OPERATING_EXPENSE: CAGRForecastMethod(OPERATING_EXPENSE),
        DEPRECIATION: AverageForecastMethod(DEPRECIATION),
        PROVISION_FOR_TAXES: -PercentageOfForecastMethod(revenue, 0.1),
        CAPITAL_EXPENDITURE: RecentForecastMethod(CAPITAL_EXPENDITURE),
        WORKING_CAPITAL: RecentForecastMethod(WORKING_CAPITAL),
    })

    forecaster.forecast_next()
    forecasted = forecaster.get_forecasted()

    slope, intercept = np.polyfit([i for i in range(len(dcf_financials.loc[REVENUE]))], dcf_financials.loc[REVENUE], 1)
    expected_revenue = slope * len(dcf_financials.loc[REVENUE]) + intercept

    first = dcf_financials.loc[OPERATING_EXPENSE].iloc[0]
    last = dcf_financials.loc[OPERATING_EXPENSE].iloc[-1]
    periods = len(dcf_financials.loc[OPERATING_EXPENSE]) - 1
    expected_operating_expense = last * ((last / first) ** (1 / periods))

    expected = pd.DataFrame({
        "2025": [
            expected_revenue,
            expected_revenue * 0.7,
            expected_operating_expense,
            dcf_financials.loc[DEPRECIATION].mean(),
            -expected_revenue * 0.1,
            dcf_financials.loc[CAPITAL_EXPENDITURE].iloc[-1],
            dcf_financials.loc[WORKING_CAPITAL].iloc[-1],
        ],
    }, index=[
        REVENUE,
        COST_OF_REVENUE,
        OPERATING_EXPENSE,
        DEPRECIATION,
        PROVISION_FOR_TAXES,
        CAPITAL_EXPENDITURE,
        WORKING_CAPITAL,
    ])
    pd.testing.assert_frame_equal(forecasted, expected)
