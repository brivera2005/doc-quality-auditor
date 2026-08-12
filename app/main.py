from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.auditor import DocumentationAuditor
from app.measures import MEASURES
from app.models import AuditRequest, AuditResponse

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
SAMPLES = ROOT / "samples"

app = FastAPI(
    title="Doc Quality Auditor",
    description="Clinical documentation quality measure gap detector (demo / portfolio).",
    version="1.0.0",
)

auditor = DocumentationAuditor()


@app.get("/api/health")
def health():
    return {"status": "ok", "measures": len(MEASURES)}


@app.get("/api/measures")
def list_measures():
    return [
        {
            "measure_id": m.measure_id,
            "name": m.name,
            "category": m.category,
            "applies_to": list(m.applies_to),
        }
        for m in MEASURES
    ]


@app.get("/api/samples/{name}")
def get_sample(name: str):
    allowed = {"encounter-note-good", "encounter-note-gaps"}
    if name not in allowed:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Sample not found")
    path = SAMPLES / f"{name}.txt"
    return {"name": name, "content": path.read_text(encoding="utf-8")}


@app.post("/api/audit", response_model=AuditResponse)
def audit_note(request: AuditRequest):
    return auditor.audit(request)


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
