#!/usr/bin/env python3
"""从日志文件中恢复今天的下载记录"""

import os
import sys
import re
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def extract_shortcodes_from_log():
    """从今天的日志文件中提取下载成功的shortcode"""
    log_file = "logs/2025-08-25-ai_vanvan.log"
    
    if not os.path.exists(log_file):
        print(f"❌ 日志文件不存在: {log_file}")
        return []
    
    shortcodes = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 查找 "下载记录: SHORTCODE -> path" 的模式
            match = re.search(r'下载记录: ([A-Za-z0-9_-]+) ->', line)
            if match:
                shortcode = match.group(1)
                shortcodes.append(shortcode)
    
    print(f"从日志中提取到 {len(shortcodes)} 个shortcode")
    return shortcodes

def recover_download_records():
    """恢复下载记录"""
    shortcodes = extract_shortcodes_from_log()
    
    if not shortcodes:
        print("没有找到需要恢复的记录")
        return
    
    logger = Logger("ai_vanvan")
    log_data = logger.load_download_log()
    
    # 检查哪些记录缺失
    existing_shortcodes = {d["shortcode"] for d in log_data["downloads"]}
    missing_shortcodes = [sc for sc in shortcodes if sc not in existing_shortcodes]
    
    print(f"需要恢复 {len(missing_shortcodes)} 条记录")
    
    for shortcode in missing_shortcodes:
        # 添加恢复的记录
        download_record = {
            "shortcode": shortcode,
            "download_time": "2025-08-25T22:00:00",  # 使用今天的时间
            "status": "success",
            "file_path": f"videos/downloads/ai_vanvan/2025-08-25",
            "error": "",
            "merged": False,
            "download_folder": "videos/downloads/ai_vanvan/2025-08-25",
            "blogger_name": "unknown"
        }
        log_data["downloads"].append(download_record)
        print(f"✅ 恢复记录: {shortcode}")
    
    # 保存更新后的记录
    logger.save_download_log(log_data)
    
    print(f"🎉 恢复完成！总记录数: {len(log_data['downloads'])}")

if __name__ == "__main__":
    recover_download_records()
