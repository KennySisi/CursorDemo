import pytest
import requests
import time
import concurrent.futures
from typing import List, Dict

class ProductionTests:
    """生产环境测试类 - 用于验证生产环境的稳定性和性能"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
    
    def test_api_availability(self):
        """测试API可用性"""
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["environment"] in ["production", "prod"]
        print("✅ Production API is available and healthy")
    
    def test_ssl_certificate(self):
        """测试SSL证书"""
        if self.base_url.startswith('https://'):
            response = self.session.get(f"{self.base_url}/health", verify=True)
            assert response.status_code == 200
            print("✅ SSL certificate is valid")
        else:
            print("⚠️ Skipping SSL test - not using HTTPS")
    
    def test_response_headers(self):
        """测试安全响应头"""
        response = self.session.get(f"{self.base_url}/health")
        headers = response.headers
        
        # 检查基本安全头
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection'
        ]
        
        for header in security_headers:
            if header in headers:
                print(f"✅ Security header present: {header}")
            else:
                print(f"⚠️ Missing security header: {header}")
    
    def test_load_performance(self):
        """测试负载性能"""
        def make_request():
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/health")
            end_time = time.time()
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time
            }
        
        # 并发请求测试
        num_requests = 10
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # 分析结果
        successful_requests = [r for r in results if r['status_code'] == 200]
        success_rate = len(successful_requests) / len(results) * 100
        
        if successful_requests:
            avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
            max_response_time = max(r['response_time'] for r in successful_requests)
        else:
            avg_response_time = 0
            max_response_time = 0
        
        assert success_rate >= 95  # 至少95%成功率
        assert avg_response_time < 2.0  # 平均响应时间小于2秒
        assert max_response_time < 5.0  # 最大响应时间小于5秒
        
        print(f"✅ Load test passed:")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Average response time: {avg_response_time:.2f}s")
        print(f"   Max response time: {max_response_time:.2f}s")
    
    def test_database_operations(self):
        """测试数据库操作（在生产环境中谨慎操作）"""
        # 创建测试用户（使用特殊标识）
        test_user_data = {
            "name": f"PROD-TEST-{int(time.time())}",
            "email": f"prod-test-{int(time.time())}@test.internal"
        }
        
        # 创建用户
        response = self.session.post(f"{self.base_url}/users", json=test_user_data)
        assert response.status_code == 200
        
        created_user = response.json()
        user_id = created_user["id"]
        
        # 获取用户
        response = self.session.get(f"{self.base_url}/users/{user_id}")
        assert response.status_code == 200
        
        # 清理测试数据
        response = self.session.delete(f"{self.base_url}/users/{user_id}")
        assert response.status_code == 200
        
        print("✅ Database operations working correctly")
    
    def test_api_consistency(self):
        """测试API响应一致性"""
        responses = []
        
        # 多次请求同一端点
        for _ in range(5):
            response = self.session.get(f"{self.base_url}/health")
            assert response.status_code == 200
            responses.append(response.json())
            time.sleep(0.1)
        
        # 检查响应结构一致性
        first_response = responses[0]
        for response in responses[1:]:
            assert set(response.keys()) == set(first_response.keys())
            assert response["status"] == first_response["status"]
            assert response["version"] == first_response["version"]
        
        print("✅ API responses are consistent")
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试404错误
        response = self.session.get(f"{self.base_url}/nonexistent-endpoint")
        assert response.status_code == 404
        
        # 测试用户不存在的情况
        response = self.session.get(f"{self.base_url}/users/99999")
        assert response.status_code == 404
        
        # 测试无效数据
        invalid_user_data = {
            "name": "",  # 空名称
            "email": "invalid-email"  # 无效邮箱
        }
        response = self.session.post(f"{self.base_url}/users", json=invalid_user_data)
        assert response.status_code in [400, 422]  # 客户端错误
        
        print("✅ Error handling working correctly")

def run_production_tests(base_url: str):
    """运行所有生产环境测试"""
    print(f"🏭 Starting production tests for: {base_url}")
    
    tests = ProductionTests(base_url)
    
    try:
        tests.test_api_availability()
        tests.test_ssl_certificate()
        tests.test_response_headers()
        tests.test_load_performance()
        tests.test_database_operations()
        tests.test_api_consistency()
        tests.test_error_handling()
        
        print("✅ All production tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Production test failed: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    success = run_production_tests(base_url)
    sys.exit(0 if success else 1)