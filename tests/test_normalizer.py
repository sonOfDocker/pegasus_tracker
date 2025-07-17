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