"""
测试合并和上传功能
"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"
ACCOUNT = "ai_vanvan"

def print_separator(title=""):
    print("\n" + "=" * 60)
    if title:
        print(f"🎯 {title}")
        print("=" * 60)

def check_response(response, step_name):
    """检查响应状态"""
    print(f"\n{'✅' if response.status_code == 200 else '❌'} {step_name}")
    print(f"   状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"   响应: {json.dumps(data, indent=3, ensure_ascii=False)}")
        return data
    except:
        print(f"   响应: {response.text}")
        return None

def main():
    print_separator("测试合并和上传功能")
    
    # 步骤1: 合并视频
    print_separator("步骤1: 合并标准化后的视频")
    print(f"🎬 合并账号 {ACCOUNT} 的标准化视频...")
    print(f"📁 源目录: /app/videos/downloads/{ACCOUNT}/2025-10-31/standardized/")
    
    merge_data = {
        "account": ACCOUNT,
        "video_folder": f"/app/videos/downloads/{ACCOUNT}/2025-10-31/standardized/",
        "limit": 5  # 合并最新的5个视频
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/merge",
            json=merge_data
        )
        result = check_response(resp, "视频合并")
        
        if result:
            print(f"\n⏳ 等待 30 秒让合并完成...")
            time.sleep(30)
            
            # 检查合并状态
            print("\n🔍 检查合并状态...")
            status_resp = requests.get(f"{BASE_URL}/merge/status/{ACCOUNT}")
            check_response(status_resp, "合并状态查询")
    except Exception as e:
        print(f"❌ 合并失败: {e}")
        return
    
    # 步骤2: 上传视频
    print_separator("步骤2: 上传到B站")
    print(f"📤 上传账号 {ACCOUNT} 的合并视频...")
    
    upload_data = {
        "account": ACCOUNT,
        "platform": "bilibili",
        "video_file": "auto"  # 自动查找最新合并的视频
    }
    
    try:
        resp = requests.post(
            f"{BASE_URL}/upload",
            json=upload_data
        )
        result = check_response(resp, "视频上传")
        
        if result:
            print(f"\n⏳ 等待 60 秒让上传启动...")
            time.sleep(60)
            
            # 检查上传状态
            print("\n🔍 检查上传状态...")
            status_resp = requests.get(f"{BASE_URL}/upload/status/{ACCOUNT}")
            check_response(status_resp, "上传状态查询")
    except Exception as e:
        print(f"❌ 上传失败: {e}")
    
    print_separator("测试完成")
    print("\n💡 提示:")
    print("   - 查看合并日志: docker logs -f social-media-hub-merger-1")
    print("   - 查看上传日志: docker logs -f social-media-hub-uploader-1")
    print("   - 查看所有日志: docker-compose logs -f")

if __name__ == "__main__":
    main()
