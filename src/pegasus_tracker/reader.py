import csv
from typing import List, Dict
from .logger import get_logger

logger = get_logger(__name__)


def read_checking_csv(filepath: str) -> List[Dict]:
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except csv.Error as exc:
        logger.error(f"CSV parsing error for {filepath}: {exc}")
        raise


def read_credit_csv(filepath: str) -> List[Dict]:
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except csv.Error as exc:
        logger.error(f"CSV parsing error for {filepath}: {exc}")
        raise
