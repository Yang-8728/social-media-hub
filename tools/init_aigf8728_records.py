#!/usr/bin/env python3
"""
为 aigf8728 账户初始化下载和合并记录
将所有已存在的视频标记为已下载和已合并
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

def scan_existing_videos():
    """扫描已存在的视频文件"""
    print("🔍 扫描 aigf8728 已存在的视频文件...")
    
    # 定义可能的视频目录
    video_dirs = [
        "c:\\Code\\social-media-hub\\videos\\downloads\\aigf8728",
        "c:\\Code\\social-media-hub\\videos\\merged\\aigf8728",
        "c:\\Code\\social-media-hub\\data\\downloads\\aigf8728", 
        "c:\\Code\\social-media-hub\\data\\merged\\aigf8728"
    ]
    
    found_videos = set()
    
    for video_dir in video_dirs:
        if os.path.exists(video_dir):
            print(f"📁 扫描目录: {video_dir}")
            
            # 递归扫描所有子目录
            for root, dirs, files in os.walk(video_dir):
                for file in files:
                    if file.endswith(('.mp4', '.mov', '.avi')):
                        # 提取 shortcode (通常在文件名中)
                        filename = os.path.splitext(file)[0]
                        
                        # 尝试从文件名提取 shortcode
                        # 常见格式: 2025-09-04_username_shortcode.mp4
                        # 或者: shortcode.mp4
                        parts = filename.split('_')
                        if len(parts) >= 3:
                            shortcode = parts[-1]  # 最后一部分通常是 shortcode
                        else:
                            shortcode = filename
                        
                        # 验证 shortcode 格式 (Instagram shortcode 通常是 11 位字母数字)
                        if len(shortcode) >= 10 and shortcode.isalnum():
                            found_videos.add(shortcode)
                            print(f"  ✅ 发现视频: {shortcode} ({file})")
    
    return list(found_videos)

def initialize_aigf8728_records():
    """初始化 aigf8728 的下载和合并记录"""
    print("🚀 开始初始化 aigf8728 记录...")
    print("=" * 60)
    
    # 创建 logger
    logger = Logger("aigf8728")
    
    # 扫描已存在的视频
    existing_videos = scan_existing_videos()
    
    if not existing_videos:
        print("ℹ️  没有发现已存在的视频文件")
        return
    
    print(f"\n📊 发现 {len(existing_videos)} 个已存在的视频")
    
    # 标记为已下载
    print(f"\n📥 标记为已下载...")
    download_count = 0
    for shortcode in existing_videos:
        if not logger.is_downloaded(shortcode):
            # 创建下载记录
            record = {
                "shortcode": shortcode,
                "url": f"https://instagram.com/p/{shortcode}/",
                "download_time": datetime.now().isoformat(),
                "status": "downloaded",
                "imported": True,  # 标记为导入的记录
                "note": "初始化时导入的已存在视频"
            }
            logger.log_download(shortcode, record)
            download_count += 1
            print(f"  ✅ {shortcode}")
        else:
            print(f"  ⏭️  {shortcode} (已有记录)")
    
    # 标记为已合并
    print(f"\n🔗 标记为已合并...")
    merge_count = 0
    for shortcode in existing_videos:
        if not logger.is_merged(shortcode):
            # 创建合并记录
            merge_record = {
                "shortcode": shortcode,
                "merged_time": datetime.now().isoformat(),
                "status": "merged", 
                "imported": True,  # 标记为导入的记录
                "note": "初始化时导入的已存在视频"
            }
            logger.log_merge(shortcode, merge_record)
            merge_count += 1
            print(f"  ✅ {shortcode}")
        else:
            print(f"  ⏭️  {shortcode} (已有记录)")
    
    # 显示结果
    print(f"\n" + "=" * 60)
    print(f"✅ 初始化完成！")
    print(f"📥 新增下载记录: {download_count} 个")
    print(f"🔗 新增合并记录: {merge_count} 个")
    print(f"📁 日志文件位置:")
    print(f"  下载日志: {logger.download_log_file}")
    print(f"  合并日志: {logger.merged_record_file}")
    
    return download_count, merge_count

def verify_records():
    """验证记录是否正确创建"""
    print(f"\n🔍 验证记录...")
    logger = Logger("aigf8728")
    
    # 检查日志文件是否存在
    if os.path.exists(logger.download_log_file):
        with open(logger.download_log_file, 'r', encoding='utf-8') as f:
            download_records = json.load(f)
        print(f"✅ 下载记录文件存在: {len(download_records)} 条记录")
    else:
        print(f"❌ 下载记录文件不存在")
    
    if os.path.exists(logger.merged_record_file):
        with open(logger.merged_record_file, 'r', encoding='utf-8') as f:
            merge_records = json.load(f)
        print(f"✅ 合并记录文件存在: {len(merge_records)} 条记录")
    else:
        print(f"❌ 合并记录文件不存在")

if __name__ == "__main__":
    print("🎯 aigf8728 记录初始化工具")
    print("将所有已存在的视频标记为已下载和已合并")
    print()
    
    if input("确认开始初始化？(y/N): ").lower() == 'y':
        download_count, merge_count = initialize_aigf8728_records()
        verify_records()
        
        print(f"\n🎉 所有操作完成！")
        print(f"现在 aigf8728 账户的记录已经与 ai_vanvan 一样完整了")
    else:
        print("❌ 操作已取消")
