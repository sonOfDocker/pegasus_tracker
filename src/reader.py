import csv
from typing import List, Dict


def read_checking_csv(filepath: str) -> List[Dict]:
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def read_credit_csv(filepath: str) -> List[Dict]:
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
