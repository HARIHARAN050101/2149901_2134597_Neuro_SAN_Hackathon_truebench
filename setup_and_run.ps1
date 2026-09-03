# setup_and_run.ps1
# Save this file INSIDE the neuro-san-studio folder and run it from there.
# Usage:  .\setup_and_run.ps1  -OpenAIKey "sk-..."
# Run PowerShell AS ADMINISTRATOR (right-click -> Run as Administrator) before executing this.

param(
    [string]$OpenAIKey = ""
)

$ErrorActionPreference = "Stop"

Write-Host "== 1. Killing any stray python processes ==" -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "== 2. Locating sibling truebench-agentic folder ==" -ForegroundColor Cyan
$src = "..\truebench-agentic"
if (-not (Test-Path $src)) {
    Write-Host "ERROR: Could not find $src relative to current folder. Run this script from inside neuro-san-studio, with truebench-agentic as its sibling." -ForegroundColor Red
    exit 1
}

Write-Host "== 3. Copying TrueBench agent network + tools (force overwrite) ==" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path .\registries | Out-Null
New-Item -ItemType Directory -Force -Path .\coded_tools | Out-Null

if (Test-Path .\registries\truebench) { Remove-Item -Recurse -Force .\registries\truebench }
Copy-Item -Recurse -Force "$src\registries\truebench" .\registries\

Copy-Item -Force "$src\registries\manifest.hocon" .\registries\manifest.hocon

if (Test-Path .\coded_tools\truebench_agent_network) { Remove-Item -Recurse -Force .\coded_tools\truebench_agent_network }
Copy-Item -Recurse -Force "$src\coded_tools\truebench_agent_network" .\coded_tools\

Write-Host "== 4. Verifying copy ==" -ForegroundColor Cyan
$manifestOk = Test-Path .\registries\manifest.hocon
$hoconOk = Test-Path .\registries\truebench\truebench_agent_network.hocon
$toolsOk = (Get-ChildItem .\coded_tools\truebench_agent_network -Filter "*.py" -ErrorAction SilentlyContinue).Count -ge 7

Write-Host "manifest.hocon present: $manifestOk"
Write-Host "truebench_agent_network.hocon present: $hoconOk"
Write-Host "coded tool .py files present (>=7): $toolsOk"

if (-not ($manifestOk -and $hoconOk -and $toolsOk)) {
    Write-Host "ERROR: One or more required files are missing after copy. Stopping." -ForegroundColor Red
    exit 1
}

Write-Host "== 5. Activating virtual environment ==" -ForegroundColor Cyan
if (-not (Test-Path .\venv\Scripts\Activate.ps1)) {
    Write-Host "No venv found — creating one and installing requirements (first run only)..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
} else {
    & .\venv\Scripts\Activate.ps1
}

Write-Host "== 6. Setting environment variables ==" -ForegroundColor Cyan
if ($OpenAIKey -ne "") {
    $env:OPENAI_API_KEY = $OpenAIKey
} elseif (-not $env:OPENAI_API_KEY) {
    Write-Host "WARNING: No -OpenAIKey passed and OPENAI_API_KEY is not already set in this session." -ForegroundColor Yellow
    Write-Host "The server may start, but agent calls needing the LLM will fail without it." -ForegroundColor Yellow
}
$env:AGENT_MANIFEST_FILE = ".\registries\manifest.hocon"
$env:AGENT_TOOL_PATH = ".\coded_tools"

Write-Host "== 7. Starting the server (this will occupy this terminal) ==" -ForegroundColor Cyan
Write-Host "Once it prints 'nsflow client started on localhost:XXXX' and 'NeuroSan server http started on port: YYYY'," -ForegroundColor Green
Write-Host "open the nsflow URL in your browser, set Host=localhost / Port=YYYY, click CONNECT, then select" -ForegroundColor Green
Write-Host "'truebench/truebench_agent_network' under Available Agents." -ForegroundColor Green
Write-Host ""

python -m neuro_san_studio run
