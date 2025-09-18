import sqlite3
from contextlib import contextmanager
import uvicorn
from dotenv import load_dotenv
import os
import atexit
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tools, tool_functions

# 加载环境变量
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "CanCong-Toys API"),
    description="实用小工具合集网站API",
    debug=os.getenv("DEBUG", "False").lower() == "true"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=os.getenv("CORS_CREDENTIALS", "True").lower() == "true",
    allow_methods=os.getenv("CORS_METHODS", "*").split(","),
    allow_headers=os.getenv("CORS_HEADERS", "*").split(","),
)

# 确保正确的字符编码
app.state.encoding = "utf-8"

# 包含路由
app.include_router(tools.router)
app.include_router(tool_functions.router)

# PID文件路径
PID_FILE = "app.pid"

def save_pid():
    """保存进程ID到文件"""
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_pid():
    """删除PID文件"""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

# 注册退出处理函数
atexit.register(remove_pid)

# 初始化数据库
def init_db():
    conn = sqlite3.connect(os.getenv("DATABASE_URL", "tools.db").replace("sqlite:///", ""))
    cursor = conn.cursor()
    
    # 创建工具表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建工具使用记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tool_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_id INTEGER,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tool_id) REFERENCES tools (id)
        )
    ''')
    
    # 插入示例工具数据
    cursor.execute("SELECT COUNT(*) FROM tools")
    if cursor.fetchone()[0] == 0:
        sample_tools = [
            ("BMI计算器", "计算身体质量指数(BMI)，评估体重是否健康", "健康"),
            ("图片格式转换器", "支持多种图片格式相互转换，如JPG、PNG、GIF等", "媒体"),
            ("密码生成器", "生成安全的随机密码，可自定义长度和字符类型", "安全"),
            ("文本大小写转换", "将文本转换为大写、小写或首字母大写格式", "文本"),
            ("时间戳转换器", "将时间戳转换为可读日期，或将日期转换为时间戳", "开发"),
            ("单位换算器", "支持长度、重量、温度等多种单位换算", "计算"),
        ]
        
        cursor.executemany(
            "INSERT INTO tools (name, description, category) VALUES (?, ?, ?)",
            sample_tools
        )
    
    conn.commit()
    conn.close()

# 应用启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    save_pid()

@app.get("/")
async def root():
    return {"message": "Welcome to CanCong-Toys API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )