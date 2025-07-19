import argparse
from datetime import datetime
from typing import List

from .reader import read_checking_csv, read_credit_csv
from .normalizer import normalize_checking, normalize_credit
from .models import Transaction
from .logger import get_logger
from .db import insert_transactions

logger = get_logger(__name__)

READERS = {
    "checking": read_checking_csv,
    "credit": read_credit_csv,
}

NORMALIZERS = {
    "checking": normalize_checking,
    "credit": normalize_credit,
}


def rows_to_transactions(rows: List[dict]) -> List[Transaction]:
    txs = []
    for r in rows:
        try:
            # normalizer returns ISO date strings. Convert to datetime objects
            date_val = r["Date"]
            if isinstance(date_val, str):
                try:
                    parsed_date = datetime.strptime(date_val, "%Y-%m-%d")
                except ValueError:
                    parsed_date = datetime.strptime(date_val, "%m/%d/%Y")
            else:
                parsed_date = date_val
            tx = Transaction(
                date=parsed_date,
                account=r["Account"],
                description=r["Description"],
                amount=float(r["Amount"]),
                category=r.get("Category"),
                source=r.get("Source"),
            )
            txs.append(tx)
        except Exception as exc:
            logger.error("Failed to create Transaction from %s: %s", r, exc)
    return txs


def process_file(filepath: str, kind: str, store: bool = False) -> List[Transaction]:
    if kind not in READERS:
        raise ValueError(f"Unknown file kind '{kind}'")
    logger.info("Reading %s file: %s", kind, filepath)
    rows = READERS[kind](filepath)
    logger.info("Read %d rows", len(rows))
    normalized = NORMALIZERS[kind](rows)
    logger.info("Normalized to %d transactions", len(normalized))
    txs = rows_to_transactions(normalized)
    for tx in txs:
        logger.info("Parsed: %s", tx)

    if store:
        try:
            insert_transactions(txs)
            logger.info("Inserted %d transactions into the database", len(txs))
        except Exception as exc:
            logger.error("Failed to store transactions: %s", exc)
    return txs


def main(argv=None):
    parser = argparse.ArgumentParser(description="Process financial CSV files")
    parser.add_argument("filepath", help="Path to CSV file")
    parser.add_argument(
        "--kind",
        choices=list(READERS.keys()),
        default="checking",
        help="Type of CSV file (checking or credit)",
    )
    parser.add_argument(
        "--store",
        action="store_true",
        help="Persist parsed transactions to the Postgres database",
    )
    args = parser.parse_args(argv)
    process_file(args.filepath, args.kind, store=args.store)


if __name__ == "__main__":
    main()
