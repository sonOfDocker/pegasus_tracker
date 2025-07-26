import os
import logging
import pytest

from pegasus_tracker.readers.bank_reader import read_credit_csv

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'sample')


def test_read_credit_csv_parses_rows():
    path = os.path.join(DATA_DIR, 'credit_bank_june2025.csv')
    rows = read_credit_csv(path)
    assert len(rows) == 3
    first = rows[0]
    assert first['Description'] == 'Netflix.com'
    assert first['Debit'] == '15.49'


def test_read_credit_csv_missing_file_logs_error(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(FileNotFoundError):
            read_credit_csv('nonexistent.csv')
    assert any('File not found' in message for message in caplog.messages)
