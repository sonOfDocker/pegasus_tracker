import os
from typing import Iterable

from .models import Transaction
from .logger import get_logger

logger = get_logger(__name__)

# Default DSN matches credentials defined in docker-compose.yml
DEFAULT_DSN = (
    "postgresql://pegasus_user:pegasus_pass@localhost:5432/pegasus"
)


def get_dsn() -> str:
    """Return the Postgres connection string.

    The value is taken from the ``PEGASUS_DB_DSN`` environment variable if set
    otherwise the credentials from ``docker-compose.yml`` are used.
    """
    return os.getenv("PEGASUS_DB_DSN", DEFAULT_DSN)


def insert_transactions(transactions: Iterable[Transaction], dsn: str | None = None) -> None:
    """Insert a collection of :class:`Transaction` objects into Postgres.

    Parameters
    ----------
    transactions:
        Iterable of Transaction instances to persist.
    dsn:
        Optional DSN string. If omitted, :func:`get_dsn` is used which reads the
        ``PEGASUS_DB_DSN`` environment variable or falls back to the default
        connection string.
    """
    try:
        import psycopg2
    except ImportError as exc:
        logger.error("psycopg2 is required for database operations: %s", exc)
        raise

    conn = psycopg2.connect(dsn or get_dsn())
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

