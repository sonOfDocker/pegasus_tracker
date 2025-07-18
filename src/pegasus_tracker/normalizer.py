from datetime import datetime
from typing import List, Dict
from .logger import get_logger

logger = get_logger(__name__)

def normalize_checking(rows: List[Dict]) -> List[Dict]:
    REQUIRED_KEYS = ['Transaction Amount', 'Transaction Date', 'Transaction Description', 'Account Number']
    normalized = []

    for idx, row in enumerate(rows):
        if not row or all(v.strip() == '' for v in row.values()):
            logger.warning(f"Empty row skipped at index {idx}: {row}")
            continue

        missing = [k for k in REQUIRED_KEYS if k not in row]
        if missing:
            logger.error(f"Missing {missing} in row at index {idx}: {row}")
            raise KeyError(f"Missing required fields {missing} in row: {row}")

        try:
            amount = float(row['Transaction Amount'])
        except ValueError:
            logger.error(f"Non-numeric amount '{row['Transaction Amount']}' in row at index {idx}: {row}")
            continue

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

    for idx, row in enumerate(rows):
        if not row or all(v.strip() == '' for v in row.values()):
            logger.warning(f"Empty row skipped at index {idx}: {row}")
            continue

        debit = row.get('Debit')
        credit = row.get('Credit')

        try:
            if debit:
                amount = float(debit)
            elif credit:
                amount = -float(credit)
            else:
                logger.warning(f"Row missing both 'Debit' and 'Credit' at index {idx}: {row}")
                continue
        except ValueError:
            logger.error(f"Non-numeric debit/credit in row at index {idx}: {row}")
            continue

        if 'Card No.' not in row:
            logger.error(f"Missing 'Card No.' in row at index {idx}: {row}")
            continue

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
        logger.warning(f"Failed to parse date: {date_str}")
        return date_str


def _mask_account(acc_num: str) -> str:
    return f"****{acc_num[-4:]}"
