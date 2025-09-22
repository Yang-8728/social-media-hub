from flask import Flask, jsonify, request
import redis
import os
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Redis连接
try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    redis_client = redis.from_url(redis_url)
    redis_client.ping()
    logger.info("✅ Redis连接成功")
except Exception as e:
    logger.error(f"❌ Redis连接失败: {e}")
    redis_client = None

@app.route('/')
def home():
    """API Gateway主页"""
    return jsonify({
        'message': 'Welcome to Social Media Hub API Gateway!',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': [
            'GET  /',
            'GET  /health',
            'GET  /api/test-redis',
            'POST /api/workflow/start'
        ]
    })

@app.route('/health')
def health():
    """健康检查接口"""
    redis_status = "connected" if redis_client else "disconnected"
    
    try:
        if redis_client:
            redis_client.ping()
            redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return jsonify({
        'status': 'healthy',
        'service': 'api-gateway',
        'redis': redis_status,
        'message': 'API Gateway运行正常'
    })

@app.route('/api/test-redis')
def test_redis():
    """测试Redis连接"""
    try:
        if not redis_client:
            raise Exception("Redis未连接")
            
        # 写入测试数据
        test_key = 'api_test'
        test_value = 'Hello from API Gateway!'
        redis_client.set(test_key, test_value)
        
        # 读取测试数据
        value = redis_client.get(test_key).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'redis_test': value,
            'message': 'Redis读写测试成功'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Redis测试失败'
        }), 500

@app.route('/api/workflow/start', methods=['POST'])
def start_workflow():
    """开始工作流"""
    try:
        if not redis_client:
            raise Exception("Redis未连接")
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        account = data.get('account')
        limit = data.get('limit', 10)
        
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        
        # 创建工作流任务
        workflow_id = f"workflow_{account}_{os.urandom(4).hex()}"
        
        workflow_data = {
            'workflow_id': workflow_id,
            'account': account,
            'limit': limit,
            'status': 'pending',
            'created_at': str(int(os.time.time()) if hasattr(os, 'time') else 0)
        }
        
        # 发送到Redis队列
        redis_client.lpush('auth_queue', json.dumps(workflow_data))
        redis_client.hset(f'workflow:{workflow_id}', mapping=workflow_data)
        
        logger.info(f"🚀 工作流已创建: {workflow_id}")
        
        return jsonify({
            'status': 'success',
            'workflow_id': workflow_id,
            'message': f'工作流已启动，账户: {account}, 限制: {limit}',
            'data': workflow_data
        })
        
    except Exception as e:
        logger.error(f"❌ 启动工作流失败: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': '启动工作流失败'
        }), 500

@app.route('/api/workflow/<workflow_id>')
def get_workflow_status(workflow_id):
    """查询工作流状态"""
    try:
        if not redis_client:
            raise Exception("Redis未连接")
        
        # 从Redis获取工作流状态
        workflow_data = redis_client.hgetall(f'workflow:{workflow_id}')
        
        if not workflow_data:
            return jsonify({
                'status': 'error',
                'message': '工作流不存在'
            }), 404
        
        # 转换字节数据为字符串
        workflow_info = {k.decode(): v.decode() for k, v in workflow_data.items()}
        
        return jsonify({
            'status': 'success',
            'workflow_id': workflow_id,
            'data': workflow_info
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"🚀 API Gateway启动在端口 {port}")
    logger.info(f"🔧 调试模式: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)