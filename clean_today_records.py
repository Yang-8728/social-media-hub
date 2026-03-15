#!/usr/bin/env python3
"""清理今天的下载和合并记录"""
import json
import os
from datetime import datetime

def clean_download_records(account_name, target_date):
    """清理下载记录中指定日期的数据"""
    log_file = f"logs/downloads/{account_name}_downloads.json"
    
    if not os.path.exists(log_file):
        print(f"❌ 下载记录文件不存在: {log_file}")
        return
    
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data.get('downloads', []))
    
    # 过滤掉今天的记录
    data['downloads'] = [
        d for d in data.get('downloads', [])
        if not d.get('download_time', '').startswith(target_date)
    ]
    
    removed_count = original_count - len(data['downloads'])
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 下载记录: 删除 {removed_count} 条记录 (剩余 {len(data['downloads'])} 条)")

def clean_merge_records(account_name, target_date):
    """清理合并记录中指定日期的数据"""
    log_file = f"logs/merges/{account_name}_merged_record.json"
    
    if not os.path.exists(log_file):
        print(f"❌ 合并记录文件不存在: {log_file}")
        return
    
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data.get('merged_videos', []))
    
    # 过滤掉今天的记录
    data['merged_videos'] = [
        m for m in data.get('merged_videos', [])
        if not m.get('timestamp', '').startswith(target_date)
    ]
    
    removed_count = original_count - len(data['merged_videos'])
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 合并记录: 删除 {removed_count} 条记录 (剩余 {len(data['merged_videos'])} 条)")

if __name__ == "__main__":
    account = "ai_vanvan"
    today = "2025-10-28"
    
    print(f"🔄 清理 {account} 账号 {today} 的记录...")
    print("="*60)
    
    clean_download_records(account, today)
    clean_merge_records(account, today)
    
    print("="*60)
    print("✅ 清理完成！")
