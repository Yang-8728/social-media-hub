"""
完整流程测试脚本 - 带自动回退机制
测试场景：下载 → 标准化 → 合并 → 上传 → 自动清理

功能：
1. 模拟有新视频的场景（测试下载、标准化、合并、上传）
2. 测试成功后自动回退所有操作
3. 删除下载的视频和文件夹
4. 删除下载日志记录
5. 删除标准化的视频
6. 删除合并的视频和记录
7. 回退B站上传序号
8. 提示手动删除B站视频

注意：上传的视频需要手动在B站后台删除
"""

import requests
import time
import json
import os
import subprocess
from datetime import datetime

API_BASE = "http://localhost:8080"
ACCOUNT = "ai_vanvan"

# 测试记录
class TestRecord:
    def __init__(self):
        self.downloaded_videos = []
        self.download_folders = []
        self.standardized_folders = []
        self.merged_videos = []
        self.uploaded_videos = []
        self.download_records = []
        self.merge_records = []
        self.start_time = datetime.now()
        
    def to_json(self):
        return {
            'account': ACCOUNT,
            'start_time': self.start_time.isoformat(),
            'downloaded_videos': self.downloaded_videos,
            'download_folders': self.download_folders,
            'standardized_folders': self.standardized_folders,
            'merged_videos': self.merged_videos,
            'uploaded_videos': self.uploaded_videos,
            'download_records': self.download_records,
            'merge_records': self.merge_records
        }
    
    def save(self):
        """保存测试记录到文件"""
        filename = f"test_record_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, indent=2, ensure_ascii=False)
        print(f"📝 测试记录已保存: {filename}")
        return filename

record = TestRecord()


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def execute_docker_command(container, command, description):
    """执行 Docker 命令"""
    full_cmd = f"docker exec {container} {command}"
    print(f"🔧 {description}")
    print(f"   命令: {full_cmd}")
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        if result.stdout.strip():
            print(f"   ✅ 成功: {result.stdout.strip()[:200]}")
        else:
            print(f"   ✅ 成功")
        return True, result.stdout
    else:
        print(f"   ❌ 失败: {result.stderr.strip()[:200]}")
        return False, result.stderr


def test_download(limit=3):
    """步骤1: 测试下载服务"""
    print_section("📥 步骤 1/4: 下载最新内容")
    
    url = f"{API_BASE}/download"
    payload = {
        "account": ACCOUNT,
        "limit": limit
    }
    
    print(f"🔗 请求: POST {url}")
    print(f"📦 参数: limit={limit}")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 下载任务已启动")
            
            # 等待下载完成
            print("⏳ 等待下载完成（最多等待60秒）...")
            time.sleep(60)
            
            # 检查下载结果
            print("\n📋 检查下载结果...")
            success, output = execute_docker_command(
                "social-media-hub-downloader-1",
                f"find /app/downloads/{ACCOUNT} -type f -name '*.mp4' -newer /tmp/test_start 2>/dev/null || echo 'no files'",
                "查找新下载的视频文件"
            )
            
            if success and output.strip() and 'no files' not in output:
                videos = [v.strip() for v in output.strip().split('\n') if v.strip()]
                record.downloaded_videos = videos
                print(f"✅ 发现 {len(videos)} 个新下载的视频")
                for v in videos[:5]:
                    print(f"   - {v}")
                return True, len(videos)
            else:
                print("ℹ️  没有新下载的视频")
                return True, 0
                
        else:
            print(f"❌ 下载失败: {response.text}")
            return False, 0
            
    except Exception as e:
        print(f"❌ 下载请求失败: {e}")
        return False, 0


def test_merge():
    """步骤2: 测试合并服务（包含自动标准化）"""
    print_section("🔗 步骤 2/4: 合并视频（包含标准化）")
    
    # 先查询合并状态
    status_url = f"{API_BASE}/merge/status/{ACCOUNT}"
    
    print(f"🔗 查询合并状态: GET {status_url}")
    
    try:
        response = requests.get(status_url, timeout=30)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            unmerged = result.get('unmerged_count', 0)
            
            print(f"📋 未合并视频数: {unmerged}")
            
            if unmerged == 0:
                print("ℹ️  没有需要合并的视频")
                return True, None
            
            # 开始合并
            print(f"\n🚀 开始合并处理...")
            merge_url = f"{API_BASE}/merge"
            merge_payload = {
                "account": ACCOUNT,
                "limit": None
            }
            
            merge_response = requests.post(merge_url, json=merge_payload, timeout=600)
            print(f"📊 合并状态码: {merge_response.status_code}")
            
            if merge_response.status_code == 200:
                merge_result = merge_response.json()
                print(f"✅ 合并响应: {json.dumps(merge_result, indent=2, ensure_ascii=False)}")
                
                # 记录合并的视频
                output_file = merge_result.get('output_file', '')
                if output_file:
                    record.merged_videos.append(output_file)
                    print(f"📁 合并输出: {output_file}")
                    return True, output_file
                else:
                    return True, None
            else:
                print(f"❌ 合并失败: {merge_response.text}")
                return False, None
        else:
            print(f"❌ 查询状态失败: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 合并请求失败: {e}")
        return False, None


def test_upload(video_path):
    """步骤3: 测试上传服务"""
    print_section("🚀 步骤 3/4: 上传到B站")
    
    if not video_path:
        print("⚠️  没有视频需要上传")
        return True, None
    
    url = f"{API_BASE}/upload"
    payload = {
        "account": ACCOUNT,
        "video_path": video_path
    }
    
    print(f"🔗 请求: POST {url}")
    print(f"📦 参数: video_path={video_path}")
    
    try:
        response = requests.post(url, json=payload, timeout=1200)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 上传响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 记录上传的视频
            uploaded_url = result.get('video_url', '')
            if uploaded_url:
                record.uploaded_videos.append({
                    'local_path': video_path,
                    'bilibili_url': uploaded_url
                })
            
            return True, uploaded_url
        else:
            print(f"❌ 上传失败: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 上传请求失败: {e}")
        return False, None


def rollback_all():
    """步骤4: 回退所有测试操作"""
    print_section("🔙 步骤 4/4: 回退测试操作")
    
    print("⚠️  准备回退所有测试操作...")
    print("📋 回退内容包括:")
    print("   1. 删除下载的视频文件")
    print("   2. 删除下载的文件夹")
    print("   3. 删除下载日志记录")
    print("   4. 删除标准化视频")
    print("   5. 删除合并视频")
    print("   6. 删除合并记录（回退序号）")
    print("   7. 清理Redis缓存")
    print()
    
    confirm = input("⚠️  确认要回退所有操作吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ 已取消回退操作")
        return False
    
    print("\n🔄 开始回退...")
    success_count = 0
    total_steps = 7
    
    # 1. 删除下载的视频文件
    print("\n1️⃣ 删除下载的视频文件...")
    if record.downloaded_videos:
        for video in record.downloaded_videos:
            success, _ = execute_docker_command(
                "social-media-hub-downloader-1",
                f"rm -f '{video}'",
                f"删除视频: {os.path.basename(video)}"
            )
            if success:
                success_count += 0.1
    else:
        # 删除测试时间段内的所有下载
        success, output = execute_docker_command(
            "social-media-hub-downloader-1",
            f"find /app/downloads/{ACCOUNT} -type f -name '*.mp4' -newer /tmp/test_start -delete 2>/dev/null || echo 'done'",
            "删除测试时间段内下载的视频"
        )
        if success:
            success_count += 1
    
    # 2. 删除下载的文件夹（如果为空）
    print("\n2️⃣ 清理空文件夹...")
    success, _ = execute_docker_command(
        "social-media-hub-downloader-1",
        f"find /app/downloads/{ACCOUNT} -type d -empty -delete 2>/dev/null || echo 'done'",
        "删除空文件夹"
    )
    if success:
        success_count += 1
    
    # 3. 删除下载日志记录
    print("\n3️⃣ 删除下载日志记录...")
    success, _ = execute_docker_command(
        "social-media-hub-downloader-1",
        f"python -c \"import json; "
        f"log_file='/app/logs/downloads/{ACCOUNT}_download.json'; "
        f"data=json.load(open(log_file)) if __import__('os').path.exists(log_file) else {{'downloads':[]}}; "
        f"data['downloads']=[d for d in data['downloads'] if d.get('timestamp','')[:10]!='{datetime.now().strftime('%Y-%m-%d')}']; "
        f"json.dump(data,open(log_file,'w'),indent=2)\"",
        "删除今天的下载记录"
    )
    if success:
        success_count += 1
    
    # 4. 删除标准化视频
    print("\n4️⃣ 删除标准化视频...")
    success, _ = execute_docker_command(
        "social-media-hub-standardizer-1",
        f"find /app/videos/standardized/{ACCOUNT} -type f -name '*ultimate.mp4' -newer /tmp/test_start -delete 2>/dev/null || echo 'done'",
        "删除测试时间段的标准化视频"
    )
    if success:
        success_count += 1
    
    # 清理空文件夹
    execute_docker_command(
        "social-media-hub-standardizer-1",
        f"find /app/videos/standardized/{ACCOUNT} -type d -empty -delete 2>/dev/null || echo 'done'",
        "清理标准化空文件夹"
    )
    
    # 5. 删除合并视频
    print("\n5️⃣ 删除合并视频...")
    if record.merged_videos:
        for video in record.merged_videos:
            video_name = os.path.basename(video)
            success, _ = execute_docker_command(
                "social-media-hub-merger-1",
                f"rm -f '/app/videos/merged/{ACCOUNT}/{video_name}'",
                f"删除合并视频: {video_name}"
            )
            if success:
                success_count += 0.5
    else:
        success_count += 1
    
    # 6. 回退合并记录（删除最后一条记录）
    print("\n6️⃣ 回退合并记录...")
    success, _ = execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json; "
        f"log_file='/app/logs/merges/{ACCOUNT}_merged_record.json'; "
        f"data=json.load(open(log_file)) if __import__('os').path.exists(log_file) else {{'merged_videos':[]}}; "
        f"if data['merged_videos'] and data['merged_videos'][-1].get('timestamp','')[:10]=='{datetime.now().strftime('%Y-%m-%d')}': "
        f"data['merged_videos'].pop(); "
        f"json.dump(data,open(log_file,'w'),indent=2,ensure_ascii=False)\"",
        "删除今天的合并记录（回退序号）"
    )
    if success:
        success_count += 1
    
    # 7. 清理Redis缓存
    print("\n7️⃣ 清理Redis缓存...")
    success, _ = execute_docker_command(
        "social-media-hub-redis-1",
        f"redis-cli DEL merge_result_{ACCOUNT}",
        "清理合并结果缓存"
    )
    if success:
        success_count += 1
    
    # 总结
    print("\n" + "=" * 60)
    print(f"✅ 回退完成: {success_count}/{total_steps} 步成功")
    print("=" * 60)
    
    # B站视频提醒
    if record.uploaded_videos:
        print("\n⚠️  重要提醒：需要手动删除B站视频！")
        print("=" * 60)
        for upload in record.uploaded_videos:
            print(f"📹 视频: {os.path.basename(upload['local_path'])}")
            if upload.get('bilibili_url'):
                print(f"   链接: {upload['bilibili_url']}")
        print("\n💡 请访问: https://member.bilibili.com/platform/upload-manager/article")
        print("   找到今天上传的视频，点击删除")
        print("=" * 60)
    
    return True


def create_test_marker():
    """在容器中创建测试开始时间标记"""
    print("📝 创建测试时间标记...")
    containers = [
        "social-media-hub-downloader-1",
        "social-media-hub-standardizer-1",
        "social-media-hub-merger-1"
    ]
    
    for container in containers:
        execute_docker_command(
            container,
            "touch /tmp/test_start",
            f"在 {container.split('-')[-2]} 容器中创建时间标记"
        )


def main():
    """运行完整测试流程"""
    print("🧪 完整流程测试 - 带自动回退机制")
    print("="*60)
    print(f"📱 账号: {ACCOUNT}")
    print(f"🌐 API地址: {API_BASE}")
    print(f"⏰ 开始时间: {record.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("⚠️  测试说明:")
    print("   1. 此测试会真实执行：下载 → 标准化 → 合并 → 上传")
    print("   2. 视频会真的上传到B站")
    print("   3. 测试后会自动回退所有操作")
    print("   4. B站上的视频需要手动删除")
    print()
    
    confirm = input("确认开始测试吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ 已取消测试")
        return
    
    # 创建时间标记
    create_test_marker()
    
    # 检查服务状态
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code != 200:
            print("⚠️  API Gateway 状态异常，但继续测试...")
    except Exception as e:
        print(f"❌ 无法连接到 API Gateway: {e}")
        print("💡 请确保服务已启动: docker-compose up -d")
        return
    
    success_steps = 0
    total_steps = 4
    
    try:
        # 步骤1: 下载
        success, video_count = test_download(limit=3)
        if success:
            success_steps += 1
            if video_count == 0:
                print("\n✅ 下载测试完成，但没有新视频")
                print("💡 测试结束（无需回退）")
                return
        else:
            print("\n❌ 下载步骤失败")
            if input("是否继续测试？(yes/no): ").lower() != 'yes':
                return
        
        # 步骤2: 合并（包含标准化）
        success, merged_video = test_merge()
        if success:
            success_steps += 1
            if not merged_video:
                print("\n✅ 合并测试完成，但没有生成合并视频")
                rollback_all()
                return
        else:
            print("\n❌ 合并步骤失败")
            rollback_all()
            return
        
        # 步骤3: 上传
        success, upload_url = test_upload(merged_video)
        if success:
            success_steps += 1
        else:
            print("\n⚠️  上传步骤失败，但继续回退")
        
        # 步骤4: 回退
        print("\n" + "="*60)
        print(f"测试完成: {success_steps}/{total_steps-1} 步成功")
        print("="*60)
        
        # 保存测试记录
        record_file = record.save()
        
        # 执行回退
        rollback_all()
        
        print("\n" + "="*60)
        print("✅ 测试流程全部完成！")
        print("="*60)
        print(f"📝 详细记录: {record_file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被中断！")
        print("是否要回退已执行的操作？")
        if input("回退？(yes/no): ").lower() == 'yes':
            rollback_all()
    except Exception as e:
        print(f"\n❌ 测试过程发生异常: {e}")
        print("是否要回退已执行的操作？")
        if input("回退？(yes/no): ").lower() == 'yes':
            rollback_all()


if __name__ == "__main__":
    main()
