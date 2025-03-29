import pytest
import pandas as pd
from tests.unit.data.path import UNIT_TESTS_DATA_PATH
from stock_valuation.constants.financial_keys import REVENUE
from stock_valuation.constants.financial_keys import COST_OF_REVENUE
from stock_valuation.constants.financial_keys import OPERATING_EXPENSE
from stock_valuation.constants.financial_keys import DEPRECIATION
from stock_valuation.constants.financial_keys import PROVISION_FOR_TAXES
from stock_valuation.constants.financial_keys import CAPITAL_EXPENDITURE
from stock_valuation.constants.financial_keys import WORKING_CAPITAL

@pytest.fixture
def raw_financials():  # TODO: rename to raw_fin..
    return (
        pd
            .read_csv(UNIT_TESTS_DATA_PATH / "uber_tenk_financials.csv", index_col=0)
            .rename_axis("concept")
            .fillna(0)
            .astype(int)
    )

@pytest.fixture
def dcf_financials():
    return pd.DataFrame({
        "2020": [11139000000,  5154000000, 10848000000,         0,  -192000000, -616000000, 3017000000],
        "2021": [17455000000,  9351000000, 11938000000,         0,  -492000000, -298000000, -205000000],
        "2022": [31877000000, 19659000000, 14050000000,         0,  -181000000, -252000000,  396000000],
        "2023": [37281000000, 22457000000, 13714000000,         0,  -213000000, -223000000, 1843000000],
        "2024": [43978000000, 26651000000, 14528000000, -71100000, -5800000000, -242000000,  769000000]
    }, index=[
        REVENUE,
        COST_OF_REVENUE,
        OPERATING_EXPENSE,
        DEPRECIATION,
        PROVISION_FOR_TAXES,
        CAPITAL_EXPENDITURE,
        WORKING_CAPITAL,
    ])
