import types
from datetime import datetime

import sys

from pegasus_tracker.db import insert_transactions, get_dsn
from pegasus_tracker.models import Transaction


class DummyCursor:
    def __init__(self):
        self.statements = []

    def execute(self, query, params):
        self.statements.append((query, params))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class DummyConnection:
    def __init__(self):
        self.cursor_obj = DummyCursor()
        self.closed = False
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True


def test_get_dsn_env(monkeypatch):
    monkeypatch.setenv('PEGASUS_DB_DSN', 'postgresql://envuser:envpass@env/db')
    assert get_dsn() == 'postgresql://envuser:envpass@env/db'


def test_insert_transactions_uses_psycopg2(monkeypatch):
    dummy_conn = DummyConnection()
    captured = {}

    def fake_connect(dsn=None):
        captured['dsn'] = dsn
        return dummy_conn

    fake_mod = types.SimpleNamespace(connect=fake_connect)
    monkeypatch.setitem(sys.modules, 'psycopg2', fake_mod)
    monkeypatch.setenv('PEGASUS_DB_DSN', 'postgresql://user:pass@host/db')

    tx = Transaction(
        date=datetime(2025, 6, 1),
        account='****1234',
        description='Coffee',
        amount=-5.75,
        category=None,
        source='test.csv',
    )

    insert_transactions([tx])

    assert dummy_conn.committed
    assert dummy_conn.closed
    assert captured['dsn'] == 'postgresql://user:pass@host/db'
    assert dummy_conn.cursor_obj.statements
    query, params = dummy_conn.cursor_obj.statements[0]
    assert 'INSERT INTO transactions' in query
    assert params[0] == datetime(2025, 6, 1)
