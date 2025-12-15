# pegasus-tracker

Pegasus is a privacy-first personal finance platform designed to help households track, analyze, and budget their finances without relying on third-party aggregators.

The system ingests financial data from multiple sources—such as bank and credit card CSVs, Amazon order reports, and other vendor exports—and standardizes it into a clean, consistent model. This unified pipeline provides a single source of truth for cash flow, spending insights, and budgeting workflows.

Pegasus is built with a modular architecture that supports local-first data processing, user-controlled storage, and future extensions for automation and intelligent analysis.

**Focus:** Secure household finance tracking • Data normalization • Budgeting • Extensible architecture


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

By default, the CLI connects using the credentials from `docker-compose.yml`, maintained in .env file.
To override them set the `PEGASUS_DB_DSN` environment variable or pass
`--dsn`:

```bash
export PEGASUS_DB_DSN=postgresql://pegasus_user:pegasus_pass@localhost:5432/pegasus
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store
# or specify explicitly
PYTHONPATH=src python3 -m pegasus_tracker.pipeline data/sample/checking_bank_june2025.csv --kind checking --store --dsn "$PEGASUS_DB_DSN"
```
