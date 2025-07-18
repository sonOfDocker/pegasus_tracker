import pytest
from pegasus_tracker.normalizer import normalize_checking, _parse_date


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


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("06/01/2025", "2025-06-01"),
        ("6/1/2025", "2025-06-01"),
        ("06/1/2025", "2025-06-01"),
        ("2025-06-01", "2025-06-01"),
        ("06-01-2025", "06-01-2025"),
    ],
)
def test_parse_date_various_formats(input_date, expected):
    """_parse_date should gracefully handle subtly different date formats."""
    assert _parse_date(input_date) == expected


def test_amount_with_comma_is_skipped():
    """Rows with a thousand separators should be skipped as malformed amounts."""
    rows = [
        {
            'Account Number': '9999888877776666',
            'Transaction Description': 'Payment',
            'Transaction Date': '06/12/2025',
            'Transaction Amount': '1,234.56',
        }
    ]
    assert normalize_checking(rows) == []


def test_amount_with_parentheses_is_skipped():
    """Rows using parentheses for negatives should be skipped as malformed."""
    rows = [
        {
            'Account Number': '9999888877776666',
            'Transaction Description': 'Adjustment',
            'Transaction Date': '06/13/2025',
            'Transaction Amount': '(123.45)',
        }
    ]
    assert normalize_checking(rows) == []