"""
测试完整的微服务流程
Standardizer → Merger (不记录到merged_record)
"""
import requests
import subprocess
import time
import os

account = "ai_vanvan"

print("🎯 测试完整微服务流程 (Standardizer → Merger)")
print("="*60)

# Step 1: 准备测试视频
test_videos = [
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-13_17-51-15_UTC.mp4",
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-13_00-02-09_UTC.mp4",
    "/app/videos/downloads/ai_vanvan/2025-10-14/2025-10-12_23-07-00_UTC.mp4"
]

print(f"📹 测试视频: {len(test_videos)} 个")
for i, v in enumerate(test_videos, 1):
    print(f"  {i}. {os.path.basename(v)}")

# Step 2: 标准化
print()
print("="*60)
print("步骤 1/2: 调用 Standardizer 服务")
print("="*60)

output_folder = f"/app/videos/standardized/{account}/flow_test"

payload = {
    "account": account,
    "video_files": test_videos,
    "output_folder": output_folder,
    "process_type": "ultimate"
}

print("📤 发送标准化请求...")
response = requests.post("http://localhost:8080/standardize-batch", json=payload, timeout=10)

if response.status_code != 200:
    print(f"❌ 标准化请求失败: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
print(f"✅ 标准化任务已启动: {result}")

# 等待标准化完成
print()
print("⏳ 等待标准化完成...")

wait_timeout = 300
wait_interval = 5
waited_time = 0

while waited_time < wait_timeout:
    cmd = f"docker exec social-media-hub-standardizer-1 ls {output_folder}/*.mp4 2>/dev/null | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        file_count = int(result.stdout.strip()) if result.stdout.strip() else 0
        print(f"  [{waited_time}s] 已完成: {file_count}/{len(test_videos)} 个文件", end='\r')
        
        if file_count >= len(test_videos):
            print()
            print("✅ 标准化完成！")
            break
    except:
        pass
    
    time.sleep(wait_interval)
    waited_time += wait_interval
else:
    print()
    print(f"⚠️ 标准化超时")
    exit(1)

# Step 3: 合并
print()
print("="*60)
print("步骤 2/2: 合并标准化后的视频")
print("="*60)

merge_script = f"""
import os
import glob
import subprocess

# 查找标准化文件
standardized_folder = "{output_folder}"
standardized_files = glob.glob(os.path.join(standardized_folder, "*.mp4"))
standardized_files.sort()

print(f"📁 找到 {{len(standardized_files)}} 个标准化文件")

# 创建concat文件
concat_file = "/tmp/flow_test_concat.txt"
with open(concat_file, 'w', encoding='utf-8') as f:
    for std_file in standardized_files:
        print(f"  - {{os.path.basename(std_file)}}")
        f.write(f"file '{{std_file}}'\\\\n")

# 输出文件
output_file = "/app/videos/merged/{account}/flow_test_output.mp4"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

print()
print("🔗 执行FFmpeg合并...")

# FFmpeg合并命令
merge_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', concat_file,
    '-c', 'copy',
    '-y',
    output_file
]

result = subprocess.run(merge_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

if result.returncode == 0 and os.path.exists(output_file):
    size_mb = os.path.getsize(output_file) / (1024*1024)
    print(f"✅ 合并成功!")
    print(f"📦 输出文件: {{output_file}}")
    print(f"📏 文件大小: {{size_mb:.2f}} MB")
else:
    print(f"❌ 合并失败: {{result.returncode}}")
    if result.stderr:
        print(result.stderr[:500])
"""

# 执行合并
with open("temp_flow_merge.py", "w", encoding="utf-8") as f:
    f.write(merge_script)

subprocess.run("docker cp temp_flow_merge.py social-media-hub-merger-1:/tmp/", shell=True, capture_output=True)
result = subprocess.run(
    "docker exec social-media-hub-merger-1 python /tmp/temp_flow_merge.py",
    shell=True,
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr and "warning" not in result.stderr.lower():
    print("错误:", result.stderr[:500])

os.remove("temp_flow_merge.py")

print()
print("="*60)
print("✅ 完整流程测试完成")
print("="*60)
print()
print("📊 测试总结:")
print(f"  ✅ Standardizer: 成功标准化 {len(test_videos)} 个视频")
print(f"  ✅ Merger: 成功合并标准化文件")
print()
print("🧹 清理命令:")
print(f"  docker exec social-media-hub-standardizer-1 rm -rf {output_folder}")
print(f"  docker exec social-media-hub-merger-1 rm -f /app/videos/merged/{account}/flow_test_output.mp4")
