import redis
import json
from pathlib import Path

# 连接 Redis
redis_client = redis.from_url("redis://localhost:6379")

# 获取下一个视频编号
merged_dir = Path("videos/merged/ai_vanvan")
existing_videos = list(merged_dir.glob("ins海外离大谱#*.mp4"))
if existing_videos:
    # 提取编号
    numbers = []
    for video in existing_videos:
        try:
            num = int(video.stem.split('#')[1])
            numbers.append(num)
        except:
            pass
    next_number = max(numbers) + 1 if numbers else 124
else:
    next_number = 124

print(f"📊 当前最新视频编号: #{max(numbers) if numbers else '无'}")
print(f"🎬 下一个视频编号: #{next_number}")

# 准备任务数据
task = {
    "account": "ai_vanvan",
    "video_path": f"/videos/ai_vanvan/ins海外离大谱#{next_number}.mp4",
    "title": f"ins海外离大谱#{next_number}",
    "tid": 138,  # 生活 > 搞笑（最合适Instagram搞笑视频）
    "tag": "Instagram,搞笑,离大谱,海外,沙雕"
}

print(f"\n📤 准备上传:")
print(f"  标题: {task['title']}")
print(f"  分区: 138 (生活 > 搞笑)")
print(f"  标签: {task['tag']}")
print(f"  路径: {task['video_path']}")

# 检查文件是否存在
local_path = Path(f"videos/merged/ai_vanvan/ins海外离大谱#{next_number}.mp4")
if not local_path.exists():
    print(f"\n❌ 文件不存在: {local_path}")
    print(f"\n💡 提示: 先运行合并任务生成视频")
else:
    file_size_mb = local_path.stat().st_size / 1024 / 1024
    print(f"\n✅ 文件存在: {file_size_mb:.2f} MB")
    
    # 发送到队列
    redis_client.rpush("biliup:queue", json.dumps(task))
    print(f"\n✅ 任务已发送到 biliup:queue")
