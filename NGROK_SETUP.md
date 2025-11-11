# NGROK Installation Guide for Market Spark

Windows Defender is blocking automatic ngrok installation. Here's how to install it manually:

## Manual Installation Steps:

### Step 1: Download ngrok
1. Go to https://ngrok.com/download
2. Download "Windows (64-bit)" version
3. Save it to your Downloads folder

### Step 2: Extract ngrok
1. Right-click the downloaded zip file
2. Select "Extract All..."
3. Extract to: `C:\tools\ngrok\`
4. You should have: `C:\tools\ngrok\ngrok.exe`

### Step 3: Test ngrok
Open PowerShell and run:
```powershell
C:\tools\ngrok\ngrok.exe version
```

### Step 4: Start tunnel for Market Spark
With Django server running on port 8000:
```powershell
C:\tools\ngrok\ngrok.exe http 8000
```

### Step 5: Configure Django
1. Copy the public URL from ngrok (like: https://abc123.ngrok-free.app)
2. Add it to Django settings in `web/settings.py`:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'abc123.ngrok-free.app',  # Your ngrok URL
]
```
3. Restart Django server

## Alternative: Use ngrok account (recommended)
1. Create account at https://ngrok.com/
2. Get your auth token from dashboard
3. Run: `C:\tools\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN`

## Current Status:
- ✅ Market Spark Django app is running locally
- ❌ ngrok blocked by Windows Defender
- ⚠️ Facebook posting won't work without public URL

For development and testing, you can use the app locally without ngrok.
For Facebook integration, manual ngrok installation is required.