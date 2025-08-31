#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查刚才下载的39个视频是否已经记录在日志中
"""

import os
import json
import lzma
from pathlib import Path
from datetime import datetime
import sys
sys.path.append('src')

from utils.logger import Logger

def check_download_records():
    """检查下载记录"""
    print("🔍 检查刚才下载的39个视频的记录状态")
    print("=" * 60)
    
    # 初始化日志器
    logger = Logger("ai_vanvan")
    
    # 加载下载日志
    log_data = logger.load_download_log()
    
    print(f"📊 下载日志总统计:")
    total_downloads = len(log_data["downloads"])
    success_downloads = len([d for d in log_data["downloads"] if d["status"] == "success"])
    failed_downloads = len([d for d in log_data["downloads"] if d["status"] == "failed"])
    skipped_downloads = len([d for d in log_data["downloads"] if d["status"] == "skipped"])
    
    print(f"   📄 总记录数: {total_downloads}")
    print(f"   ✅ 成功下载: {success_downloads}")
    print(f"   ❌ 下载失败: {failed_downloads}")
    print(f"   ⏭️ 跳过下载: {skipped_downloads}")
    
    # 检查今天的下载记录
    today = datetime.now().date().strftime("%Y-%m-%d")
    todays_downloads = []
    
    for download in log_data["downloads"]:
        timestamp = download.get("timestamp", "")
        if timestamp.startswith(today):
            todays_downloads.append(download)
    
    print(f"\n📅 今天({today})的下载记录:")
    print(f"   📄 今天总记录: {len(todays_downloads)}")
    
    # 按时间分组显示今天的下载
    success_today = [d for d in todays_downloads if d["status"] == "success"]
    failed_today = [d for d in todays_downloads if d["status"] == "failed"]
    
    print(f"   ✅ 今天成功: {len(success_today)}")
    print(f"   ❌ 今天失败: {len(failed_today)}")
    
    # 显示最近的下载记录（按时间排序）
    if success_today:
        success_today.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        print(f"\n🕐 最近的成功下载记录:")
        for i, download in enumerate(success_today[:10], 1):
            timestamp = download.get("timestamp", "未知")
            shortcode = download.get("shortcode", "未知")
            time_part = timestamp.split("T")[1][:8] if "T" in timestamp else "未知时间"
            print(f"   {i:2}. {shortcode} ({time_part})")
        
        if len(success_today) > 10:
            print(f"   ... 及其他 {len(success_today) - 10} 条记录")
    
    # 检查21:03-21:10这个时间段的记录
    print(f"\n⏰ 检查21:03-21:10时间段的下载记录:")
    evening_downloads = []
    
    for download in success_today:
        timestamp = download.get("timestamp", "")
        if "T21:" in timestamp:
            time_part = timestamp.split("T")[1][:5]  # HH:MM
            if "21:03" <= time_part <= "21:10":
                evening_downloads.append(download)
    
    print(f"   🎯 21:03-21:10时间段: {len(evening_downloads)} 个记录")
    
    if evening_downloads:
        print(f"   📋 该时间段的shortcode:")
        for i, download in enumerate(evening_downloads, 1):
            shortcode = download.get("shortcode", "未知")
            timestamp = download.get("timestamp", "")
            time_part = timestamp.split("T")[1][:8] if "T" in timestamp else "未知"
            print(f"      {i:2}. {shortcode} ({time_part})")
    
    # 验证广告文件夹中的视频是否都有日志记录
    print(f"\n📁 验证广告文件夹中的视频记录:")
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if ads_folder.exists():
        video_files = list(ads_folder.glob("*.mp4"))
        print(f"   🎥 广告文件夹中的视频: {len(video_files)} 个")
        
        # 通过文件名找对应的shortcode
        logged_shortcodes = {d["shortcode"] for d in log_data["downloads"] if d["status"] == "success"}
        
        print(f"   📝 日志中的成功shortcode: {len(logged_shortcodes)} 个")
        
        # 检查每个视频文件是否有对应的日志记录
        missing_records = []
        found_records = []
        
        for video_file in video_files:
            # 从文件名提取时间戳，然后查找原始目录中的json文件来获取shortcode
            timestamp_part = video_file.stem  # 2025-08-26_14-00-00_UTC
            
            # 在原始目录中查找对应的json文件
            original_json = Path("videos/downloads/ai_vanvan/2025-08-27") / f"{timestamp_part}.json.xz"
            
            if original_json.exists():
                try:
                    with lzma.open(original_json, 'rb') as f:
                        data = json.loads(f.read().decode('utf-8'))
                        shortcode = data.get('node', {}).get('shortcode')
                        
                        if shortcode and shortcode in logged_shortcodes:
                            found_records.append((video_file.name, shortcode))
                        else:
                            missing_records.append((video_file.name, shortcode or "未知"))
                except Exception as e:
                    missing_records.append((video_file.name, f"解析错误: {e}"))
            else:
                missing_records.append((video_file.name, "未找到json文件"))
        
        print(f"\n📊 验证结果:")
        print(f"   ✅ 有日志记录的视频: {len(found_records)} 个")
        print(f"   ❌ 缺少日志记录的视频: {len(missing_records)} 个")
        
        if missing_records:
            print(f"\n⚠️ 缺少记录的视频:")
            for i, (filename, shortcode) in enumerate(missing_records[:5], 1):
                print(f"      {i}. {filename} (shortcode: {shortcode})")
            if len(missing_records) > 5:
                print(f"      ... 及其他 {len(missing_records) - 5} 个")
        
        # 预测再次下载的结果
        print(f"\n🔮 预测再次下载的结果:")
        if len(missing_records) == 0:
            print(f"   ✅ 所有39个视频都有日志记录")
            print(f"   📝 再次下载应该显示: '没有新视频需要下载'")
        else:
            print(f"   ⚠️ 有 {len(missing_records)} 个视频缺少日志记录")
            print(f"   📝 再次下载可能会重新下载这些视频")
    
    else:
        print(f"   ❌ 广告文件夹不存在")

def main():
    check_download_records()

if __name__ == "__main__":
    main()
