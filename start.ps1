$ErrorActionPreference = "Stop"

$venvPython = ".\.venv\Scripts\python.exe"
$uvicorn = ".\.venv\Scripts\uvicorn.exe"
$streamlit = ".\.venv\Scripts\streamlit.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual env not found. Run: python -m venv .venv" -ForegroundColor Red
    exit 1
}

Start-Process -FilePath $uvicorn -ArgumentList "app.main:app", "--reload"
Start-Sleep -Seconds 2
Start-Process -FilePath $streamlit -ArgumentList "run", "dashboard.py"
