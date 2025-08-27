#!/usr/bin/env python3
"""测试预扫描功能，不实际下载"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.platforms.instagram.downloader import InstagramDownloader
from src.core.models import Account
from src.utils.logger import Logger

def test_prescan():
    """测试预扫描功能"""
    print("🔍 开始预扫描测试...")
    
    # 创建账号和下载器
    account = Account(name="ai_vanvan", username="ai_vanvan", platform="instagram")
    downloader = InstagramDownloader()
    logger = Logger("ai_vanvan")
    
    # 登录
    print("🔐 正在登录...")
    if not downloader.login(account):
        print("❌ 登录失败")
        return
    
    print("✅ 登录成功")
    
    # 模拟预扫描逻辑
    print("📊 开始预扫描...")
    
    try:
        from instaloader import Profile
        profile = Profile.from_username(downloader.loader.context, account.username)
        saved_posts = profile.get_saved_posts()
        
        # 预扫描参数
        MAX_PROCESS_COUNT = 50  # 最大下载数量
        scan_limit = min(MAX_PROCESS_COUNT, 50)  # 最多扫描50个posts
        
        print(f"📋 扫描参数: 最大下载{MAX_PROCESS_COUNT}个, 最多扫描{scan_limit}个posts")
        
        new_videos = []
        scan_count = 0
        
        for post in saved_posts:
            scan_count += 1
            if scan_count > scan_limit:
                print(f"⏹️  扫描了 {scan_limit} 个posts，停止扫描")
                break
                
            shortcode = post.shortcode
            is_downloaded = logger.is_downloaded(shortcode)
            
            if scan_count <= 10:  # 显示前10个的详细信息
                status = "已下载" if is_downloaded else "新视频"
                print(f"  {scan_count:2d}. {shortcode} - {status}")
            
            if not is_downloaded:
                new_videos.append(post)
                if len(new_videos) >= MAX_PROCESS_COUNT:
                    print(f"🎯 找到足够的新视频({MAX_PROCESS_COUNT}个)，停止扫描")
                    break
        
        print(f"\n📈 扫描结果:")
        print(f"  扫描了 {scan_count} 个posts")
        print(f"  发现 {len(new_videos)} 个新视频")
        print(f"  跳过 {scan_count - len(new_videos)} 个已下载")
        
        if len(new_videos) > 0:
            actual_download_count = min(len(new_videos), MAX_PROCESS_COUNT)
            print(f"  计划下载 {actual_download_count} 个视频")
            
            print(f"\n🎬 前5个新视频:")
            for i, post in enumerate(new_videos[:5]):
                print(f"  {i+1}. {post.shortcode}")
        else:
            print("  📭 没有新视频需要下载")
            
    except Exception as e:
        print(f"❌ 预扫描出错: {e}")

if __name__ == "__main__":
    test_prescan()
