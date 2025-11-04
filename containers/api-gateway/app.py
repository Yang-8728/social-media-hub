from flask import Flask, jsonify, request, render_template
import redis
import os
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Redis连接
try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    redis_client = redis.from_url(redis_url)
    redis_client.ping()
    logger.info(' Redis连接成功')
except Exception as e:
    logger.error(f' Redis连接失败: {e}')
    redis_client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    redis_status = 'connected' if redis_client else 'disconnected'
    try:
        if redis_client:
            redis_client.ping()
            redis_status = 'connected'
    except:
        redis_status = 'disconnected'
    return jsonify({'status': 'healthy', 'service': 'api-gateway', 'redis': redis_status})

@app.route('/api/test-redis')
def test_redis():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        test_key = 'api_test'
        test_value = 'Hello from API Gateway!'
        redis_client.set(test_key, test_value)
        value = redis_client.get(test_key).decode('utf-8')
        return jsonify({'status': 'success', 'redis_test': value})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'auth_{account}_{os.urandom(4).hex()}'
        task_data = {'task_id': task_id, 'account': account}
        redis_client.lpush('auth_queue', json.dumps(task_data))
        logger.info(f' 认证任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 认证失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/auth/status/<account>')
def auth_status(account):
    return jsonify({'authenticated': True, 'account': account})

@app.route('/api/scanner/scan', methods=['POST'])
def scanner_scan():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        limit = data.get('limit', 50)
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'scan_{account}_{os.urandom(4).hex()}'
        task_data = {'task_id': task_id, 'account': account, 'limit': limit}
        redis_client.lpush('scan_queue', json.dumps(task_data))
        logger.info(f' 扫描任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 扫描失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/downloader/download', methods=['POST'])
def downloader_download():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        max_downloads = data.get('max_downloads', 20)
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'download_{account}_{os.urandom(4).hex()}'
        task_data = {'task_id': task_id, 'account': account, 'max_downloads': max_downloads}
        redis_client.lpush('download_queue', json.dumps(task_data))
        logger.info(f' 下载任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 下载失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/standardizer/process', methods=['POST'])
def standardizer_process():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        resolution = data.get('resolution', '1080x1920')
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'standardize_{account}_{os.urandom(4).hex()}'
        task_data = {'task_id': task_id, 'account': account, 'resolution': resolution}
        redis_client.lpush('standardizer_queue', json.dumps(task_data))
        logger.info(f' 标准化任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 标准化失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/merger/merge', methods=['POST'])
def merger_merge():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        limit = data.get('limit', 15)
        date = data.get('date')  # 新增：可选的日期参数 YYYY-MM-DD
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'merge_{account}_{os.urandom(4).hex()}'
        task_data = {
            'task_id': task_id, 
            'type': 'merge', 
            'account': account, 
            'limit': limit
        }
        # 如果指定了日期，添加到任务数据中
        if date:
            task_data['date'] = date
        redis_client.lpush('merge_queue', json.dumps(task_data))
        logger.info(f' 合并任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 合并失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/uploader/upload', methods=['POST'])
def uploader_upload():
    try:
        if not redis_client:
            raise Exception('Redis未连接')
        data = request.get_json()
        account = data.get('account')
        video_path = data.get('video_path')
        if not account:
            return jsonify({'error': '请提供account参数'}), 400
        task_id = f'upload_{account}_{os.urandom(4).hex()}'
        task_data = {'task_id': task_id, 'account': account, 'video_path': video_path}
        redis_client.lpush('upload_queue', json.dumps(task_data))
        logger.info(f' 上传任务已创建: {task_id}')
        return jsonify({'status': 'success', 'task_id': task_id})
    except Exception as e:
        logger.error(f' 上传失败: {e}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    logger.info(f' API Gateway启动在端口 {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)
