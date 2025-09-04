#!/usr/bin/env python3
"""
扫描 aigf8728 的新收藏视频，并将它们标记为已下载和已合并
这样下次扫描就不会重复处理了
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.platforms.instagram.downloader import InstagramDownloader
from src.core.models import Account
from src.utils.logger import Logger

def scan_and_mark_new_videos():
    """扫描新收藏视频并标记为已处理"""
    print("🔍 扫描 aigf8728 新收藏视频并标记为已处理...")
    print("=" * 60)
    
    # 创建账户对象
    account = Account(
        name="aigf8728",
        platform="instagram", 
        username="aigf8728"
    )
    
    # 加载配置
    try:
        with open("config/accounts.json", "r", encoding="utf-8") as f:
            config_data = json.load(f)
        account.config = config_data.get("aigf8728", {})
        print(f"✅ 加载配置成功")
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        return
    
    # 创建下载器和 logger
    downloader = InstagramDownloader()
    logger = Logger("aigf8728")
    
    # 登录
    print("🔐 正在登录...")
    if not downloader.login(account):
        print("❌ 登录失败")
        return
    
    print("✅ 登录成功")
    
    # 扫描收藏的视频
    print("\n📋 扫描收藏的视频...")
    try:
        from instaloader import Profile
        profile = Profile.from_username(downloader.loader.context, account.username)
        saved_posts = profile.get_saved_posts()
        
        new_videos = []
        scanned_count = 0
        max_scan = 50  # 扫描更多一些
        
        for post in saved_posts:
            scanned_count += 1
            if scanned_count > max_scan:
                print(f"⏹️  扫描了 {max_scan} 个posts，停止扫描")
                break
                
            shortcode = post.shortcode
            
            # 检查是否已下载
            is_downloaded = logger.is_downloaded(shortcode)
            
            if not is_downloaded and post.is_video:
                new_videos.append({
                    'shortcode': shortcode,
                    'url': f"https://instagram.com/p/{shortcode}/",
                    'owner': post.owner_username,
                    'post': post
                })
                status = "🆕 新视频"
            elif is_downloaded:
                status = "✅ 已下载"
            else:
                status = "📷 图片/已处理"
            
            if scanned_count <= 15:  # 显示前15个的详细信息
                print(f"  {scanned_count:2d}. {shortcode} - {status} - @{post.owner_username}")
        
        print(f"\n📊 扫描结果:")
        print(f"  ✅ 扫描了 {scanned_count} 个收藏")
        print(f"  🆕 发现 {len(new_videos)} 个新视频")
        
        if new_videos:
            print(f"\n🎬 新视频列表:")
            for i, video in enumerate(new_videos, 1):
                print(f"  {i}. @{video['owner']} - {video['shortcode']}")
            
            # 询问是否标记为已处理
            print(f"\n❓ 是否将这 {len(new_videos)} 个新视频标记为已下载和已合并？")
            print("   这样下次扫描就不会再看到它们了")
            
            if input("确认标记？(y/N): ").lower() == 'y':
                mark_videos_as_processed(new_videos, logger)
            else:
                print("❌ 未标记，新视频下次扫描时仍会出现")
        else:
            print(f"\nℹ️  没有发现新视频，所有收藏都已处理过")
            
    except Exception as e:
        print(f"❌ 扫描过程出错: {e}")
        import traceback
        traceback.print_exc()

def mark_videos_as_processed(new_videos, logger):
    """将新视频标记为已下载和已合并"""
    print(f"\n🏷️  开始标记 {len(new_videos)} 个视频...")
    
    current_time = datetime.now()
    
    # 读取现有的下载记录
    downloads_file = "logs/downloads/aigf8728_downloads.json"
    if os.path.exists(downloads_file):
        with open(downloads_file, 'r', encoding='utf-8') as f:
            downloads_data = json.load(f)
    else:
        downloads_data = {"account": "aigf8728", "downloads": []}
    
    # 读取现有的合并记录
    merges_file = "logs/merges/aigf8728_merged_record.json"
    if os.path.exists(merges_file):
        with open(merges_file, 'r', encoding='utf-8') as f:
            merges_data = json.load(f)
    else:
        merges_data = {"merged_videos": []}
    
    # 添加新的下载记录
    print("📥 添加到下载记录...")
    added_downloads = 0
    for video in new_videos:
        download_record = {
            "shortcode": video['shortcode'],
            "download_time": current_time.isoformat(),
            "status": "success",
            "file_path": f"videos/downloads/aigf8728/{current_time.strftime('%Y-%m-%d')}_{video['owner']}",
            "error": "",
            "merged": True,
            "uploaded": True,
            "marked_as_processed": True,
            "note": f"标记为已处理 - @{video['owner']}"
        }
        downloads_data["downloads"].append(download_record)
        added_downloads += 1
        print(f"  ✅ {video['shortcode']} - @{video['owner']}")
    
    # 创建一个批量合并记录
    print("🔗 添加到合并记录...")
    merge_record = {
        "merge_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "output_file": f"videos\\merged\\aigf8728\\{current_time.strftime('%Y-%m-%d_%H-%M-%S')}_batch_marked.mp4",
        "input_count": len(new_videos),
        "input_videos": [f"videos\\downloads\\aigf8728\\{v['shortcode']}.mp4" for v in new_videos],
        "shortcodes": [v['shortcode'] for v in new_videos],
        "status": "success",
        "marked_as_processed": True,
        "note": f"批量标记为已处理 - {len(new_videos)} 个视频"
    }
    merges_data["merged_videos"].append(merge_record)
    
    # 保存更新后的记录
    with open(downloads_file, 'w', encoding='utf-8') as f:
        json.dump(downloads_data, f, ensure_ascii=False, indent=2)
    
    with open(merges_file, 'w', encoding='utf-8') as f:
        json.dump(merges_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 标记完成！")
    print(f"📥 添加了 {added_downloads} 条下载记录")
    print(f"🔗 添加了 1 条合并记录")
    print(f"📁 文件已更新:")
    print(f"  {downloads_file}")
    print(f"  {merges_file}")
    print(f"\n🎉 现在这些视频不会在下次扫描中出现了！")

if __name__ == "__main__":
    print("🎯 aigf8728 新视频标记工具")
    print("扫描新收藏视频并标记为已处理")
    print()
    
    scan_and_mark_new_videos()
    
    print("\n" + "=" * 60)
    print("✅ 操作完成")
