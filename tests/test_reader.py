import os
import logging
import pytest

from pegasus_tracker.reader import read_checking_csv, read_credit_csv

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'sample')


def test_read_checking_csv_parses_rows():
    """
    Test that read_checking_csv successfully reads a valid checking account CSV file.

    Verifies that:
    - The correct number of rows is parsed.
    - Key fields like 'Account Number' and 'Transaction Amount' match expected values.
    """
    path = os.path.join(DATA_DIR, 'checking_bank_june2025.csv')
    rows = read_checking_csv(path)
    assert len(rows) == 3
    first = rows[0]
    assert first['Account Number'] == '123456789'
    assert first['Transaction Amount'] == '-5.75'


def test_read_credit_csv_parses_rows():
    """
    Test that read_credit_csv correctly parses a valid credit account CSV file.

    Verifies that:
    - The row count matches expectations.
    - Fields like 'Description' and 'Debit' are read accurately from the first row.
    """
    path = os.path.join(DATA_DIR, 'credit_bank_june2025.csv')
    rows = read_credit_csv(path)
    assert len(rows) == 3
    first = rows[0]
    assert first['Description'] == 'Netflix.com'
    assert first['Debit'] == '15.49'


def test_read_checking_csv_missing_file_logs_error(caplog):
    """
    Test that read_checking_csv raises FileNotFoundError and logs an error when the file is missing.

    Uses caplog to assert that an appropriate error message is logged.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(FileNotFoundError):
            read_checking_csv('nonexistent.csv')
    assert any('File not found' in message for message in caplog.messages)


def test_read_credit_csv_missing_file_logs_error(caplog):
    """
    Test that read_credit_csv raises FileNotFoundError and logs an error when the file is missing.

    Uses caplog to confirm error logging behavior.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(FileNotFoundError):
            read_credit_csv('nonexistent.csv')
    assert any('File not found' in message for message in caplog.messages)