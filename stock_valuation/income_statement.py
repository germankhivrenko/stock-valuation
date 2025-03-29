from dataclasses import dataclass
from typing import TYPE_CHECKING

from stock_valuation.income_statement_ratios import IncomeStatementRatios

if TYPE_CHECKING:
    from stock_valuation.balance_sheet import BalanceSheet


@dataclass(frozen=True)
class IncomeStatement:
    # revenue
    revenue: int
    cost_of_revenue: int

    # operating expenses
    operating_expenses: int
    selling_general_and_administrative: int
    research_and_development: int
    deprecation_and_amortization: int

    # interest & debt expenses
    interest_expense: int

    # taxes
    provision_for_taxes: int

    # net income
    consolidated_net_income: int
    net_income: int

    @property
    def gross_profit(self) -> int:
        return self.revenue - self.cost_of_revenue

    @property
    def operating_income(self) -> int:
        return self.gross_profit - self.operating_expenses

    @property
    def pretax_profit(self) -> int:
        return self.consolidated_net_income + self.provision_for_taxes

    @property
    def minority_interest(self) -> int:
        return self.consolidated_net_income - self.net_income

    @staticmethod
    def from_alpha_vantage(data: dict[str, int]) -> "IncomeStatement":
        return IncomeStatement(
            revenue=int(data["totalRevenue"]),
            cost_of_revenue=int(data["costOfRevenue"]),
            operating_expenses=int(data["operatingExpenses"]),
            selling_general_and_administrative=int(data["sellingGeneralAndAdministrative"]),
            research_and_development=int(data["researchAndDevelopment"]),
            deprecation_and_amortization=int(data["depreciationAndAmortization"]),
            interest_expense=int(data["interestAndDebtExpense"]),
            provision_for_taxes=int(data["incomeTaxExpense"]),
            consolidated_net_income=int(data["netIncomeFromContinuingOperations"]),
            net_income=int(data["netIncome"]),
        )

    def get_ratios(self, prev: "IncomeStatement", prev_bs: "BalanceSheet") -> IncomeStatementRatios:
        return IncomeStatementRatios(
            revenue_growth=(self.revenue / prev.revenue) - 1,
            gross_margin=self.cost_of_revenue / self.revenue,

            operating_margin=self.operating_expenses / self.revenue,
            sga_to_revenue=self.selling_general_and_administrative / self.revenue,
            research_and_development_to_revenue=self.research_and_development / self.revenue,
            deprecation_and_amortization_to_ppe=self.deprecation_and_amortization / prev_bs.property_plant_and_equipment,

            interest_expense_to_total_debt=self.interest_expense / prev_bs.total_debt,
            taxes_to_pretax_profit=self.provision_for_taxes / self.pretax_profit,
            minority_interest_to_consolidated_net_income=self.minority_interest / self.consolidated_net_income,
        )
