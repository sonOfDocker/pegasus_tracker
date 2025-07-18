import pytest
from pegasus_tracker.normalizer import normalize_checking


def test_unknown_column_raises_key_error():
    """Should raise KeyError when 'Transaction Amount' is missing"""
    rows = [
        {
            'Account Number': '123456789',
            'Transaction Description': 'Coffee Shop',
            'Transaction Date': '06/10/2025',
            'Amount': '9.99',  # should be 'Transaction Amount'
        }
    ]
    with pytest.raises(KeyError):
        normalize_checking(rows)


def test_empty_row_is_skipped():
    """An empty row should be skipped without raising an error"""
    rows = [{}]
    result = normalize_checking(rows)
    assert result == []


def test_malformed_amount_is_skipped():
    """Rows with non-numeric amounts should be skipped without raising an error"""
    rows = [
        {
            'Account Number': '1111222233334444',
            'Transaction Description': 'Refund',
            'Transaction Date': '06/11/2025',
            'Transaction Amount': 'not-a-number',
        }
    ]
    result = normalize_checking(rows)
    assert result == []
