@echo off
cd /d C:\Users\Administrator\Desktop\MBPI-Projects\Warehouse-Program-Backend-API
echo Starting FastAPI server...
C:\Users\Administrator\Desktop\MBPI-Projects\Warehouse-Program-Backend-API\venv\Scripts\python.exe -m uvicorn backend._app.main:app --host 0.0.0.0 --port 8000 --workers 2
pause
