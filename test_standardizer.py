"""
测试 Standardizer 服务
单独测试视频标准化功能
"""
import requests
import time
import os
import glob

# 准备测试数据
account = "ai_vanvan"
test_videos = [
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-13_17-51-15_UTC.mp4",
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-13_00-02-09_UTC.mp4",
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-12_23-07-00_UTC.mp4"
]

output_folder = f"/app/videos/standardized/{account}/test"

print("🎨 测试 Standardizer 服务")
print("="*60)
print(f"账户: {account}")
print(f"测试视频数: {len(test_videos)}")
print(f"输出文件夹: {output_folder}")
print(f"处理类型: ultimate (终极标准化)")
print()

# 构建请求
url = "http://localhost:8080/standardize-batch"
payload = {
    "account": account,
    "video_files": test_videos,
    "output_folder": output_folder,
    "process_type": "ultimate"
}

print("📤 发送标准化请求...")
try:
    response = requests.post(url, json=payload, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 请求成功: {result}")
        print()
        
        # 等待处理完成
        print("⏳ 等待标准化完成...")
        print("提示: 可以用 docker logs -f social-media-hub-standardizer-1 查看实时日志")
        
        # 轮询检查输出文件
        wait_timeout = 300  # 5分钟
        wait_interval = 5
        waited_time = 0
        
        while waited_time < wait_timeout:
            # 检查容器内的文件
            import subprocess
            cmd = f"docker exec social-media-hub-standardizer-1 ls {output_folder} 2>/dev/null | grep .mp4 | wc -l"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                file_count = int(result.stdout.strip()) if result.stdout.strip() else 0
                
                print(f"  [{waited_time}s] 已完成: {file_count}/{len(test_videos)} 个文件")
                
                if file_count >= len(test_videos):
                    print()
                    print("✅ 所有视频标准化完成！")
                    
                    # 显示文件列表
                    cmd_ls = f"docker exec social-media-hub-standardizer-1 ls -lh {output_folder}"
                    result_ls = subprocess.run(cmd_ls, shell=True, capture_output=True, text=True)
                    print("\n标准化文件列表:")
                    print(result_ls.stdout)
                    break
                    
            except Exception as e:
                print(f"  检查失败: {e}")
            
            time.sleep(wait_interval)
            waited_time += wait_interval
        else:
            print(f"\n⚠️ 等待超时 ({wait_timeout}s)")
            
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"❌ 请求异常: {e}")

print()
print("="*60)
print("测试完成")
print("清理命令: docker exec social-media-hub-standardizer-1 rm -rf " + output_folder)
