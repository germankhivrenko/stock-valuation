import pandas as pd
from stock_valuation.financials_mappers.composite_financials_mapper import CompositeFinancialsMapper
from stock_valuation.financials_mappers.row_financials_mapper import RowFinancialsMapper
from stock_valuation.financials_mappers.delta_financials_mapper import DeltaFinancialsMapper
from tests.unit.fixtures import raw_financials
from stock_valuation.constants.financial_keys import REVENUE
from stock_valuation.constants.financial_keys import COST_OF_REVENUE
from stock_valuation.constants.financial_keys import OPERATING_EXPENSE
from stock_valuation.constants.financial_keys import DEPRECIATION
from stock_valuation.constants.financial_keys import PROVISION_FOR_TAXES
from stock_valuation.constants.financial_keys import CAPITAL_EXPENDITURE
from stock_valuation.constants.financial_keys import WORKING_CAPITAL_DELTA
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_REVENUES
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_REVENUE_FROM_CONTRACT_WITH_CUSTOMER_EXCLUDING_ASSESSED_TAX
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_COST_OF_REVENUE
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_COST_OF_GOODS_AND_SERVICE_EXCLUDING_DEPRECIATION_DEPLETION_AND_AMORTIZATION
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_OPERATING_INCOME_LOSS
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_DEPRECIATION_DEPLETION_AND_AMORTIZATION
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_INCOME_TAX_EXPENSE_BENEFIT
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_PAYMENTS_TO_ACQUIRE_PROPERTY_PLANT_AND_EQUIPMENT
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_ASSETS_CURRENT
from stock_valuation.constants.us_gaap_financial_keys import US_GAAP_LIABILITIES_CURRENT


def test_map(raw_financials):
    revenue = RowFinancialsMapper([US_GAAP_REVENUES, US_GAAP_REVENUE_FROM_CONTRACT_WITH_CUSTOMER_EXCLUDING_ASSESSED_TAX])
    cost_of_revenue = RowFinancialsMapper([US_GAAP_COST_OF_REVENUE, US_GAAP_COST_OF_GOODS_AND_SERVICE_EXCLUDING_DEPRECIATION_DEPLETION_AND_AMORTIZATION])
    current_assets = RowFinancialsMapper([US_GAAP_ASSETS_CURRENT])
    current_liabilities = RowFinancialsMapper([US_GAAP_LIABILITIES_CURRENT])
    mapping_config = {
        REVENUE: revenue,
        COST_OF_REVENUE: cost_of_revenue,
        OPERATING_EXPENSE: revenue - cost_of_revenue - RowFinancialsMapper([US_GAAP_OPERATING_INCOME_LOSS]),
        DEPRECIATION: RowFinancialsMapper([US_GAAP_DEPRECIATION_DEPLETION_AND_AMORTIZATION]),
        PROVISION_FOR_TAXES: RowFinancialsMapper([US_GAAP_INCOME_TAX_EXPENSE_BENEFIT]),
        CAPITAL_EXPENDITURE: RowFinancialsMapper([US_GAAP_PAYMENTS_TO_ACQUIRE_PROPERTY_PLANT_AND_EQUIPMENT]),
        WORKING_CAPITAL_DELTA: DeltaFinancialsMapper(current_assets - current_liabilities),
    }

    financials_mapper = CompositeFinancialsMapper(mapping_config)
    actual = financials_mapper.map(raw_financials)

    expected = _get_expected(raw_financials)
    pd.testing.assert_frame_equal(actual, expected)


def _get_expected(finacials_df):
    revenue = finacials_df.loc[[US_GAAP_REVENUES]].reset_index(drop=True).astype(int)
    cost_of_revenue = finacials_df.loc[[US_GAAP_COST_OF_GOODS_AND_SERVICE_EXCLUDING_DEPRECIATION_DEPLETION_AND_AMORTIZATION]].reset_index(drop=True).astype(int)
    operating_income = finacials_df.loc[[US_GAAP_OPERATING_INCOME_LOSS]].reset_index(drop=True).astype(int)
    operating_expense = revenue - cost_of_revenue - operating_income
    depreciation = finacials_df.loc[[US_GAAP_DEPRECIATION_DEPLETION_AND_AMORTIZATION]].astype(int)
    provision_for_taxes = finacials_df.loc[[US_GAAP_INCOME_TAX_EXPENSE_BENEFIT]].astype(int)
    capital_expenditure = finacials_df.loc[[US_GAAP_PAYMENTS_TO_ACQUIRE_PROPERTY_PLANT_AND_EQUIPMENT]].astype(int)
    current_assets = finacials_df.loc[[US_GAAP_ASSETS_CURRENT]].reset_index(drop=True).astype(int)
    current_liabilites = finacials_df.loc[[US_GAAP_LIABILITIES_CURRENT]].reset_index(drop=True).astype(int)
    working_capital_delta = (current_assets - current_liabilites).diff(axis=1)

    revenue.index = [REVENUE]
    cost_of_revenue.index = [COST_OF_REVENUE]
    operating_expense.index = [OPERATING_EXPENSE]
    depreciation.index = [DEPRECIATION]
    provision_for_taxes.index = [PROVISION_FOR_TAXES]
    capital_expenditure.index = [CAPITAL_EXPENDITURE]
    working_capital_delta.index = [WORKING_CAPITAL_DELTA]

    return pd.concat([
        revenue,
        cost_of_revenue,
        operating_expense,
        depreciation,
        provision_for_taxes,
        capital_expenditure,
        working_capital_delta,
    ])
