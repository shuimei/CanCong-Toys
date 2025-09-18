from fastapi import APIRouter, HTTPException, Query
import sqlite3
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/tools", tags=["tools"])

class Tool(BaseModel):
    id: int
    name: str
    description: str
    category: str
    usage_count: int

class ToolCreate(BaseModel):
    name: str
    description: str
    category: str

def get_db_connection():
    conn = sqlite3.connect('tools.db')
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/", response_model=List[Tool])
async def get_tools():
    """获取所有工具"""
    conn = get_db_connection()
    tools = conn.execute('SELECT * FROM tools').fetchall()
    conn.close()
    return [dict(tool) for tool in tools]

@router.get("/search", response_model=List[Tool])
async def search_tools(query: str = Query(..., min_length=1)):
    """根据关键词搜索工具"""
    conn = get_db_connection()
    tools = conn.execute('''
        SELECT * FROM tools 
        WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
        ORDER BY usage_count DESC
    ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return [dict(tool) for tool in tools]

@router.get("/popular", response_model=List[Tool])
async def get_popular_tools(limit: int = 4):
    """获取热门工具"""
    conn = get_db_connection()
    tools = conn.execute('''
        SELECT * FROM tools 
        ORDER BY usage_count DESC 
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(tool) for tool in tools]

@router.get("/recent", response_model=List[Tool])
async def get_recent_tools(limit: int = 4):
    """获取最新工具"""
    conn = get_db_connection()
    tools = conn.execute('''
        SELECT * FROM tools 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(tool) for tool in tools]

@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: int):
    """获取特定工具"""
    conn = get_db_connection()
    tool = conn.execute('SELECT * FROM tools WHERE id = ?', (tool_id,)).fetchone()
    conn.close()
    
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    # 增加工具使用次数
    conn = get_db_connection()
    conn.execute('''
        UPDATE tools 
        SET usage_count = usage_count + 1 
        WHERE id = ?
    ''', (tool_id,))
    
    conn.execute('''
        INSERT INTO tool_usage (tool_id) 
        VALUES (?)
    ''', (tool_id,))
    
    conn.commit()
    conn.close()
    
    return dict(tool)

@router.post("/", response_model=Tool)
async def create_tool(tool: ToolCreate):
    """创建新工具"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO tools (name, description, category) 
        VALUES (?, ?, ?)
    ''', (tool.name, tool.description, tool.category))
    
    tool_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return await get_tool(tool_id)