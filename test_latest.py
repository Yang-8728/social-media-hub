import redis
import json

# 连接到Redis
r = redis.Redis(host='localhost', port=6380, decode_responses=True)

# 清空队列
r.delete('biliup:queue')
print('已清空队列')

# 推送最新视频上传任务
task = {
    'account': 'ai_vanvan',
    'video_path': '/videos/ai_vanvan/ins海外离大谱#123.mp4',
}

print(f'推送任务: {task}')
r.lpush('biliup:queue', json.dumps(task))
print(' 任务已推送到队列')
queue_len = r.llen('biliup:queue')
print(f'当前队列长度: {queue_len}')
