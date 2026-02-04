$ErrorActionPreference = "Stop"


$venvPython = ".\.venv\Scripts\python.exe"
$uvicorn = ".\.venv\Scripts\uvicorn.exe"
$streamlit = ".\.venv\Scripts\streamlit.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual env not found. Run: python -m venv .venv" -ForegroundColor Red
    exit 1
}

# Load .env into environment if present (do not commit secrets to repo)
if (Test-Path ".\.env") {
    Get-Content ".\.env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) { return }
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            # Safely strip surrounding single/double/backtick quotes without regex
            if ($value.Length -ge 2) {
                $first = $value[0]
                $last = $value[$value.Length - 1]
                $single = [char]39   # '
                $double = [char]34   # "
                $backtick = [char]96 # `
                if ((($first -eq $single) -and ($last -eq $single)) -or (($first -eq $double) -and ($last -eq $double)) -or (($first -eq $backtick) -and ($last -eq $backtick))) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
            }
            $envPath = 'Env:' + $key
            Set-Item -Path $envPath -Value $value
        }
    }
}

    Start-Process -FilePath $uvicorn -ArgumentList @("app.main:app", "--reload")
    Start-Sleep -Seconds 2
    Start-Process -FilePath $streamlit -ArgumentList @("run", "dashboard.py")
