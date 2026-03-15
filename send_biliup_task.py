import redis
import json

# 连接 Redis
redis_client = redis.from_url("redis://localhost:6379")

# 准备任务数据
task = {
    "account": "ai_vanvan",
    "video_path": "/videos/ai_vanvan/ins海外离大谱#123.mp4",  # 容器内路径
    "title": "ins海外离大谱#123",
    "tid": 171,  # 娱乐分区
    "tag": "Instagram,搞笑,离大谱"
}

# 发送到队列
redis_client.rpush("biliup:queue", json.dumps(task))

print("✅ 任务已发送到 biliup:queue")
print(f"账号: {task['account']}")
print(f"视频: {task['video_path']}")
print(f"标题: {task['title']}")
