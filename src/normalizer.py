from datetime import datetime
from typing import List, Dict


def normalize_checking(rows: List[Dict]) -> List[Dict]:
    normalized = []
    for row in rows:
        amount = float(row['Transaction Amount'])
        normalized.append({
            'Date': _parse_date(row['Transaction Date']),
            'Description': row['Transaction Description'].strip(),
            'Amount': amount,
            'Category': None,  # will be set later
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
