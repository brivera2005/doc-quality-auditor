# Doc Quality Auditor

**Clinical documentation quality measure auditor** - paste an encounter note and get a gap report with measure IDs and suggested addendum snippets.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## What it does

- Audits pasted **encounter notes** against demo **quality measures** (CMS/HEDIS-style IDs)
- Checks for documentation of **HbA1c**, **BP follow-up**, **medication reconciliation**, and more
- Returns a **gap report** with measure IDs, findings, and **suggested addendum** text
- Supports office, inpatient, and ED encounter types

> **Demo only** - keyword/rule-based checks, not certified for quality reporting.

## Quick start (Windows)

```powershell
cd C:\Users\brive\Projects\doc-quality-auditor
.\run.ps1
```

Open **http://127.0.0.1:8096**

### Manual setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8096
```

## API

| Endpoint | Description |
|----------|-------------|
| `GET /` | Auditor UI |
| `GET /api/health` | Health check |
| `GET /api/measures` | Measure catalog |
| `GET /api/samples/{name}` | Sample encounter notes |
| `POST /api/audit` | Run documentation audit |

## Project structure

```
app/
 main.py FastAPI app
 auditor.py Audit orchestration
 measures.py Quality measure rules
 models.py Pydantic schemas
static/ Note editor + gap report UI
samples/ Good vs gaps encounter notes
```

See **[PORTFOLIO.md](./PORTFOLIO.md)** for interview talking points.

## License

MIT - see [LICENSE](./LICENSE)
