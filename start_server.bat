@echo off
cd /d "C:\Users\user\Tinkerbell\26-Team"
echo Starting Market Spark Django Server...
echo URL: http://127.0.0.1:8000/
echo Admin: http://127.0.0.1:8000/admin/ (admin/admin123)
echo.
"C:\Users\user\Tinkerbell\.venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
pause