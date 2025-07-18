# pegasus-tracker
A privacy-focused personal finance tracking system for aggregating bank data, receipts, and expenses from various sources. Built with Python and designed for secure, local analysis.

## Processing CSV Files

A simple CLI is available to parse sample CSVs and inspect the normalized transactions.

```bash
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking
```

This will read the CSV, normalize each row, convert it into `Transaction` objects and log the parsed transactions. Use `--kind credit` for credit card statements.