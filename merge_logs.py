#!/usr/bin/env python3
"""合并data和videos文件夹中的下载记录"""

import json
import shutil
from pathlib import Path

def merge_download_logs():
    """合并下载记录"""
    data_file = Path("data/download_logs/ai_vanvan_downloads.json")
    videos_file = Path("videos/download_logs/ai_vanvan_downloads.json")
    
    if not data_file.exists():
        print("❌ data文件夹中没有记录文件")
        return
    
    if not videos_file.exists():
        print("❌ videos文件夹中没有记录文件")
        return
    
    # 读取两个文件
    with open(data_file, 'r', encoding='utf-8') as f:
        data_records = json.load(f)
    
    with open(videos_file, 'r', encoding='utf-8') as f:
        videos_records = json.load(f)
    
    print(f"data文件夹记录数: {len(data_records['downloads'])}")
    print(f"videos文件夹记录数: {len(videos_records['downloads'])}")
    
    # 合并记录（data中的今天记录 + videos中的历史记录）
    # 创建shortcode集合避免重复
    videos_shortcodes = {d["shortcode"] for d in videos_records["downloads"]}
    
    new_records = []
    for record in data_records["downloads"]:
        if record["shortcode"] not in videos_shortcodes:
            new_records.append(record)
    
    print(f"需要添加的新记录: {len(new_records)}")
    
    # 合并到videos文件
    videos_records["downloads"].extend(new_records)
    
    # 保存合并后的记录
    with open(videos_file, 'w', encoding='utf-8') as f:
        json.dump(videos_records, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ 合并完成！总记录数: {len(videos_records['downloads'])}")
    
    # 备份data文件夹的记录
    backup_file = Path("data/download_logs/ai_vanvan_downloads.json.backup")
    shutil.copy2(data_file, backup_file)
    print(f"📦 已备份data记录到: {backup_file}")

if __name__ == "__main__":
    merge_download_logs()
