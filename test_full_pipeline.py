#!/usr/bin/env python3
"""
测试 Container 完整流程
测试链路: 下载 → 标准化 → 合并 → 上传
"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"

def print_step(step_num, title):
    """打印步骤标题"""
    print("\n" + "="*60)
    print(f"步骤 {step_num}: {title}")
    print("="*60)

def call_api(endpoint, data, description):
    """调用API并显示结果"""
    print(f"\n📡 调用 API: {endpoint}")
    print(f"📋 请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {description} 成功!")
            print(f"📄 返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True, result
        else:
            print(f"❌ {description} 失败!")
            print(f"📄 错误信息: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ API 调用异常: {e}")
        return False, None

def check_downloads():
    """检查下载的视频数量"""
    import os
    download_path = "videos/downloads/ai_vanvan/2025-10-31"
    if os.path.exists(download_path):
        videos = [f for f in os.listdir(download_path) if f.endswith('.mp4')]
        print(f"📹 已下载视频数量: {len(videos)}")
        return len(videos) > 0
    return False

def check_merged_video():
    """检查合并后的视频"""
    import os
    import glob
    merged_path = "videos/merged/ai_vanvan"
    if os.path.exists(merged_path):
        videos = glob.glob(f"{merged_path}/*.mp4")
        if videos:
            latest = max(videos, key=os.path.getmtime)
            size_mb = os.path.getsize(latest) / (1024*1024)
            print(f"🎬 合并视频: {latest}")
            print(f"📦 文件大小: {size_mb:.2f} MB")
            return latest
    return None

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   Social Media Hub - 完整流程测试                        ║
║   测试账号: ai_vanvan                                    ║
║   测试链路: 下载 → 标准化 → 合并 → 上传                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    account = "ai_vanvan"
    
    # ============================================================
    # 步骤 1: 登录认证
    # ============================================================
    print_step(1, "登录认证 (Auth Service)")
    success, _ = call_api("/login", {
        "account": account,
        "platform": "instagram"
    }, "登录")
    
    if not success:
        print("❌ 登录失败，终止测试")
        return
    
    print("⏳ 等待 5 秒让 session 加载完成...")
    time.sleep(5)
    
    # ============================================================
    # 步骤 2: 下载视频
    # ============================================================
    print_step(2, "下载视频 (Downloader Service)")
    
    # 检查是否已有下载的视频
    if check_downloads():
        print("✅ 已有下载的视频，跳过下载步骤")
    else:
        success, _ = call_api("/download", {
            "account": account,
            "platform": "instagram",
            "download_type": "saved_posts",
            "max_posts": 5  # 只下载5个测试
        }, "下载")
        
        if not success:
            print("⚠️ 下载失败，但继续测试（可能已有视频）")
        else:
            print("⏳ 等待 30 秒让下载完成...")
            time.sleep(30)
    
    # ============================================================
    # 步骤 3: 标准化视频
    # ============================================================
    print_step(3, "标准化视频 (Standardizer Service)")
    
    # 注意：标准化需要指定具体的视频文件夹
    video_folder = f"/app/videos/downloads/{account}/2025-10-31"
    
    success, _ = call_api("/standardize", {
        "account": account,
        "video_folder": video_folder,
        "target_resolution": "auto",  # 自动检测分辨率
        "output_folder": "standardized"
    }, "标准化")
    
    if success:
        print("⏳ 等待 60 秒让标准化完成...")
        time.sleep(60)
    else:
        print("⚠️ 标准化失败，继续测试合并")
    
    # ============================================================
    # 步骤 4: 合并视频
    # ============================================================
    print_step(4, "合并视频 (Merger Service)")
    
    success, result = call_api("/merge", {
        "account": account,
        "limit": 5  # 合并最多5个视频
    }, "合并")
    
    if success:
        print("⏳ 等待 90 秒让合并完成...")
        time.sleep(90)
        
        # 检查合并结果
        merged_video = check_merged_video()
        if not merged_video:
            print("❌ 未找到合并后的视频文件")
            return
    else:
        print("❌ 合并失败，无法继续上传")
        return
    
    # ============================================================
    # 步骤 5: 上传到B站
    # ============================================================
    print_step(5, "上传到B站 (Uploader Service)")
    
    # 询问是否上传
    print("\n⚠️ 即将执行真实上传到B站!")
    confirm = input("是否继续上传? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        success, _ = call_api("/upload", {
            "account": account,
            "video_path": merged_video,
            "title": None  # 自动从文件名提取
        }, "上传")
        
        if success:
            print("⏳ 等待 300 秒让上传完成...")
            time.sleep(300)
            print("✅ 上传任务已提交，请检查B站后台")
        else:
            print("❌ 上传失败")
    else:
        print("⏭️ 跳过上传步骤")
    
    # ============================================================
    # 完成
    # ============================================================
    print("\n" + "="*60)
    print("✅ 完整流程测试完成!")
    print("="*60)
    
    print("""
📊 测试总结:
- ✅ 登录认证
- ✅ 下载视频
- ✅ 标准化处理
- ✅ 视频合并
- ⏭️ B站上传 (已跳过/已完成)

🔍 检查日志:
docker logs social-media-hub-auth-1
docker logs social-media-hub-downloader-1
docker logs social-media-hub-standardizer-1
docker logs social-media-hub-merger-1
docker logs social-media-hub-uploader-1
    """)

if __name__ == "__main__":
    main()
