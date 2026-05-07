Set-StrictMode -Version Latest

function Test-Command($Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

Write-Host "NyayPath prerequisite check" -ForegroundColor Cyan
Write-Host ""

$pythonOk = Test-Command "python"
$pyOk = Test-Command "py"
$nodeOk = Test-Command "node"
$npmOk = Test-Command "npm"

if ($pythonOk) {
    Write-Host "[OK] python found:" -ForegroundColor Green
    python --version
} elseif ($pyOk) {
    Write-Host "[OK] py launcher found:" -ForegroundColor Green
    py --version
} else {
    Write-Host "[MISSING] Python was not found." -ForegroundColor Red
    Write-Host "Install Python 3.11+ and enable 'Add python.exe to PATH'."
}

if ($nodeOk) {
    Write-Host "[OK] node found:" -ForegroundColor Green
    node --version
} else {
    Write-Host "[MISSING] Node.js was not found." -ForegroundColor Red
    Write-Host "Install Node.js LTS from https://nodejs.org/."
}

if ($npmOk) {
    Write-Host "[OK] npm found:" -ForegroundColor Green
    npm --version
} else {
    Write-Host "[MISSING] npm was not found." -ForegroundColor Red
    Write-Host "npm is installed with Node.js LTS."
}

Write-Host ""
Write-Host "After installing missing tools, close PowerShell and open a new one." -ForegroundColor Yellow

