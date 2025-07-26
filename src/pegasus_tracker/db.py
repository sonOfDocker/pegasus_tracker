import os
from typing import Iterable
from dotenv import load_dotenv
from .models import Transaction
from .logger import get_logger

logger = get_logger(__name__)



# Load .env file
load_dotenv()

# Pull from environment
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE")

# Build the DSN
DEFAULT_DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


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

