# pegasus-tracker
A privacy-focused personal finance tracking system for aggregating bank data, receipts, and expenses from various sources. Built with Python and designed for secure, local analysis.

## Processing CSV Files

A simple CLI is available to parse sample CSVs and inspect the normalized transactions or persist them to Postgres.

```bash
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store
```

This will read the CSV, normalize each row, convert it into `Transaction` objects and log the parsed transactions. Use `--kind credit` for credit card statements.
## Local Postgres Setup

A `docker-compose.yml` is provided to run a development Postgres instance. Start it with:

```bash
docker compose up -d db
```

The database will be available on `localhost:5432` with the default credentials defined in the compose file. An initialization script creates a `transactions` table that can be extended with categories and budgets.

Once Postgres is running you can persist parsed transactions by including the `--store` flag when running the CLI:

```bash
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store
```

By default the CLI connects using the credentials from `docker-compose.yml`.
To override them set the `PEGASUS_DB_DSN` environment variable or pass
`--dsn`:

```bash
export PEGASUS_DB_DSN=postgresql://pegasus_user:pegasus_pass@localhost:5432/pegasus
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store
# or specify explicitly
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store --dsn "$PEGASUS_DB_DSN"
```
