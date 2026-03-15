import redis
import json
import sys

r = redis.Redis(host='localhost', port=6380, decode_responses=True)

task = {
    "account": "ai_vanvan",
    "video_path": "/videos/ai_vanvan/9月11日.mp4",
    "title": "Docker测试上传",
    "tid": 171,
    "tag": "测试,AI"
}

r.rpush("upload_queue", json.dumps(task, ensure_ascii=False))
print(" 已发送上传任务到队列")
print(f"标题: {task['title']}")
print("查看日志: docker logs -f biliup-uploader")
