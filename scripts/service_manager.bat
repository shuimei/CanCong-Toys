@echo off
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0.."
set "BACKEND_DIR=%PROJECT_DIR%\backend"

title CanCong-Toys Service Manager

echo ==========================================
echo     CanCong-Toys 服务管理脚本
echo ==========================================
echo.

:MENU
echo 请选择操作:
echo 1. 启动服务
echo 2. 停止服务
echo 3. 重启服务
echo 4. 查看服务状态
echo 5. 后台启动服务
echo 6. 开发模式启动
echo 7. 退出
echo.

set /p choice=请输入选项 (1-7): 

if "%choice%"=="1" goto START_SERVICE
if "%choice%"=="2" goto STOP_SERVICE
if "%choice%"=="3" goto RESTART_SERVICE
if "%choice%"=="4" goto CHECK_STATUS
if "%choice%"=="5" goto BACKGROUND_START
if "%choice%"=="6" goto DEV_MODE
if "%choice%"=="7" goto EXIT

echo 无效选项，请重新选择
echo.
goto MENU

:START_SERVICE
echo.
echo 正在启动 CanCong-Toys 服务...
cd /d "%BACKEND_DIR%"
python cli.py start
goto MENU

:STOP_SERVICE
echo.
echo 正在停止 CanCong-Toys 服务...
cd /d "%BACKEND_DIR%"
python cli.py stop
goto MENU

:RESTART_SERVICE
echo.
echo 正在重启 CanCong-Toys 服务...
cd /d "%BACKEND_DIR%"
python cli.py restart
goto MENU

:CHECK_STATUS
echo.
echo 正在检查 CanCong-Toys 服务状态...
cd /d "%BACKEND_DIR%"
python cli.py status
goto MENU

:BACKGROUND_START
echo.
echo 正在后台启动 CanCong-Toys 服务...
cd /d "%BACKEND_DIR%"
python cli.py start --daemon
goto MENU

:DEV_MODE
echo.
echo 以开发模式启动 CanCong-Toys 服务...
cd /d "%BACKEND_DIR%"
python cli.py dev
goto MENU

:EXIT
echo.
echo 感谢使用 CanCong-Toys 服务管理器！
exit /b