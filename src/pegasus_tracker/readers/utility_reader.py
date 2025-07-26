from .base_reader import read_csv


def read_checking_csv(filepath: str):
    """Read a checking account CSV exported from a utility bank."""
    return read_csv(filepath)
