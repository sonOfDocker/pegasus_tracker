from datetime import datetime
from typing import List, Dict
from .logger import get_logger;

logger = get_logger(__name__)

def normalize_checking(rows: List[Dict]) -> List[Dict]:
    REQUIRED_KEYS = ['Transaction Amount', 'Transaction Date', 'Transaction Description', 'Account Number']
    normalized = []

    for row in rows:
        missing = [k for k in REQUIRED_KEYS if k not in row]
        if missing:
            logger.error(f"Missing {missing} in row {row}")
            raise KeyError(f"Missing required fields {missing} in row: {row}")

        amount = float(row['Transaction Amount'])

        normalized.append({
            'Date': _parse_date(row['Transaction Date']),
            'Description': row['Transaction Description'].strip(),
            'Amount': amount,
            'Category': None,
            'Account': _mask_account(row['Account Number']),
            'Source': 'Chase Checking'
        })

    return normalized



def normalize_credit(rows: List[Dict]) -> List[Dict]:
    normalized = []
    for row in rows:
        debit = row.get('Debit')
        credit = row.get('Credit')
        amount = float(debit) if debit else -float(credit)
        normalized.append({
            'Date': _parse_date(row['Transaction Date']),
            'Description': row['Description'].strip(),
            'Amount': -amount,  # spending is negative
            'Category': row.get('Category'),
            'Account': row['Card No.'],
            'Source': 'Amex Credit'
        })
    return normalized


def _parse_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_str


def _mask_account(acc_num: str) -> str:
    return f"****{acc_num[-4:]}"
