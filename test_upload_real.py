import redis
import json
import time

# 连接到Redis
r = redis.Redis(host='localhost', port=6380, decode_responses=True)

# 测试上传一个符合标准命名的视频
task = {
    'account': 'ai_vanvan',
    'video_path': '/videos/ai_vanvan/ins海外离大谱#100.mp4',
}

print(f'推送任务到队列: {task}')
r.lpush('biliup:queue', json.dumps(task))
print('任务已推送')

# 检查队列
time.sleep(1)
queue_length = r.llen('biliup:queue')
print(f'当前队列长度: {queue_length}')
