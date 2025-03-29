import pytest
from stock_valuation.income_statement import IncomeStatement


def test_init():
    data = {
        "fiscalDateEnding": "2023-12-31",
        "reportedCurrency": "USD",
        "grossProfit": "34300000000",
        "totalRevenue": "61860000000",
        "costOfRevenue": "27560000000",
        "costofGoodsAndServicesSold": "245000000",
        "operatingIncome": "6979000000",
        "sellingGeneralAndAdministrative": "19003000000",
        "researchAndDevelopment": "6775000000",
        "operatingExpenses": "27321000000",
        "investmentIncomeNet": "None",
        "netInterestIncome": "-1607000000",
        "interestIncome": "591000000",
        "interestExpense": "1607000000",
        "nonInterestIncome": "-77000000",
        "otherNonOperatingIncome": "266000000",
        "depreciation": "2109000000",
        "depreciationAndAmortization": "2287000000",
        "incomeBeforeTax": "8678000000",
        "incomeTaxExpense": "1176000000",
        "interestAndDebtExpense": "1607000000",
        "netIncomeFromContinuingOperations": "7514000000",
        "comprehensiveIncomeNetOfTax": "5481000000",
        "ebit": "10285000000",
        "ebitda": "12572000000",
        "netIncome": "7502000000"
    }

    income_statement = IncomeStatement.from_alpha_vantage(data)

    assert income_statement.revenue == int(data["totalRevenue"])
    assert income_statement.cost_of_revenue == int(data["costOfRevenue"])
    assert income_statement.operating_expenses == int(data["operatingExpenses"])
    assert income_statement.selling_general_and_administrative == int(data["sellingGeneralAndAdministrative"])
    assert income_statement.research_and_development == int(data["researchAndDevelopment"])
    assert income_statement.deprecation_and_amortization == int(data["depreciationAndAmortization"])
    assert income_statement.interest_expense == int(data["interestExpense"])
    assert income_statement.provision_for_taxes == int(data["incomeTaxExpense"])
    assert income_statement.consolidated_net_income == int(data["netIncomeFromContinuingOperations"])
    assert income_statement.net_income == int(data["netIncome"])
    assert income_statement.gross_profit == int(data["totalRevenue"]) - int(data["costOfRevenue"])
    assert income_statement.operating_income == int(data["totalRevenue"]) - int(data["costOfRevenue"]) - int(data["operatingExpenses"])
