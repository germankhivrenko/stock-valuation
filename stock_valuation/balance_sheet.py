from typing import TYPE_CHECKING

from stock_valuation.balance_sheet_ratios import BalanceSheetRatios
from dataclasses import dataclass

if TYPE_CHECKING:
    from stock_valuation.income_statement import IncomeStatement


@dataclass(frozen=True)
class BalanceSheet:
    # current (short-term) assets
    cash: int
    inventory: int
    accounts_receivables: int
    other_current_assets: int
    # short_term_investments: int
    total_current_assets: int

    # long-term assets
    property_plant_and_equipment: int
    goodwill: int
    # other_long_term_assets: int

    total_assets: int

    # current (short-term) liabilites
    short_term_debt: int
    accounts_payable: int
    other_current_liabilities: int
    total_current_liabilities: int

    # long-term liabilites
    long_term_debt: int

    total_liabilities: int

    # equity
    total_shareholder_equity: int

    @property
    def total_long_term_assets(self) -> int:
        return self.total_assets - self.total_current_assets

    @property
    def total_long_term_liabilities(self) -> int:
        return self.total_liabilities - self.total_current_liabilities

    @property
    def total_debt(self) -> int:
        return self.short_term_debt + self.long_term_debt

    @staticmethod
    def from_alpha_vantage(data: dict[str, str]) -> "BalanceSheet":
        return BalanceSheet(
            cash=int(data["cashAndCashEquivalentsAtCarryingValue"]),
            inventory=int(0 if data["inventory"] == "None" else data["inventory"]),  # TODO: fix
            accounts_receivables=int(0 if data["currentNetReceivables"] == "None" else data["currentNetReceivables"]),
            # short_term_investments=int(data["shortTermInvestements"]),
            other_current_assets=int(data["otherCurrentAssets"]),
            total_current_assets=int(data["totalCurrentAssets"]),

            property_plant_and_equipment=int(data["propertyPlantEquipment"]),
            goodwill=int(data["goodwill"]),
            # other_long_term_assets=int(data["otherNonCurrentAssets"]),

            total_assets=int(data["totalAssets"]),

            short_term_debt=int(data["shortTermDebt"]),
            accounts_payable=int(data["currentAccountsPayable"]),
            other_current_liabilities=int(data["otherCurrentLiabilities"]),
            total_current_liabilities=int(data["totalCurrentLiabilities"]),

            long_term_debt=int(data["longTermDebt"]),

            total_liabilities=int(data["totalLiabilities"]),

            total_shareholder_equity=int(data["totalShareholderEquity"]),
        )

    def get_ratios(self, income_statement: "IncomeStatement", prev_bs: "BalanceSheet") -> BalanceSheetRatios:
        return BalanceSheetRatios(
            accounts_receivables_to_revenue=self.accounts_receivables / income_statement.revenue,
            inventory_to_revenue=self.inventory / income_statement.revenue,
            ppe_to_revenue=self.property_plant_and_equipment / income_statement.revenue,
            short_term_debt_to_revenue=self.short_term_debt / income_statement.revenue,
            accounts_payable_to_cost_of_revenue=self.accounts_payable / income_statement.revenue,
        )
