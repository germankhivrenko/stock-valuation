from dataclasses import dataclass


@dataclass(frozen=True)
class BalanceSheetRatios:
    accounts_receivables_to_revenue: float
    inventory_to_revenue: float
    ppe_to_revenue: float
    short_term_debt_to_revenue: float
    accounts_payable_to_cost_of_revenue: float
