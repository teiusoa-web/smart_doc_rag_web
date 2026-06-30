$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT

Write-Host "Starting Smart Document RAG Web..." -ForegroundColor Cyan

# Check Ollama
$ollamaRunning = $false
try {
    $result = ollama list 2>&1
    if ($LASTEXITCODE -eq 0) {
        $ollamaRunning = $true
        Write-Host "✓ Ollama OK" -ForegroundColor Green
    }
} catch {
    Write-Host "Ollama not running" -ForegroundColor Yellow
}

if (-not $ollamaRunning) {
    Write-Host "Starting Ollama..." -ForegroundColor Yellow
    Start-Process powershell -NoNewWindow -ArgumentList {ollama serve}
    Start-Sleep -Seconds 5
}

# Pull models if missing
Write-Host "Checking models..." -ForegroundColor Cyan
$models = ollama list 2>&1
$output = $models | Out-String

if ($output -notmatch "nomic-embed-text") {
    Write-Host "Pulling nomic-embed-text..." -ForegroundColor Yellow
    ollama pull nomic-embed-text
} else {
    Write-Host "✓ nomic-embed-text exists" -ForegroundColor Green
}

if ($output -notmatch "llama3.2") {
    Write-Host "Pulling llama3.2..." -ForegroundColor Yellow
    ollama pull llama3.2
} else {
    Write-Host "✓ llama3.2 exists" -ForegroundColor Green
}

# Start backend terminal
$backendScript = @"
cd `"$ROOT`"
Set-ExecutionPolicy Bypass -Scope Process -Force
.\.venv\Scripts\Activate.ps1
Write-Host "Backend starting..." -ForegroundColor Green
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
"@

$backendScriptPath = Join-Path $ROOT "start_backend.ps1"
$backendScript | Out-File -FilePath $backendScriptPath -Encoding UTF8 -Force

Start-Process powershell -ArgumentList "-NoExit", "-File", $backendScriptPath

Start-Sleep -Seconds 3

# Start frontend terminal
$frontendScript = @"
cd `"$ROOT\frontend`"
npm run dev
"@

$frontendScriptPath = Join-Path $ROOT "start_frontend.ps1"
$frontendScript | Out-File -FilePath $frontendScriptPath -Encoding UTF8 -Force

Start-Process powershell -ArgumentList "-NoExit", "-File", $frontendScriptPath

Start-Sleep -Seconds 5

Start-Process "http://127.0.0.1:5173"
Start-Process "http://127.0.0.1:8000/docs"

Write-Host "Started successfully." -ForegroundColor Green
Write-Host "Backend:  http://127.0.0.1:8000/docs"
Write-Host "Frontend: http://127.0.0.1:5173"