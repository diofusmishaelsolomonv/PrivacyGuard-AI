# Instamart Customer Intelligence & Support Copilot

A reproducible, offline-first capstone implementation connecting data quality, customer analytics, privacy-aware support triage, policy retrieval, and a tool-using refund agent. All generated data and policies are synthetic and fictional; this project is not affiliated with or connected to Swiggy Instamart.

## Repository contents

The complete project package is available in the accompanying ZIP. To keep your existing PrivacyGuard-AI repository intact, this README is added under `InstamartCopilot/` rather than replacing the root README.

## Four parts

- **Part A — Data Foundation:** clean raw CSV exports, SQLite database, seven SQL analyses and validation.
- **Part B — Customer Intelligence:** RFM segmentation, PCA, lapse prediction and retention shortlist.
- **Part C — Support Triage:** PII redaction, retries, output validation, token limits and customer-aware routing.
- **Part D — Policy RAG and Refund Agent:** TF-IDF retrieval, grounded question answering, simulated refund tools and crash recovery.

## Reproduce (from the project folder)

Use Python 3.11 or newer. On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_data.py
python run_all.py
```

`generate_data.py` and `mock_llm.py` are kept unmodified. The project uses synthetic data and an offline mock language model; no API key or paid model is required.

## Synthetic-data note

All customers, orders, tickets, policy text, and refund scenarios are artificial. Any refund actions are simulated ledger entries and do not transfer money or interact with real accounts.
