from datetime import datetime
from pegasus_tracker.models import Transaction

def test_transaction_creation():
    """It should create a Transaction object with all fields correctly assigned."""
    tx = Transaction(
        date=datetime(2025, 6, 30),
        account="Chase Checking",
        description="Starbucks",
        amount=-5.75,
        category="Coffee",
        source="chase_june2025.csv"
    )

    assert tx.date == datetime(2025, 6, 30)
    assert tx.account == "Chase Checking"
    assert tx.description == "Starbucks"
    assert tx.amount == -5.75
    assert tx.category == "Coffee"
    assert tx.source == "chase_june2025.csv"

def test_income_expense_flags():
    """It should correctly classify transactions as income or expense based on amount."""
    income = Transaction(
        date=datetime.now(),
        account="PayPal",
        description="Freelance gig",
        amount=200.0
    )
    expense = Transaction(
        date=datetime.now(),
        account="Chase",
        description="Groceries",
        amount=-50.0
    )

    assert income.is_income()
    assert not income.is_expense()
    assert not expense.is_income()
    assert expense.is_expense()
