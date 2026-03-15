#!/usr/bin/env python3
"""
AI VanVan 容器化系统测试脚本
测试完整的流水线：下载 → 标准化 → 合并 → 上传
"""

import requests
import json
import time
import sys

class ContainerTester:
    def __init__(self, api_gateway_url="http://localhost:8080"):
        self.api_gateway_url = api_gateway_url
    
    def test_service_health(self):
        """测试服务健康状态"""
        print("🏥 检查服务健康状态...")
        try:
            response = requests.get(f"{self.api_gateway_url}/")
            if response.status_code == 200:
                print("✅ API Gateway 运行正常")
                return True
            else:
                print("❌ API Gateway 连接失败")
                return False
        except Exception as e:
            print(f"❌ 服务连接失败: {e}")
            return False
    
    def start_full_pipeline(self, account_name="ai_vanvan", max_posts=5):
        """启动完整流水线"""
        print(f"🚀 启动 {account_name} 完整流水线...")
        
        data = {
            "account": account_name,
            "max_posts": max_posts
        }
        
        try:
            response = requests.post(
                f"{self.api_gateway_url}/pipeline",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 流水线启动成功: {result['message']}")
                print(f"📋 执行步骤: {result['steps']}")
                return True
            else:
                print(f"❌ 流水线启动失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def monitor_pipeline_status(self, account_name="ai_vanvan", timeout=1800):
        """监控流水线执行状态"""
        print(f"👀 监控 {account_name} 流水线状态...")
        
        start_time = time.time()
        last_status = None
        
        while time.time() - start_time < timeout:
            try:
                # 检查上传状态（最后一步）
                response = requests.get(f"{self.api_gateway_url}/upload/status/{account_name}")
                
                if response.status_code == 200:
                    status_data = response.json()
                    current_status = status_data.get('status', 'unknown')
                    
                    if current_status != last_status:
                        print(f"📊 状态更新: {current_status}")
                        last_status = current_status
                    
                    if current_status == 'completed':
                        print(f"🎉 流水线执行完成！")
                        print(f"📄 结果: {status_data.get('result', 'N/A')}")
                        return True
                    elif current_status == 'failed':
                        print(f"❌ 流水线执行失败")
                        print(f"📄 错误: {status_data.get('error', 'N/A')}")
                        return False
                
                time.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                print(f"⚠️ 状态检查失败: {e}")
                time.sleep(5)
        
        print(f"⏰ 监控超时 ({timeout}秒)")
        return False
    
    def test_individual_services(self, account_name="ai_vanvan"):
        """测试各个独立服务"""
        print(f"🧪 测试各个独立服务...")
        
        # 1. 测试下载服务
        print("📥 测试下载服务...")
        download_data = {"account": account_name, "max_posts": 2}
        try:
            response = requests.post(f"{self.api_gateway_url}/download", json=download_data)
            if response.status_code == 200:
                print("✅ 下载服务测试通过")
            else:
                print(f"❌ 下载服务测试失败: {response.text}")
        except Exception as e:
            print(f"❌ 下载服务请求失败: {e}")
        
        time.sleep(5)
        
        # 2. 测试标准化服务
        print("🔧 测试标准化服务...")
        standardize_data = {
            "account": account_name,
            "video_folder": f"/app/downloads/{account_name}"
        }
        try:
            response = requests.post(f"{self.api_gateway_url}/standardize", json=standardize_data)
            if response.status_code == 200:
                print("✅ 标准化服务测试通过")
            else:
                print(f"❌ 标准化服务测试失败: {response.text}")
        except Exception as e:
            print(f"❌ 标准化服务请求失败: {e}")
        
        time.sleep(5)
        
        # 3. 测试合并服务
        print("🎬 测试合并服务...")
        merge_data = {"account": account_name}
        try:
            response = requests.post(f"{self.api_gateway_url}/merge", json=merge_data)
            if response.status_code == 200:
                print("✅ 合并服务测试通过")
            else:
                print(f"❌ 合并服务测试失败: {response.text}")
        except Exception as e:
            print(f"❌ 合并服务请求失败: {e}")
        
        time.sleep(5)
        
        # 4. 测试上传服务
        print("📤 测试上传服务...")
        upload_data = {"account": account_name}
        try:
            response = requests.post(f"{self.api_gateway_url}/upload", json=upload_data)
            if response.status_code == 200:
                print("✅ 上传服务测试通过")
            else:
                print(f"❌ 上传服务测试失败: {response.text}")
        except Exception as e:
            print(f"❌ 上传服务请求失败: {e}")

def main():
    print("🐳 AI VanVan 容器化系统测试")
    print("=" * 50)
    
    tester = ContainerTester()
    
    # 检查服务健康状态
    if not tester.test_service_health():
        print("❌ 服务未启动，请先运行: docker-compose up -d")
        sys.exit(1)
    
    print("\n选择测试模式:")
    print("1. 完整流水线测试")
    print("2. 独立服务测试")
    print("3. 两者都测试")
    
    choice = input("请输入选择 (1-3): ").strip()
    account_name = input("请输入账号名称 (默认: ai_vanvan): ").strip() or "ai_vanvan"
    
    if choice in ["1", "3"]:
        print(f"\n🚀 开始完整流水线测试...")
        if tester.start_full_pipeline(account_name):
            tester.monitor_pipeline_status(account_name)
    
    if choice in ["2", "3"]:
        print(f"\n🧪 开始独立服务测试...")
        tester.test_individual_services(account_name)
    
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    main()