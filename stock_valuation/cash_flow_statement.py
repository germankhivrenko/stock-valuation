from dataclasses import dataclass


@dataclass(frozen=True)
class CashFlowStatement:
    # consolidated_net_income: int
    operating_cash_flow: int
    # add_deprecation_and_amortization: int
    # add_interest_expense: int
    # add_increase_in_accounts_payable: int
    # add_increase_in_other_current_liabilities: int
    # less_increase_in_inventory: int
    # less_increase_in_accounts_receivables: int
    # less_increase_in_other_current_assets: int

    investment_cash_frow: int
    # less_capex: int
    # less_increase_in_goodwill: int

    financing_cash_flow: int
    # add_new_sort_term_debt_to_be_raised
    # add_long_sort_term_debt_to_be_raised
    # less_interest_expense
    # less_short_term_to_be_repaid
    # less_long_term_to_be_repaid
    # less_dividends_to_be_paid
    # less_share_buyback

    # short_term_debt_change
    short_term_debt_proceeds: int
    # long_term_debt_change
    long_term_debt_proceeds: int

    common_stock_dividend_payout: int
    common_stock_buybacks: int

    @property
    def net_cash_flow(self) -> int:
        return self.operating_cash_flow + self.investment_cash_frow + self.financing_cash_flow

    @staticmethod
    def from_alpha_vantage(data: dict[str, str]) -> "CashFlowStatement":
        return CashFlowStatement(
            operating_cash_flow=int(data["operatingCashflow"]),
            investment_cash_frow=int(data["cashflowFromInvestment"]),
            financing_cash_flow=int(data["cashflowFromFinancing"]),
            short_term_debt_proceeds=int(data["proceedsFromRepaymentsOfShortTermDebt"]),
            long_term_debt_proceeds=int(data["proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"]),
            common_stock_dividend_payout=int(data["dividendPayoutCommonStock"]),
            common_stock_buybacks=int(data["paymentsForRepurchaseOfCommonStock"]),
        )
