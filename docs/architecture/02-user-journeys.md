# Pegasus Finance Pipeline — Step 2: Key User Journeys & Questions

This document defines the **core user journeys** and **questions Pegasus must answer** for the MVP.
All downstream design decisions (data model, ingestion pipeline, APIs, UI) must support these journeys.

---

## Goals of This Step

- Anchor system design in **real user workflows**
- Define **clear success criteria** for MVP
- Enumerate the **questions the system must answer**
- Prevent premature optimization and scope creep

---

## MVP Scope Guardrails

- **Sources:** CSV imports only (bank / credit card exports)
- **Users:** Single household (multi-user later)
- **UI:** CLI + basic web/table output acceptable
- **Categorization:** Manual + rule-based only (no ML)
- **Budgets:** Monthly, category-based

---

## J1 — Import a Statement / Export and See “What Got In”

**Trigger**  
User uploads or drops a CSV (bank, credit card, vendor export).

**Success Criteria**  
User can clearly see what was imported, skipped, or rejected — and why.

### Questions Answered
- How many rows were read vs imported vs rejected?
- What account(s) were these mapped to?
- Were duplicates detected?
- What errors or unknown formats were encountered?

### Inputs
- CSV files

### Outputs
- Import run summary (counts, totals)
- Rejected rows with reasons
- Staged transactions ready for review

### Acceptance Tests
- Importing the same CSV twice results in **zero net new transactions** on the second run.
- A malformed row is rejected without failing the entire import.

---

## J2 — View Transactions by Account, Date, Category, Merchant

**Trigger**  
User wants to browse or verify financial activity.

**Success Criteria**  
Fast filtering, consistent totals, predictable behavior.

### Questions Answered
- What transactions occurred in a given date range?
- What did I spend per account?
- Show all transactions for a specific merchant.
- Which transactions are uncategorized?

### Inputs
- Normalized transactions

### Outputs
- Filterable transaction list
- Totals for current filters

### Acceptance Tests
- Filter totals equal the sum of displayed rows.
- Merchant search returns normalized variants (when supported).

---

## J3 — Categorize Transactions Quickly (Rules + Manual)

**Trigger**  
New transactions are imported and require categorization.

**Success Criteria**  
Low friction categorization with an audit trail.

### Questions Answered
- What is uncategorized or low-confidence?
- Can I fix this once and never again?
- What transactions would a rule affect before applying it?

### Inputs
- Transactions
- Category taxonomy
- Categorization rules

### Outputs
- Manual categorization flow
- Rule management and previews
- Rule application results

### Acceptance Tests
- Manual category changes persist immediately.
- New rules apply to historical and future transactions (with preview).

---

## J4 — Monthly Spend Summary (Category + Merchant + Trend)

**Trigger**  
User wants a monthly financial snapshot.

**Success Criteria**  
Clear monthly view with trustworthy numbers and trend context.

### Questions Answered
- How much was spent per category this month?
- Who were the top merchants?
- What changed compared to last month?
- How much is uncategorized?

### Inputs
- Categorized transactions
- Date/month boundaries

### Outputs
- Monthly summary report
- Month-over-month deltas
- Drill-down paths to transactions

### Acceptance Tests
- Reports clearly flag uncategorized spend.
- Refunds do not silently inflate totals.

---

## J5 — Budget Setup (Category Budgets + Over/Under)

**Trigger**  
User defines monthly budgets and monitors progress.

**Success Criteria**  
Clear visibility into remaining budget and problem areas.

### Questions Answered
- What is my budget per category?
- How much is spent vs remaining?
- Which categories are over budget?

### Inputs
- Budget definitions (category + month)
- Categorized spend

### Outputs
- Budget vs actual table
- Remaining budget calculations
- Over-budget indicators

### Acceptance Tests
- Editing a budget updates remaining values immediately.
- Split transactions allocate spend correctly across categories.

---

## Core Question Catalog (Must Be Supported by the System)

- Transactions by date range, account, merchant, category
- Uncategorized transactions
- Monthly totals by category and merchant
- Month-over-month deltas
- Budget vs actual per category per month
- Import run audit data (read / imported / rejected / deduplicated)

---

## What This Enables Next

This document directly informs:
- Step 3: Data Model & Entities
- Step 4: Ingestion & Normalization Pipeline
- Step 5: Query & Reporting Layer

If a future feature does not support a journey or question listed here, it is **out of MVP scope**.

---
