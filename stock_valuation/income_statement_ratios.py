from dataclasses import dataclass


@dataclass(frozen=True)
class IncomeStatementRatios:
    revenue_growth: float
    gross_margin: float

    # TODO: consider comparison to Gross Profit instead of Revenue
    operating_margin: float
    sga_to_revenue: float
    research_and_development_to_revenue: float
    deprecation_and_amortization_to_ppe: float

    interest_expense_to_total_debt: float
    taxes_to_pretax_profit: float
    minority_interest_to_consolidated_net_income: float
