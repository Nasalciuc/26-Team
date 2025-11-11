# Setup ngrok with Authentication Token for Market Spark
# Your token: 35794tZGBz1cjI2cuCaNtzhv40Y_4paVCv3RCQ9a7XYPJFyfM

Write-Host "=== NGROK SETUP WITH AUTHENTICATION ===" -ForegroundColor Green
Write-Host ""

# Step 1: Manual Download Instructions
Write-Host "STEP 1: Manual Download (Windows Defender blocks automatic download)" -ForegroundColor Yellow
Write-Host "1. Open browser and go to: https://ngrok.com/download" -ForegroundColor White
Write-Host "2. Click 'Download for Windows (64-bit)'" -ForegroundColor White
Write-Host "3. Save the file to C:\tools\ngrok\" -ForegroundColor White
Write-Host "4. Extract ngrok.exe from the zip file to C:\tools\ngrok\" -ForegroundColor White
Write-Host ""

# Step 2: Verify Installation
Write-Host "STEP 2: Verify Installation" -ForegroundColor Yellow
Write-Host "Run this command to test:" -ForegroundColor White
Write-Host "C:\tools\ngrok\ngrok.exe version" -ForegroundColor Cyan
Write-Host ""

# Step 3: Add Authentication Token
Write-Host "STEP 3: Add Your Authentication Token" -ForegroundColor Yellow
Write-Host "Run this command:" -ForegroundColor White
Write-Host "C:\tools\ngrok\ngrok.exe config add-authtoken 35794tZGBz1cjI2cuCaNtzhv40Y_4paVCv3RCQ9a7XYPJFyfM" -ForegroundColor Cyan
Write-Host ""

# Step 4: Start Tunnel for Market Spark
Write-Host "STEP 4: Start Tunnel for Market Spark" -ForegroundColor Yellow
Write-Host "With Django running on port 8000, run:" -ForegroundColor White
Write-Host "C:\tools\ngrok\ngrok.exe http 8000" -ForegroundColor Cyan
Write-Host ""

# Step 5: Update Django Settings
Write-Host "STEP 5: Update Django Settings" -ForegroundColor Yellow
Write-Host "1. Copy the public URL from ngrok (like https://abc123.ngrok-free.app)" -ForegroundColor White
Write-Host "2. Add it to ALLOWED_HOSTS in web/settings.py" -ForegroundColor White
Write-Host "3. Restart Django server" -ForegroundColor White
Write-Host ""

Write-Host "Current Status:" -ForegroundColor Green
Write-Host "✅ Authentication token ready" -ForegroundColor Green
Write-Host "❌ ngrok needs manual installation (Windows Defender blocking)" -ForegroundColor Red
Write-Host "✅ Django server working locally" -ForegroundColor Green
Write-Host ""

# Check if ngrok is already installed
if (Test-Path "C:\tools\ngrok\ngrok.exe") {
    Write-Host "NGROK FOUND! Configuring with your token..." -ForegroundColor Green
    & "C:\tools\ngrok\ngrok.exe" config add-authtoken 35794tZGBz1cjI2cuCaNtzhv40Y_4paVCv3RCQ9a7XYPJFyfM
    Write-Host ""
    Write-Host "✅ Token configured! Now run:" -ForegroundColor Green
    Write-Host "C:\tools\ngrok\ngrok.exe http 8000" -ForegroundColor Cyan
} else {
    Write-Host "Please download ngrok manually from https://ngrok.com/download" -ForegroundColor Red
    Write-Host "Extract to C:\tools\ngrok\ then run this script again" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")