# Doc Quality Auditor — local dev server (Windows)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Doc Quality Auditor — starting local server..." -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error "Python not found. Install Python 3.11+ from https://python.org and try again."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
  Write-Host "Creating virtual environment (first run)..."
  python -m venv .venv
  .\.venv\Scripts\pip install -r requirements.txt
}

Write-Host ""
Write-Host "Open in browser:  http://127.0.0.1:8096" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8096 --reload
