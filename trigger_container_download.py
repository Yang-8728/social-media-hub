import requests
import json
import time

# API Gateway地址
API_BASE = "http://localhost:8080"

def trigger_full_pipeline(account_name, max_posts=20):
    """触发完整的下载流程"""
    print("=" * 60)
    print(f"🚀 启动 {account_name} 的完整下载流程")
    print("=" * 60)
    
    # 步骤1: 登录认证
    print("\n📱 步骤1: 发送登录任务...")
    try:
        response = requests.post(
            f"{API_BASE}/login",
            json={"account": account_name}
        )
        print(f"   状态: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"   ❌ 登录任务发送失败: {e}")
        return False
    
    # 等待登录完成
    print("\n⏳ 等待5秒让登录完成...")
    time.sleep(5)
    
    # 步骤2: 启动下载任务
    print(f"\n📥 步骤2: 发送下载任务 (最多{max_posts}个帖子)...")
    try:
        response = requests.post(
            f"{API_BASE}/download",
            json={
                "account": account_name,
                "max_posts": max_posts,
                "type": "saved_posts"
            }
        )
        print(f"   状态: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"   ❌ 下载任务发送失败: {e}")
        return False
    
    print("\n✅ 所有任务已发送！")
    print("\n💡 提示:")
    print("   - 查看下载进度: docker-compose logs -f downloader")
    print("   - 查看认证进度: docker-compose logs -f auth")
    print("   - 查看所有日志: docker-compose logs -f")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    # 触发 ai_vanvan 的下载任务
    trigger_full_pipeline("ai_vanvan", max_posts=20)
