# Market Spark Django Server Launcher
Write-Host "=== MARKET SPARK - AI-POWERED MARKETING PLATFORM ===" -ForegroundColor Green
Write-Host "Starting Django development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Application URL: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin Panel:     http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "Credentials:     admin / admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Set working directory
Set-Location "C:\Users\user\Tinkerbell\26-Team"

# Run Django server
try {
    & "C:\Users\user\Tinkerbell\.venv\Scripts\python.exe" "manage.py" runserver "127.0.0.1:8000"
}
catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}