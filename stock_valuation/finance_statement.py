from dataclasses import dataclass

from stock_valuation.balance_sheet import BalanceSheet
from stock_valuation.income_statement import IncomeStatement


@dataclass(frozen=True)
class FinanceStatement:
    income_statement: IncomeStatement
    balance_sheet: BalanceSheet
