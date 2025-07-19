import os
from typing import Iterable
from .models import Transaction
from .logger import get_logger

logger = get_logger(__name__)


def insert_transactions(transactions: Iterable[Transaction], dsn: str | None = None) -> None:
    """Insert a collection of :class:`Transaction` objects into Postgres.

    Parameters
    ----------
    transactions:
        Iterable of Transaction instances to persist.
    dsn:
        Optional DSN string. If omitted, connection parameters are read from the
        environment using the standard ``PG*`` variables.
    """
    try:
        import psycopg2
    except ImportError as exc:
        logger.error("psycopg2 is required for database operations: %s", exc)
        raise

    conn = psycopg2.connect(dsn or "")
    try:
        with conn.cursor() as cur:
            for tx in transactions:
                cur.execute(
                    "INSERT INTO transactions (date, description, amount, category, account, source) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        tx.date,
                        tx.description,
                        tx.amount,
                        tx.category,
                        tx.account,
                        tx.source,
                    ),
                )
        conn.commit()
    finally:
        conn.close()

