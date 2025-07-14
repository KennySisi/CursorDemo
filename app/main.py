from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

# 创建FastAPI应用实例
app = FastAPI(
    title="DevOps Demo API",
    description="一个用于演示CI/CD流程的FastAPI应用",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    environment: str

class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

# 模拟数据库
fake_users_db: List[User] = []
user_id_counter = 1

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "欢迎使用DevOps Demo API！",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.get("/users", response_model=List[User])
async def get_users():
    """获取所有用户"""
    return fake_users_db

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """创建新用户"""
    global user_id_counter
    
    # 检查邮箱是否已存在
    for existing_user in fake_users_db:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="邮箱已存在")
    
    new_user = User(
        id=user_id_counter,
        name=user.name,
        email=user.email,
        created_at=datetime.now().isoformat()
    )
    
    fake_users_db.append(new_user)
    user_id_counter += 1
    
    return new_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据ID获取用户"""
    for user in fake_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="用户未找到")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    global fake_users_db
    for i, user in enumerate(fake_users_db):
        if user.id == user_id:
            deleted_user = fake_users_db.pop(i)
            return {"message": f"用户 {deleted_user.name} 已删除"}
    raise HTTPException(status_code=404, detail="用户未找到")

if __name__ == "__main__":
    # 本地开发时运行
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )