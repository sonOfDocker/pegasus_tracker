# Step 3 – Data Sources Inventory (Pegasus Tracker)

This document lists all known data sources that can be ingested into Pegasus and converts that inventory into **actionable engineering decisions**:
- A **data sources inventory table** 
- **Ingestion complexity tiers**
- A **canonical ingestion contract** (what every importer must output)
- A **clear MVP cut line**
- **Input assumptions** that drive Step 4 (schema), pipeline stages, and React UI expectations

---

## 1) Data Sources Inventory Table

| Source | Type | Account/Data Scope | Formats | Historical Window | Access / SLA | Notes | Complexity Tier |
|---|---|---|---|---|---|---|---|
| Capital One | Financial Institution | Checking | CSV, PDF stmt | ~24 months tx history | Immediate download | CSV is generally clean; PDFs are monthly statements; single-account PDFs | Tier 1 |
| Capital One | Financial Institution | Savings | CSV, PDF stmt | ~24 months tx history | Immediate download | Same as checking | Tier 1 |
| Capital One | Financial Institution | Credit Cards | CSV, PDF stmt | Up to 25 months, ~12 months per download | Immediate download | Fields include posted vs transaction date; category included | Tier 1 |
| Amazon | Vendor | Orders, subscriptions, shipments, line items | CSV (via data request) | 10+ years (account lifetime) | Data request SLA 1–2 weeks | Order-centric and verbose; may include noise; payment instruments may include non-owned/untracked | Tier 3 |
| Receipts | Evidence Input | Photos/PDFs of purchases | Image/PDF | User-provided | Immediate upload | Must-have; unstructured; requires manual entry or later extraction | Tier 3 |

---

## 2) Ingestion Complexity Tiers

### Tier 1 – Easy Structured CSV (High confidence)
**Definition:** predictable row-based transactions with stable fields.
- Capital One Checking/Savings CSV
- Capital One Credit Card CSV

**Typical risks:** duplicates on re-import, minor description noise, pending vs posted confusion.

### Tier 2 – Messy CSV/PDF (Medium confidence)
**Definition:** data is extractable but inconsistent or needs heavy parsing.
- (Not yet present in your inventory)
- Placeholder tier for future banks/vendors where CSV is messy or PDFs are needed for extraction.

**Decision:** Tier 2 is reserved for “future sources.” Do not design MVP around PDF parsing.

### Tier 3 – Semi-Structured Vendor + Evidence Inputs (Lower confidence initially)
**Definition:** non-transaction-centric datasets, itemized events, or unstructured evidence.
- Amazon export via data request (order/shipment/item-centric)
- Receipts (photos/PDFs)

**Typical risks:** partial info, many-to-one mapping to bank transactions, reconciliation complexity.

---

## 3) Canonical Ingestion Contract (Importer Output)

Every importer (Capital One CSV, Amazon export, receipts upload) must produce a **standard output contract** so the pipeline is consistent, testable, and idempotent.

### 3.1 Required Output Objects

#### A) `IngestionJob`
Represents one import run (one file, one API export, one upload batch).
- `job_id` (UUID)
- `source_system` (e.g., `capital_one_credit_csv`, `amazon_data_export`, `receipt_upload`)
- `source_artifact` (filename, export id, or upload batch id)
- `imported_at` (timestamp)
- `importer_version` (semantic version)
- `status` (`SUCCESS|PARTIAL|FAILED`)
- `row_counts` / `record_counts` (summary metrics)
- `warnings[]` (non-fatal issues)

#### B) `RawRecord`
A normalized wrapper for “what the source gave us,” preserved for audit/debug.
- `job_id`
- `record_type` (e.g., `BANK_TXN_ROW`, `AMAZON_LINE_ITEM_ROW`, `RECEIPT_METADATA`)
- `source_row_hash` (stable idempotency key)
- `raw_payload` (JSON)
- `observed_at` (timestamp)

#### C) `CanonicalEvent`
The earliest “clean” representation of the business fact (event-first).
- `canonical_event_id`
- `job_id`
- `event_type` (`BANK_TRANSACTION`, `AMAZON_ORDER`, `RECEIPT_PURCHASE`, etc.)
- `event_date` (best-known date; may differ from posted date)
- `description` (best-known human label)
- `amount` (optional for vendor/evidence until reconciled)
- `currency` (if known)
- `source_ref` (Order ID, bank row composite key, etc.)
- `confidence` (optional; helpful for receipts/matching)

#### D) Optional `LineItem` (for itemized sources)
- `canonical_event_id`
- `name`
- `quantity`
- `unit_price`
- `tax`
- `discount`
- `asin/sku` (if available)

> **Note:** “Ledger postings” are not required in Step 3’s contract, but Step 4 will add them as the financial projection of events.

---

## 4) Clear MVP Cut Line (What We Do / Don’t Do)

### MVP Includes (Must ship)
1. **Capital One CSV import**
    - Checking/Savings
    - Credit Cards
2. **Amazon import (via export files)**
    - Ingest exports as events + line items (do not force perfect reconciliation yet)
3. **Receipts upload**
    - Store receipt files + metadata
    - Create receipt events (manual entry acceptable)

### MVP Explicitly Excludes (For now)
- PDF statement parsing (bank PDFs used only as a reference artifact)
- Automated receipt OCR/parsing (manual entry first; OCR later)
- Automatic Amazon ↔ bank reconciliation as a hard requirement
- Multi-bank aggregation / Plaid-like connectivity
- Any credential storage or screen scraping

**Why this cut line works:** it delivers value quickly (bank spend + Amazon detail + receipts capture) while keeping “hard automation” as a controlled Phase 2.

---

## 5) Input Assumptions Driving Step 4, Pipeline, and UI

### 5.1 Assumptions (Based on your inventory)
- Bank CSVs are generally clean and stable (Capital One).
- Capital One history is limited (~24–25 months), so backfills are incremental.
- Amazon history is deep (10+ years) but asynchronous (1–2 week SLA).
- Amazon may reference payment instruments you don’t own/track.
- Receipts are must-have but initially unstructured.

### 5.2 Step 4 Schema Drivers (Implications)
- Need entities for:
    - `IngestionJob`, `RawRecord` (audit + idempotency)
    - `EconomicEvent` (canonical event layer)
    - `LineItem` (Amazon + receipts)
    - `Account` (bank accounts + “virtual accounts” like cash, gift card if you choose)
    - Later: `LedgerPosting` (event → financial impact)
- Need dedupe keys:
    - Bank: stable row hash from key fields
    - Amazon: Order ID + item identifiers
    - Receipts: file hash + timestamp

### 5.3 Pipeline Stage Expectations
1. **Acquire** (download/export/upload)
2. **Parse → RawRecord** (lossless preservation)
3. **Normalize → CanonicalEvent (+ LineItems)** (event-first)
4. **Enrich** (categories, merchant cleanup, user rules)
5. **Match/Reconcile (Phase 2+)** (Amazon ↔ bank, receipts ↔ bank)
6. **Project to Ledger (Step 4+)** for account/budget views

### 5.4 React UI Expectations (What the UI must support)
For MVP, the UI should expect:
- Import screens that show:
    - “What got in” (jobs, counts, warnings)
    - Per-source import history
- Views that pivot on:
    - Bank transactions by account/date/category
    - Amazon orders with item detail
    - Receipts inbox (unprocessed → processed)
- A “match later” posture:
    - Amazon order can exist without a linked bank transaction at first
    - Receipt can exist without structured amounts/categories until user fills in fields

---

## 6) Current Data Source Field Notes (Observed Fields)

### Capital One – Credit Card CSV Fields
- Transaction Date
- Posted Date
- Card No.
- Description
- Category
- Debit
- Credit

### Capital One – Checking/Savings CSV Fields
- Account Number
- Transaction Date
- Transaction Amount
- Transaction Type
- Transaction Description
- Balance

### Amazon Export Fields (Representative)
- Order ID, Order Date, Currency
- Unit Price, Taxes, Shipping, Discounts, Total Owed
- ASIN, Product Name, Condition, Quantity
- Payment Instrument Type, Order/Shipment Status, Ship Date
- Addresses, Carrier/Tracking
- Gift metadata, serial number (optional/noisy)

---
