import typer
import uvicorn
import os
import signal
import sys
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = typer.Typer()

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent
PID_FILE = BASE_DIR / "app.pid"

def save_pid(pid: int):
    """保存进程ID到文件"""
    with open(PID_FILE, "w") as f:
        f.write(str(pid))

def get_pid():
    """从文件获取进程ID"""
    if PID_FILE.exists():
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    return None

def remove_pid():
    """删除PID文件"""
    if PID_FILE.exists():
        PID_FILE.unlink()

def is_process_running(pid: int) -> bool:
    """检查进程是否正在运行"""
    if not pid:
        return False
    
    try:
        # 尝试向进程发送信号0，仅检查进程是否存在
        os.kill(pid, 0)
        return True
    except OSError:
        return False

@app.command()
def start(daemon: bool = typer.Option(False, "--daemon", "-d", help="以后台模式运行")):
    """启动服务"""
    pid = get_pid()
    if pid and is_process_running(pid):
        typer.echo("服务已在运行中")
        return
    
    if daemon:
        # 后台模式运行
        typer.echo("以后台模式启动服务...")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", os.getenv("HOST", "0.0.0.0"),
            "--port", str(os.getenv("PORT", 8000)),
            "--log-level", "info"
        ], cwd=BASE_DIR)
        
        save_pid(process.pid)
        typer.echo(f"服务已在后台启动 (PID: {process.pid})")
    else:
        # 前台模式运行
        typer.echo("以前台模式启动服务...")
        save_pid(os.getpid())
        try:
            uvicorn.run(
                "main:app",
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", 8000)),
                reload=os.getenv("DEBUG", "False").lower() == "true"
            )
        finally:
            remove_pid()

@app.command()
def stop():
    """停止服务"""
    pid = get_pid()
    if not pid:
        typer.echo("未找到运行中的服务")
        return
    
    if not is_process_running(pid):
        typer.echo("服务未在运行")
        remove_pid()
        return
    
    try:
        # 尝试优雅地终止进程
        os.kill(pid, signal.SIGTERM)
        # 等待一段时间看进程是否终止
        for _ in range(10):
            if not is_process_running(pid):
                break
            time.sleep(0.5)
        
        # 如果进程仍然存在，则强制终止
        if is_process_running(pid):
            os.kill(pid, signal.SIGKILL)
        
        remove_pid()
        typer.echo("服务已停止")
    except ProcessLookupError:
        typer.echo("进程不存在")
        remove_pid()
    except PermissionError:
        typer.echo("权限不足，无法终止进程")
    except Exception as e:
        typer.echo(f"停止服务时出错: {e}")

@app.command()
def restart():
    """重启服务"""
    typer.echo("重启服务...")
    stop()
    time.sleep(2)
    start()

@app.command()
def status():
    """查看服务状态"""
    pid = get_pid()
    if not pid:
        typer.echo("服务未运行")
        return
    
    if is_process_running(pid):
        typer.echo(f"服务正在运行 (PID: {pid})")
    else:
        typer.echo("服务未运行")
        remove_pid()

@app.command()
def dev():
    """开发模式启动服务（带重载功能）"""
    typer.echo("以开发模式启动服务...")
    save_pid(os.getpid())
    try:
        uvicorn.run(
            "main:app",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", 8000)),
            reload=True
        )
    finally:
        remove_pid()

if __name__ == "__main__":
    app()