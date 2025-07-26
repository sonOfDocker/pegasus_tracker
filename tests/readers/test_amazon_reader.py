import os

from pegasus_tracker.readers.amazon_reader import read_amazon_csv

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'sample')


def test_read_amazon_csv_stubs():
    path = os.path.join(DATA_DIR, 'checking_bank_june2025.csv')
    rows = read_amazon_csv(path)
    assert isinstance(rows, list)
