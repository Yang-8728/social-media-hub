"""
手动回退工具
用于清理测试数据和回退操作

使用场景：
1. 测试中断需要手动清理
2. 从测试记录文件恢复并回退
3. 指定日期的数据清理
"""

import json
import subprocess
import os
from datetime import datetime
import argparse


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
        if result.stderr.strip():
            print(f"   ⚠️  {result.stderr.strip()[:200]}")
        return False, result.stderr


def rollback_by_date(account, date_str):
    """
    按日期回退测试数据
    date_str: YYYY-MM-DD 格式
    """
    print(f"🔙 回退 {account} 账号 {date_str} 的测试数据")
    print("="*60)
    
    # 1. 删除下载的视频
    print("\n1️⃣ 删除下载的视频...")
    execute_docker_command(
        "social-media-hub-downloader-1",
        f"find /app/downloads/{account} -type f -name '*.mp4' -newermt '{date_str}' ! -newermt '{date_str} 23:59:59' -delete 2>/dev/null || echo 'done'",
        f"删除 {date_str} 下载的视频"
    )
    
    # 2. 清理空文件夹
    print("\n2️⃣ 清理空文件夹...")
    execute_docker_command(
        "social-media-hub-downloader-1",
        f"find /app/downloads/{account} -type d -empty -delete 2>/dev/null || echo 'done'",
        "删除空文件夹"
    )
    
    # 3. 删除下载日志
    print("\n3️⃣ 删除下载日志记录...")
    execute_docker_command(
        "social-media-hub-downloader-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/downloads/{account}_download.json'; "
        f"data=json.load(open(log_file)) if os.path.exists(log_file) else {{'downloads':[]}}; "
        f"data['downloads']=[d for d in data['downloads'] if d.get('timestamp','')[:10]!='{date_str}']; "
        f"json.dump(data,open(log_file,'w'),indent=2)\"",
        f"删除 {date_str} 的下载记录"
    )
    
    # 4. 删除标准化视频
    print("\n4️⃣ 删除标准化视频...")
    execute_docker_command(
        "social-media-hub-standardizer-1",
        f"find /app/videos/standardized/{account} -type f -name '*.mp4' -newermt '{date_str}' ! -newermt '{date_str} 23:59:59' -delete 2>/dev/null || echo 'done'",
        f"删除 {date_str} 的标准化视频"
    )
    
    execute_docker_command(
        "social-media-hub-standardizer-1",
        f"find /app/videos/standardized/{account} -type d -empty -delete 2>/dev/null || echo 'done'",
        "清理标准化空文件夹"
    )
    
    # 5. 查询并删除合并视频
    print("\n5️⃣ 查询并删除合并视频...")
    success, output = execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/merges/{account}_merged_record.json'; "
        f"data=json.load(open(log_file)) if os.path.exists(log_file) else {{'merged_videos':[]}}; "
        f"today_merges=[m for m in data['merged_videos'] if m.get('timestamp','')[:10]=='{date_str}']; "
        f"print('\\n'.join([m.get('output_file','') for m in today_merges]))\"",
        f"查询 {date_str} 的合并记录"
    )
    
    if success and output.strip():
        merged_files = [f.strip() for f in output.strip().split('\n') if f.strip()]
        for merged_file in merged_files:
            filename = os.path.basename(merged_file)
            execute_docker_command(
                "social-media-hub-merger-1",
                f"rm -f '/app/videos/merged/{account}/{filename}'",
                f"删除合并视频: {filename}"
            )
    
    # 6. 删除合并记录
    print("\n6️⃣ 删除合并记录（回退序号）...")
    execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/merges/{account}_merged_record.json'; "
        f"data=json.load(open(log_file)) if os.path.exists(log_file) else {{'merged_videos':[]}}; "
        f"data['merged_videos']=[m for m in data['merged_videos'] if m.get('timestamp','')[:10]!='{date_str}']; "
        f"json.dump(data,open(log_file,'w'),indent=2,ensure_ascii=False)\"",
        f"删除 {date_str} 的合并记录"
    )
    
    # 7. 清理Redis缓存
    print("\n7️⃣ 清理Redis缓存...")
    execute_docker_command(
        "social-media-hub-redis-1",
        f"redis-cli DEL merge_result_{account}",
        "清理合并结果缓存"
    )
    
    execute_docker_command(
        "social-media-hub-redis-1",
        f"redis-cli DEL standardize_result_{account}",
        "清理标准化结果缓存"
    )
    
    print("\n✅ 回退完成！")
    print("\n⚠️  提醒: 如果已上传到B站，请手动删除视频")
    print("   访问: https://member.bilibili.com/platform/upload-manager/article")


def rollback_from_record(record_file):
    """从测试记录文件回退"""
    print(f"📄 从记录文件回退: {record_file}")
    print("="*60)
    
    if not os.path.exists(record_file):
        print(f"❌ 记录文件不存在: {record_file}")
        return
    
    with open(record_file, 'r', encoding='utf-8') as f:
        record = json.load(f)
    
    account = record.get('account', 'ai_vanvan')
    print(f"📱 账号: {account}")
    print(f"⏰ 测试时间: {record.get('start_time', 'unknown')}")
    
    # 删除下载的视频
    print("\n1️⃣ 删除下载的视频...")
    for video in record.get('downloaded_videos', []):
        execute_docker_command(
            "social-media-hub-downloader-1",
            f"rm -f '{video}'",
            f"删除: {os.path.basename(video)}"
        )
    
    # 删除标准化文件夹
    print("\n2️⃣ 删除标准化文件夹...")
    for folder in record.get('standardized_folders', []):
        execute_docker_command(
            "social-media-hub-standardizer-1",
            f"rm -rf '{folder}'",
            f"删除: {folder}"
        )
    
    # 删除合并视频
    print("\n3️⃣ 删除合并视频...")
    for video in record.get('merged_videos', []):
        filename = os.path.basename(video)
        execute_docker_command(
            "social-media-hub-merger-1",
            f"rm -f '/app/videos/merged/{account}/{filename}'",
            f"删除: {filename}"
        )
    
    # 删除合并记录
    print("\n4️⃣ 删除合并记录...")
    execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/merges/{account}_merged_record.json'; "
        f"data=json.load(open(log_file)) if os.path.exists(log_file) else {{'merged_videos':[]}}; "
        f"data['merged_videos']=data['merged_videos'][:-1] if data['merged_videos'] else []; "
        f"json.dump(data,open(log_file,'w'),indent=2,ensure_ascii=False)\"",
        "删除最后一条合并记录"
    )
    
    # 显示上传的视频
    if record.get('uploaded_videos'):
        print("\n⚠️  需要手动删除B站视频:")
        for upload in record['uploaded_videos']:
            print(f"   - {os.path.basename(upload.get('local_path', ''))}")
            if upload.get('bilibili_url'):
                print(f"     链接: {upload['bilibili_url']}")
    
    print("\n✅ 回退完成！")


def rollback_last_merge(account):
    """回退最后一次合并"""
    print(f"🔙 回退 {account} 最后一次合并")
    print("="*60)
    
    # 1. 获取最后一次合并记录
    print("\n1️⃣ 查询最后一次合并...")
    success, output = execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/merges/{account}_merged_record.json'; "
        f"data=json.load(open(log_file)) if os.path.exists(log_file) else {{'merged_videos':[]}}; "
        f"last=data['merged_videos'][-1] if data['merged_videos'] else None; "
        f"print(json.dumps(last) if last else '')\"",
        "读取最后一次合并记录"
    )
    
    if not success or not output.strip():
        print("❌ 没有找到合并记录")
        return
    
    last_merge = json.loads(output.strip())
    print(f"📋 最后一次合并:")
    print(f"   时间: {last_merge.get('timestamp', 'unknown')}")
    print(f"   输出: {last_merge.get('output_file', 'unknown')}")
    print(f"   输入: {last_merge.get('input_count', 0)} 个视频")
    
    confirm = input("\n确认删除这次合并？(yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ 已取消")
        return
    
    # 2. 删除合并视频
    print("\n2️⃣ 删除合并视频...")
    output_file = last_merge.get('output_file', '')
    if output_file:
        filename = os.path.basename(output_file)
        execute_docker_command(
            "social-media-hub-merger-1",
            f"rm -f '/app/videos/merged/{account}/{filename}'",
            f"删除: {filename}"
        )
    
    # 3. 删除合并记录
    print("\n3️⃣ 删除合并记录...")
    execute_docker_command(
        "social-media-hub-merger-1",
        f"python -c \"import json,os; "
        f"log_file='/app/logs/merges/{account}_merged_record.json'; "
        f"data=json.load(open(log_file)); "
        f"data['merged_videos'].pop(); "
        f"json.dump(data,open(log_file,'w'),indent=2,ensure_ascii=False)\"",
        "删除记录（序号回退）"
    )
    
    # 4. 清理Redis
    print("\n4️⃣ 清理Redis缓存...")
    execute_docker_command(
        "social-media-hub-redis-1",
        f"redis-cli DEL merge_result_{account}",
        "清理缓存"
    )
    
    print("\n✅ 回退完成！")


def main():
    parser = argparse.ArgumentParser(description='测试数据回退工具')
    parser.add_argument('--account', default='ai_vanvan', help='账号名称')
    parser.add_argument('--date', help='回退指定日期的数据 (YYYY-MM-DD)')
    parser.add_argument('--record', help='从测试记录文件回退')
    parser.add_argument('--last-merge', action='store_true', help='回退最后一次合并')
    parser.add_argument('--today', action='store_true', help='回退今天的数据')
    
    args = parser.parse_args()
    
    if args.record:
        rollback_from_record(args.record)
    elif args.last_merge:
        rollback_last_merge(args.account)
    elif args.today:
        today = datetime.now().strftime('%Y-%m-%d')
        rollback_by_date(args.account, today)
    elif args.date:
        rollback_by_date(args.account, args.date)
    else:
        print("请指定回退方式:")
        print("  --today              回退今天的数据")
        print("  --date YYYY-MM-DD    回退指定日期")
        print("  --last-merge         回退最后一次合并")
        print("  --record FILE        从记录文件回退")
        print("\n示例:")
        print("  python rollback_tool.py --today")
        print("  python rollback_tool.py --date 2025-10-17")
        print("  python rollback_tool.py --last-merge")
        print("  python rollback_tool.py --record test_record_20251017_143000.json")


if __name__ == "__main__":
    main()
