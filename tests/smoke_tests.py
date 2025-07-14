import pytest
import requests
import time
from typing import Optional

class SmokeTests:
    """烟雾测试类 - 用于验证部署后的基本功能"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # 设置超时时间
        self.session.timeout = 30
    
    def test_api_health(self):
        """测试API健康检查端点"""
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        print(f"✅ Health check passed: {data}")
    
    def test_api_root(self):
        """测试API根端点"""
        response = self.session.get(f"{self.base_url}/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "DevOps Demo API" in data["message"]
        print(f"✅ Root endpoint passed: {data['message']}")
    
    def test_api_docs_accessible(self):
        """测试API文档是否可访问"""
        response = self.session.get(f"{self.base_url}/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        print("✅ API documentation is accessible")
    
    def test_users_endpoint(self):
        """测试用户端点基本功能"""
        # 测试获取用户列表
        response = self.session.get(f"{self.base_url}/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✅ Users list endpoint working")
        
        # 测试创建用户
        user_data = {
            "name": f"测试用户-{int(time.time())}",
            "email": f"test-{int(time.time())}@example.com"
        }
        response = self.session.post(f"{self.base_url}/users", json=user_data)
        assert response.status_code == 200
        
        created_user = response.json()
        assert created_user["name"] == user_data["name"]
        assert created_user["email"] == user_data["email"]
        assert "id" in created_user
        print(f"✅ User creation working: {created_user['name']}")
        
        # 测试获取单个用户
        user_id = created_user["id"]
        response = self.session.get(f"{self.base_url}/users/{user_id}")
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == user_id
        print(f"✅ Get user by ID working: {user['name']}")
    
    def test_api_performance(self):
        """测试API基本性能"""
        start_time = time.time()
        response = self.session.get(f"{self.base_url}/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 5.0  # 响应时间应少于5秒
        
        print(f"✅ Performance test passed: {response_time:.2f}s")

def run_smoke_tests(base_url: str):
    """运行所有烟雾测试"""
    print(f"🚀 Starting smoke tests for: {base_url}")
    
    tests = SmokeTests(base_url)
    
    try:
        tests.test_api_health()
        tests.test_api_root()
        tests.test_api_docs_accessible()
        tests.test_users_endpoint()
        tests.test_api_performance()
        
        print("✅ All smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    success = run_smoke_tests(base_url)
    sys.exit(0 if success else 1)