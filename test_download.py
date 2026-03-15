import redis
import json

r = redis.Redis(host='localhost', port=6379)

# 创建下载任务 - 基于scanner找到的shortcode
task = {
    'account': 'ai_vanvan',
    'shortcodes': [],  # 空列表表示下载所有扫描到的新视频
    'max_downloads': 1
}

r.lpush('download_queue', json.dumps(task))
print(' 下载任务已推送到download_queue')
print(f' 任务: {json.dumps(task, indent=2)}')
