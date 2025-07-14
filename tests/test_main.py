import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "DevOps Demo API" in data["message"]

def test_health_check():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

def test_get_users_empty():
    """测试获取用户列表（空列表）"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    """测试创建用户"""
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data

def test_create_duplicate_user():
    """测试创建重复用户（应该失败）"""
    user_data = {
        "name": "李四",
        "email": "lisi@example.com"
    }
    # 第一次创建
    client.post("/users", json=user_data)
    # 第二次创建相同邮箱
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert "邮箱已存在" in response.json()["detail"]

def test_get_user_by_id():
    """测试根据ID获取用户"""
    # 先创建一个用户
    user_data = {
        "name": "王五",
        "email": "wangwu@example.com"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # 获取用户
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

def test_get_nonexistent_user():
    """测试获取不存在的用户"""
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert "用户未找到" in response.json()["detail"]

def test_delete_user():
    """测试删除用户"""
    # 先创建一个用户
    user_data = {
        "name": "赵六",
        "email": "zhaoliu@example.com"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # 删除用户
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert "已删除" in response.json()["message"]
    
    # 验证用户已被删除
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404