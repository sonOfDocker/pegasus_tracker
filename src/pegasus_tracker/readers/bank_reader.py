from .base_reader import read_csv


def read_credit_csv(filepath: str):
    """Read a credit card CSV statement."""
    return read_csv(filepath)
