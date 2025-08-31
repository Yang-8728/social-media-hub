#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将今天下载的视频复制到广告文件夹
"""

import os
import shutil
import json
import lzma
from pathlib import Path
from datetime import datetime, date
import sys
sys.path.append('src')

from utils.logger import Logger

def copy_todays_videos_to_ads():
    """将今天下载的视频复制到广告文件夹"""
    print("📱 复制今天下载的视频到广告文件夹")
    print("=" * 50)
    
    # 初始化日志器
    logger = Logger("ai_vanvan")
    
    # 获取今天的日期
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    print(f"📅 目标日期: {today_str}")
    
    # 加载下载日志
    log_data = logger.load_download_log()
    
    # 筛选今天下载的视频
    todays_downloads = []
    for download in log_data["downloads"]:
        if download["status"] == "success":
            # 检查下载时间
            download_time = download.get("timestamp", "")
            if download_time.startswith(today_str):
                todays_downloads.append(download)
    
    if not todays_downloads:
        print("❌ 今天没有下载任何视频")
        return
    
    print(f"🎯 找到今天下载的视频: {len(todays_downloads)} 个")
    
    # 创建广告文件夹
    ads_folder = Path("data/downloads/ai_vanvan") / "2025-08-27" / "广告"
    ads_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 广告文件夹: {ads_folder}")
    
    copied_count = 0
    failed_count = 0
    
    for download in todays_downloads:
        shortcode = download["shortcode"]
        folder_path = download.get("folder", "")
        
        if not folder_path or not os.path.exists(folder_path):
            print(f"❌ 文件夹不存在: {folder_path}")
            failed_count += 1
            continue
        
        # 查找与shortcode相关的所有文件
        related_files = []
        for file in os.listdir(folder_path):
            # 查找包含shortcode的文件，或者json.xz文件中包含该shortcode的
            if shortcode in file:
                related_files.append(file)
            elif file.endswith('.json.xz'):
                # 检查json.xz文件内容
                try:
                    json_path = os.path.join(folder_path, file)
                    with lzma.open(json_path, 'rb') as f:
                        data = json.loads(f.read().decode('utf-8'))
                        if data.get('node', {}).get('shortcode') == shortcode:
                            related_files.append(file)
                            # 还要找对应的媒体文件
                            base_name = file.replace('.json.xz', '')
                            for media_file in os.listdir(folder_path):
                                if media_file.startswith(base_name) and not media_file.endswith('.json.xz'):
                                    if media_file not in related_files:
                                        related_files.append(media_file)
                except Exception as e:
                    continue
        
        if not related_files:
            print(f"❌ 没找到 {shortcode} 的相关文件")
            failed_count += 1
            continue
        
        # 复制文件到广告文件夹
        video_copied = False
        for file in related_files:
            src_path = os.path.join(folder_path, file)
            dst_path = ads_folder / file
            
            try:
                shutil.copy2(src_path, dst_path)
                if file.endswith(('.mp4', '.jpg', '.png')):
                    video_copied = True
                    print(f"✅ 复制: {file}")
            except Exception as e:
                print(f"❌ 复制失败 {file}: {e}")
                failed_count += 1
        
        if video_copied:
            copied_count += 1
    
    print(f"\n📊 复制完成:")
    print(f"   ✅ 成功复制: {copied_count} 个视频")
    print(f"   ❌ 复制失败: {failed_count} 个")
    print(f"   📁 目标文件夹: {ads_folder}")
    
    # 显示广告文件夹内容
    if ads_folder.exists():
        ads_files = list(ads_folder.glob("*"))
        print(f"\n📁 广告文件夹内容: {len(ads_files)} 个文件")
        for file in ads_files[:10]:  # 显示前10个文件
            print(f"   📄 {file.name}")
        if len(ads_files) > 10:
            print(f"   ... 及其他 {len(ads_files) - 10} 个文件")

def main():
    copy_todays_videos_to_ads()

if __name__ == "__main__":
    main()
