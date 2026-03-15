"""
测试 Merger 服务
假设视频已经标准化，测试合并功能
"""
import requests
import subprocess
import os

account = "ai_vanvan"

print("🔗 测试 Merger 服务 (合并已标准化的视频)")
print("="*60)

# 首先检查是否有标准化文件
print("📋 检查标准化文件...")
cmd = f"docker exec social-media-hub-standardizer-1 ls /app/videos/standardized/{account}/test/*.mp4 2>/dev/null"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if result.returncode != 0:
    print("❌ 没有找到标准化文件")
    print("请先运行: python test_standardizer.py")
    exit(1)

files = result.stdout.strip().split('\n')
print(f"✅ 找到 {len(files)} 个标准化文件")
for f in files:
    print(f"  - {os.path.basename(f)}")

print()
print("🔗 开始合并测试...")
print("注意: 这个测试只验证合并逻辑，不会生成最终输出")
print()

# 创建测试脚本在merger容器中执行
test_script = """
import os
import glob
import subprocess

# 查找标准化文件
standardized_folder = "/app/videos/standardized/ai_vanvan/test"
standardized_files = glob.glob(os.path.join(standardized_folder, "*.mp4"))
standardized_files.sort()

print(f"找到 {len(standardized_files)} 个标准化文件")

if not standardized_files:
    print("没有文件可合并")
    exit(1)

# 创建concat文件
concat_file = "/tmp/test_concat.txt"
with open(concat_file, 'w', encoding='utf-8') as f:
    for std_file in standardized_files:
        f.write(f"file '{std_file}'\\n")

print(f"已创建concat文件: {concat_file}")

# 输出文件
output_file = "/app/videos/merged/ai_vanvan/test_merge.mp4"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

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

print(f"执行FFmpeg合并...")
result = subprocess.run(merge_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

if result.returncode == 0 and os.path.exists(output_file):
    size_mb = os.path.getsize(output_file) / (1024*1024)
    print(f"✅ 合并成功! 输出: {output_file} ({size_mb:.1f}MB)")
else:
    print(f"❌ 合并失败")
    print(result.stderr[:500])
"""

# 写入临时文件
with open("temp_merge_test.py", "w", encoding="utf-8") as f:
    f.write(test_script)

# 复制到容器并执行
print("📤 上传测试脚本到容器...")
subprocess.run("docker cp temp_merge_test.py social-media-hub-merger-1:/tmp/", shell=True)

print("🚀 执行合并测试...")
result = subprocess.run(
    "docker exec social-media-hub-merger-1 python /tmp/temp_merge_test.py",
    shell=True,
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("错误:", result.stderr)

# 清理
os.remove("temp_merge_test.py")

print()
print("="*60)
print("测试完成")
print()
print("清理命令:")
print("  docker exec social-media-hub-merger-1 rm -f /app/videos/merged/ai_vanvan/test_merge.mp4")
print("  docker exec social-media-hub-standardizer-1 rm -rf /app/videos/standardized/ai_vanvan/test")
