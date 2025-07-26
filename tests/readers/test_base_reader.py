import os

from pegasus_tracker.readers.base_reader import read_csv

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'sample')


def test_read_csv_returns_rows():
    path = os.path.join(DATA_DIR, 'checking_bank_june2025.csv')
    rows = read_csv(path)
    assert len(rows) == 3
