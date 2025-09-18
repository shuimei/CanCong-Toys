@echo off
setlocal

echo Installing frontend dependencies...
call npm install

if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check your network connection and try again.
    pause
    exit /b %errorlevel%
)

echo Starting development server...
npm run dev