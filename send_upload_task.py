"""发送正确的上传任务到Redis"""
import redis
import json

# 连接Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 清空队列
r.delete('upload_queue')

# 创建任务
task = {
    "account": "ai_vanvan",
    "video_path": "videos/merged/ins海外离大谱#123.mp4",
    "title": "海外离大谱合集 #123",
    "description": "精选海外离谱瞬间",
    "tags": ["搞笑", "海外", "生活"]
}

# 推送到队列
r.lpush('upload_queue', json.dumps(task))

print(f"✅ 任务已发送: {task}")

# 验证
length = r.llen('upload_queue')
print(f"📊 队列长度: {length}")
