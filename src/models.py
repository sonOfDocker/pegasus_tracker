from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    date: datetime
    account: str
    description: str
    amount: float
    category: Optional[str] = None
    source: Optional[str] = None  # e.g., "chase_checking_june2025.csv"

    def is_income(self) -> bool:
        return self.amount > 0

    def is_expense(self) -> bool:
        return self.amount < 0
