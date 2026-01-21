# Pegasus — Ingestion & Storage Architecture

## Status
Draft (v0.1)

## Purpose
This document defines the **ingestion inputs**, **source-of-truth model**, and **storage abstraction** for Pegasus v2.

The goal is to:
- Support local-first MVP development
- Enable future hosted and monetized deployments
- Avoid vendor lock-in and licensing risk
- Ensure reprocessing, deduplication, and lineage are first-class concerns

---

## Design Principles

1. **Raw artifacts are immutable and authoritative**
    - PDFs, CSVs, and images are the source of truth
    - All parsed and normalized data is derived

2. **Storage is abstracted**
    - Application code must not depend on a specific storage backend
    - Local filesystem, S3, and GCP storage are interchangeable

3. **Reprocessing is expected**
    - Parsers will improve over time
    - Historical data must be re-parsable without data loss

4. **Local-first, cloud-ready**
    - MVP runs entirely on a local machine
    - Production can migrate to cloud object storage without code changes

---

## Supported Input Types

### A. Tabular Exports
- CSV (primary)
- OFX/QFX (future)
- XLSX (future)

### B. Statements (Semi-structured)
- PDF bank statements
- PDF credit card statements
- PDF invoices (future)

### C. Unstructured Evidence
- JPEG / PNG receipts
- Screenshots or photos

### D. Programmatic Sources (Future)
- Amazon order history (CSV or API)
- Financial institution APIs

---

## Source of Truth Model

### Raw Artifacts
- Stored as immutable binary objects
- Never modified in-place
- Identified by content hash (SHA-256)

### Derived Data
- Parsed tables
- Normalized transactions
- Aggregations and analytics

Derived data **must be reproducible** from raw artifacts.

---

## BlobStore Abstraction

Pegasus uses a **BlobStore interface** to decouple ingestion logic from physical storage.

### BlobStore Responsibilities
- Store binary objects
- Retrieve objects by key
- Support listing by prefix
- Support existence checks

### Supported Backends
- Local filesystem (MVP)
- Local filesystem synced by Proton Drive
- AWS S3
- Google Cloud Storage
- S3-compatible alternatives (e.g., R2)

### BlobStore Interface (Conceptual)

