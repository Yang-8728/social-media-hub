import redis
import json
from pathlib import Path

# 连接 Redis
redis_client = redis.from_url("redis://localhost:6379")

# 使用现有的 #123 文件，但标题改为 #124
task = {
    "account": "ai_vanvan",
    "video_path": "/videos/ai_vanvan/ins海外离大谱#123.mp4",  # 用现有文件
    "title": "ins海外离大谱#124",  # 改标题为 #124
    "tid": 138,  # 生活 > 搞笑（正确分区）
    "tag": "Instagram,搞笑,离大谱,海外,沙雕"
}

print("=" * 70)
print("📤 上传 #124 (使用 #123 的文件，正确分区)")
print("=" * 70)
print(f"\n视频信息:")
print(f"  文件: ins海外离大谱#123.mp4")
print(f"  标题: {task['title']} ← 改为 #124")
print(f"  分区: 138 (生活 > 搞笑) ← 正确分区！")
print(f"  标签: {task['tag']}")

# 检查文件
local_file = Path("videos/merged/ai_vanvan/ins海外离大谱#123.mp4")
if local_file.exists():
    size_mb = local_file.stat().st_size / 1024 / 1024
    print(f"\n✅ 文件存在: {size_mb:.2f} MB")
else:
    print(f"\n❌ 文件不存在")
    exit(1)

print(f"\n💡 说明:")
print(f"  - 之前的 #123 (BV1cx1kBvEtG) 用了错误分区 171")
print(f"  - 这次上传为 #124，使用正确分区 138")
print(f"  - 可以稍后在B站删除旧的 #123")

# 直接上传，无需确认
redis_client.rpush("biliup:queue", json.dumps(task))
print(f"\n✅ 任务已发送到 biliup:queue")
print(f"\n查看进度: docker logs biliup-uploader --tail 30 --follow")
