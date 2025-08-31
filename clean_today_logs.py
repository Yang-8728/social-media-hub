#!/usr/bin/env python3
"""
清理今天的下载和合并日志记录
"""
import json
from datetime import datetime
from pathlib import Path

def clean_today_logs():
    """清理今天的所有日志记录"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = Path("videos/download_logs/ai_vanvan_downloads.json")
    
    if not log_file.exists():
        print("日志文件不存在")
        return
    
    # 加载日志
    with open(log_file, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    # 统计清理前的数量
    original_downloads = len(log_data.get("downloads", []))
    original_merges = len(log_data.get("merged_sessions", []))
    
    # 清理今天的下载记录
    cleaned_downloads = []
    removed_downloads = 0
    
    for download in log_data.get("downloads", []):
        download_time = download.get("download_time", "")
        if not download_time.startswith(today):
            cleaned_downloads.append(download)
        else:
            removed_downloads += 1
    
    # 清理今天的合并记录
    cleaned_merges = []
    removed_merges = 0
    
    for merge in log_data.get("merged_sessions", []):
        merge_time = merge.get("merge_time", "")
        if not merge_time.startswith(today):
            cleaned_merges.append(merge)
        else:
            removed_merges += 1
    
    # 更新日志数据
    log_data["downloads"] = cleaned_downloads
    log_data["merged_sessions"] = cleaned_merges
    
    # 保存清理后的日志
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ 清理完成!")
    print(f"📥 下载记录: {original_downloads} -> {len(cleaned_downloads)} (删除 {removed_downloads} 条)")
    print(f"🔄 合并记录: {original_merges} -> {len(cleaned_merges)} (删除 {removed_merges} 条)")

if __name__ == "__main__":
    clean_today_logs()
