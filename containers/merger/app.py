from flask import Flask, jsonify, request
import redis
import json
import os
import threading
import time
import sys
import subprocess
import glob

# 添加项目路径以便导入核心模块
sys.path.append('/app')

app = Flask(__name__)
redis_client = redis.from_url('redis://redis:6379')

# 加载账号配置
def load_account_config():
    config_path = '/app/config/accounts.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def home():
    return jsonify({'service': 'merger', 'status': 'running'})

@app.route('/merge', methods=['POST'])
def start_merge():
    """启动视频合并任务"""
    data = request.get_json()
    account_name = data.get('account')
    limit = data.get('limit', None)
    video_folder = data.get('video_folder', None)  # 新增：指定视频文件夹
    
    if not account_name:
        return jsonify({'error': 'account is required'}), 400
    
    # 加载账号配置
    accounts_config = load_account_config()
    account_config = accounts_config.get(account_name, {})
    
    if not account_config:
        return jsonify({'error': f'Account {account_name} not found in config'}), 404
    
    # 构建合并任务
    task = {
        'account': account_name,
        'limit': limit,
        'video_folder': video_folder,  # 新增字段
        'type': 'merge',
        'status': 'pending'
    }
    
    redis_client.lpush('merge_queue', json.dumps(task))
    
    return jsonify({
        'message': f'Merge task started',
        'account': account_name,
        'limit': limit,
        'video_folder': video_folder
    })

def process_merge_queue():
    """处理合并队列的工作进程"""
    while True:
        try:
            # 从队列获取任务
            task_data = redis_client.brpop('merge_queue', timeout=5)
            if not task_data:
                continue
                
            task = json.loads(task_data[1])
            
            print(f"🔄 处理合并任务: {task}", flush=True)
            
            if task['type'] == 'merge':
                process_merge_task(task)
                
        except Exception as e:
            print(f"❌ 处理队列任务出错: {e}", flush=True)
            time.sleep(1)

def process_merge_task(task):
    """处理视频合并任务 - 微服务架构版本（调用standardizer）"""
    try:
        account_name = task['account']
        limit = task.get('limit')
        video_folder = task.get('video_folder', None)  # 新增：指定文件夹
        date = task.get('date', None)  # 新增：指定日期
        is_pipeline = task.get('pipeline', False)
        
        print(f"🎬 开始合并任务: {account_name}, 限制: {limit}, 日期: {date}, 文件夹: {video_folder}", flush=True)
        
        # 使用微服务架构
        result = process_merge_with_microservices(account_name, limit, video_folder, date)
        
        print(f"✅ 合并完成: {result}", flush=True)
        
        # 将结果存储到Redis以供查询
        redis_client.setex(f"merge_result_{account_name}", 3600, json.dumps(result))
        
        # 如果是流水线任务且合并成功，自动触发上传
        if is_pipeline and result.get('merged', 0) > 0:
            print(f"🚀 流水线模式：自动触发上传任务", flush=True)
            upload_task = {
                'account': account_name,
                'video_path': result.get('output_file'),
                'title': None,  # 从文件名提取
                'status': 'pending'
            }
            redis_client.lpush('upload_queue', json.dumps(upload_task))
            print(f"📤 已添加上传任务到队列", flush=True)
        
    except Exception as e:
        print(f"❌ 合并任务失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        error_result = {"merged": 0, "skipped": 0, "failed": 1, "error": str(e)}
        redis_client.setex(f"merge_result_{account_name}", 3600, json.dumps(error_result))

def process_merge_with_microservices(account_name: str, limit: int = None, video_folder: str = None, date: str = None):
    """使用微服务架构进行合并: Standardizer + Merger分离
    
    Args:
        account_name: 账号名称
        limit: 限制合并数量
        video_folder: 指定视频文件夹路径（优先级最高）
        date: 指定日期 YYYY-MM-DD（如果不指定则使用今天）
    """
    try:
        # 如果指定了 video_folder，直接使用该文件夹的视频
        if video_folder:
            print(f"📁 使用指定文件夹: {video_folder}", flush=True)
            
            if not os.path.exists(video_folder):
                print(f"⚠️ 指定的文件夹不存在: {video_folder}", flush=True)
                return {"merged": 0, "skipped": 0, "failed": 0}
            
            # 获取文件夹中的所有视频
            all_videos = []
            for ext in ['mp4', 'avi', 'mov']:
                all_videos.extend(glob.glob(os.path.join(video_folder, f"*.{ext}")))
            
            all_videos = sorted(all_videos, reverse=True)  # 最新的在前
            
            if not all_videos:
                print(f"⚠️ 指定文件夹中没有找到视频文件", flush=True)
                return {"merged": 0, "skipped": 0, "failed": 0}
            
            print(f"📹 找到 {len(all_videos)} 个视频文件", flush=True)
            
            # 应用limit
            if limit:
                videos_to_merge = all_videos[:limit]
                print(f"📹 准备合并最新的 {len(videos_to_merge)} 个视频（剩余 {len(all_videos) - len(videos_to_merge)} 个）", flush=True)
            else:
                videos_to_merge = all_videos
                print(f"📹 准备合并全部 {len(videos_to_merge)} 个视频", flush=True)
            
            print(f"   视频列表: {[os.path.basename(v) for v in videos_to_merge]}", flush=True)
            
            # 直接合并（文件已经标准化）
            return merge_standardized_videos(account_name, videos_to_merge, video_folder)
        
        # 原有逻辑：处理指定日期或今天的视频
        print(f"📋 步骤1: 扫描视频文件", flush=True)
        
        # 获取日期（使用指定日期或今天）
        from datetime import datetime
        if date:
            target_date = date
            print(f"   🗓️  使用指定日期: {target_date}", flush=True)
        else:
            target_date = datetime.now().strftime("%Y-%m-%d")
            print(f"   🗓️  使用今天日期: {target_date}", flush=True)
        
        # 扫描下载目录
        downloads_base = f"/app/videos/downloads/{account_name}"
        
        if not os.path.exists(downloads_base):
            print(f"⚠️ 下载目录不存在: {downloads_base}", flush=True)
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # 获取账户配置的folder_strategy
        try:
            from main import load_account_config
            account_configs = load_account_config()
            account_config = account_configs.get(account_name, {})
            folder_strategy = account_config.get("folder_strategy", "daily")
        except:
            folder_strategy = "daily"
        
        # 根据策略查找指定日期的视频
        all_today_videos = []
        
        if folder_strategy == "date_blogger":
            # date_blogger格式：YYYY-MM-DD_博主ID
            pattern = os.path.join(downloads_base, f"{target_date}_*")
            today_folders = glob.glob(pattern)
            
            for folder in today_folders:
                if os.path.isdir(folder):
                    videos = glob.glob(os.path.join(folder, "*.mp4"))
                    all_today_videos.extend(videos)
        else:
            # daily格式：YYYY-MM-DD
            today_path = os.path.join(downloads_base, target_date)
            if os.path.exists(today_path):
                videos = glob.glob(os.path.join(today_path, "*.mp4"))
                all_today_videos.extend(videos)
        
        if not all_today_videos:
            print(f"ℹ️  没有找到 {target_date} 的视频文件", flush=True)
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # 检查哪些已经合并过
        from src.utils.video_merger import VideoMerger
        temp_merger = VideoMerger(account_name)
        
        unmerged_videos = []
        skipped_count = 0
        for video in all_today_videos:
            if temp_merger.is_video_merged(video):
                skipped_count += 1
            else:
                unmerged_videos.append(video)
        
        if skipped_count > 0:
            print(f"📊 {target_date} 找到 {len(all_today_videos)} 个视频，其中 {skipped_count} 个已合并，{len(unmerged_videos)} 个待合并", flush=True)
        
        if not unmerged_videos:
            print(f"ℹ️  {target_date} 所有视频都已经合并过了", flush=True)
            return {"merged": 0, "skipped": skipped_count, "failed": 0}
        
        # 按修改时间排序
        unmerged_videos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # 应用限制
        if limit:
            merge_videos = unmerged_videos[:limit]
            print(f"📹 准备合并最新的 {len(merge_videos)} 个视频（剩余 {len(unmerged_videos) - len(merge_videos)} 个）", flush=True)
        else:
            merge_videos = unmerged_videos
            print(f"📹 准备合并全部 {len(unmerged_videos)} 个未合并视频", flush=True)
        
        print(f"   视频列表: {[os.path.basename(v) for v in merge_videos]}", flush=True)
        
        # 步骤2: 调用Standardizer服务进行标准化
        print(f"🎨 步骤2: 调用Standardizer服务进行标准化...", flush=True)
        
        import requests
        standardize_task = {
            'account': account_name,
            'video_files': merge_videos,
            'output_folder': f'/app/videos/standardized/{account_name}',
            'process_type': 'ultimate'
        }
        
        standardize_response = requests.post(
            'http://standardizer:8000/process-batch',
            json=standardize_task,
            timeout=600  # 10分钟超时
        )
        
        if standardize_response.status_code != 200:
            raise Exception(f"Standardizer服务失败: {standardize_response.text}")
        
        standardize_result = standardize_response.json()
        print(f"✅ 视频标准化任务已加入队列: {standardize_result}", flush=True)
        
        # 步骤3: 等待标准化完成
        print(f"⏳ 步骤3: 等待标准化完成...", flush=True)
        
        standardized_folder = f"/app/videos/standardized/{account_name}"
        os.makedirs(standardized_folder, exist_ok=True)
        
        # 等待标准化文件出现（最多10分钟）
        wait_timeout = 600  # 10分钟
        wait_interval = 5  # 每5秒检查一次
        waited_time = 0
        
        while waited_time < wait_timeout:
            standardized_files = glob.glob(os.path.join(standardized_folder, "*_ultimate.mp4"))
            if len(standardized_files) >= len(merge_videos):
                print(f"✅ 标准化完成！找到 {len(standardized_files)} 个文件", flush=True)
                break
            
            print(f"   等待中... ({waited_time}s/{wait_timeout}s), 当前文件数: {len(standardized_files)}/{len(merge_videos)}", flush=True)
            time.sleep(wait_interval)
            waited_time += wait_interval
        else:
            raise Exception(f"等待标准化超时 ({wait_timeout}s)，只找到 {len(standardized_files)} 个文件")
        
        # 步骤4: 合并标准化后的视频
        print(f"🔗 步骤4: 合并标准化后的视频...", flush=True)
        
        standardized_folder = f"/app/videos/standardized/{account_name}"
        output_folder = f"/app/videos/merged/{account_name}"
        os.makedirs(output_folder, exist_ok=True)
        
        # 生成输出文件名
        output_filename = temp_merger._generate_title_filename(merge_videos)
        output_path = os.path.join(output_folder, output_filename)
        
        # 创建concat文件列表
        concat_file = f"/tmp/concat_{account_name}.txt"
        standardized_files = glob.glob(os.path.join(standardized_folder, "*.mp4"))
        standardized_files.sort()  # 确保顺序
        
        print(f"   找到 {len(standardized_files)} 个标准化文件", flush=True)
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for std_file in standardized_files:
                f.write(f"file '{std_file}'\n")
        
        # FFmpeg合并命令
        merge_cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        result_code = subprocess.run(merge_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result_code.returncode == 0 and os.path.exists(output_path):
            output_size_mb = os.path.getsize(output_path) / (1024*1024)
            print(f"✅ 合并成功! 输出文件: {output_path} ({output_size_mb:.1f}MB)", flush=True)
            
            # 记录已合并视频
            temp_merger.add_merged_videos(merge_videos, output_path)
            
            return {"merged": 1, "skipped": skipped_count, "failed": 0, "output_file": output_path}
        else:
            print(f"❌ FFmpeg合并失败: {result_code.stderr}", flush=True)
            return {"merged": 0, "skipped": skipped_count, "failed": 1}
            
    except Exception as e:
        print(f"❌ 微服务合并流程失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return {"merged": 0, "skipped": 0, "failed": 1, "error": str(e)}

@app.route('/status/<account_name>')
def get_status(account_name):
    """获取合并状态"""
    result = redis_client.get(f"merge_result_{account_name}")
    if result:
        return jsonify(json.loads(result))
    else:
        return jsonify({'status': 'no recent tasks'})

def merge_standardized_videos(account_name: str, video_files: list, source_folder: str):
    """直接合并已标准化的视频文件"""
    try:
        print(f"🔗 开始合并标准化视频...", flush=True)
        
        output_folder = f"/app/videos/merged/{account_name}"
        os.makedirs(output_folder, exist_ok=True)
        
        # 生成输出文件名（简化版）
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_{timestamp}.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        # 创建concat文件列表
        concat_file = f"/tmp/concat_{account_name}_{timestamp}.txt"
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for video_file in video_files:
                # 转义单引号
                escaped_path = video_file.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        print(f"📝 创建了concat文件: {concat_file}", flush=True)
        print(f"   包含 {len(video_files)} 个视频", flush=True)
        
        # FFmpeg合并命令
        merge_cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        print(f"🎬 执行合并命令...", flush=True)
        result = subprocess.run(
            merge_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )
        
        if result.returncode != 0:
            raise Exception(f"FFmpeg合并失败: {result.stderr}")
        
        # 检查输出文件
        if not os.path.exists(output_path):
            raise Exception(f"合并后的文件不存在: {output_path}")
        
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ 合并成功! 输出文件: {output_path} ({file_size_mb:.1f}MB)", flush=True)
        
        # 清理concat文件
        try:
            os.remove(concat_file)
        except:
            pass
        
        return {
            "merged": 1,
            "skipped": 0,
            "failed": 0,
            "output_file": output_path,
            "file_size_mb": round(file_size_mb, 2),
            "video_count": len(video_files)
        }
        
    except Exception as e:
        print(f"❌ 合并失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return {
            "merged": 0,
            "skipped": 0,
            "failed": 1,
            "error": str(e)
        }

# 启动后台工作进程（在模块加载时立即启动）
worker_thread = threading.Thread(target=process_merge_queue, daemon=True)
worker_thread.start()
print("🔄 后台合并队列监听器已启动", flush=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
