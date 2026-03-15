#!/usr/bin/env python3
import redis
import json

# 连接Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 创建任务
task = {
    "account": "ai_vanvan",
    "video_path": "/app/videos/merged/test.mp4",
    "title": "自动登录测试",
    "description": "测试Fresh Profile",
    "tags": ["测试"],
    "cover_path": "",
    "category": 138
}

# 发送任务
r.lpush('upload_queue', json.dumps(task, ensure_ascii=False))
print(f"✅ 任务已发送: {task['title']}")
