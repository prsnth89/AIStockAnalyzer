# Quick Start Script - AI Stock Analyzer
# Run this script to start the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Stock Analyzer - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "[2/3] Checking dependencies..." -ForegroundColor Green
$flask = pip show flask 2>$null
if (-Not $flask) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start Flask server
Write-Host "[3/3] Starting Flask server..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Server starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open your browser and go to:" -ForegroundColor Green
Write-Host "  http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available tickers: AAPL, MSFT, GOOGL" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

cd src
python app.py
