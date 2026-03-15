import redis
import json

# 连接Redis
r = redis.Redis(host='localhost', port=6379)

# 创建登录测试任务
task = {
    'account': 'ai_vanvan',
    'username': 'ai_vanvan',
    'platform': 'instagram',
    'firefox_profile': '370tsjzy.default-release'
}

# 推送到auth队列
r.lpush('auth_queue', json.dumps(task))
print(' 登录测试任务已推送到auth_queue')
print(f' 任务内容: {json.dumps(task, indent=2)}')
