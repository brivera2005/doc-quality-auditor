# Doc Quality Auditor - Portfolio brief

**Repo:** [github.com/brivera2005/doc-quality-auditor](https://github.com/brivera2005/doc-quality-auditor)

## Elevator pitch

Paste a clinical encounter note and get an explainable quality-measure gap report - each gap includes a measure ID, finding, and a suggested addendum snippet to close the documentation hole.

## Skills demonstrated

- **Backend:** Python, FastAPI, composable measure rules, regex-based NLP-lite
- **Frontend:** Note editor, compliance summary, gap cards with addendum suggestions
- **Domain:** HEDIS/CMS measure literacy, clinical documentation improvement (CDI)
- **Engineering:** Measure catalog separated from auditor and API layers

## Interview line

*"I built a documentation quality auditor that scans encounter notes for common measure gaps - like missing A1c, BP follow-up, or med rec - and suggests addendum language for each gap."*

## Run locally in 30 seconds

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8096
```

## Disclaimer

Rule-based demo using keyword patterns. Not validated for regulatory quality reporting.
