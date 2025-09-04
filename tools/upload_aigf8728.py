#!/usr/bin/env python3
"""
aigf8728专用上传工具 - 保持浏览器打开
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.platforms.bilibili.uploader import BilibiliUploader

def upload_aigf8728_with_browser_keep_alive(video_path=None):
    """启动aigf8728上传，浏览器保持打开"""
    print("🚀 启动 aigf8728 专用上传工具")
    print("=" * 50)
    
    if not video_path:
        video_path = "videos/merged/aigf8728/test_video.mp4"
    
    print(f"📤 准备上传: {video_path}")
    print(f"📱 账号: aigf8728")
    print("🏷️ 分区: 手动选择（跳过自动设置）")
    print()
    
    try:
        # 创建上传器
        uploader = BilibiliUploader("aigf8728")
        
        # 启动浏览器（不会自动关闭）
        if uploader.setup_driver():
            print("✅ Chrome启动成功")
            print("🌐 打开B站上传页面...")
            
            try:
                uploader.driver.get("https://member.bilibili.com/platform/upload/video/")
                time.sleep(3)
                
                current_url = uploader.driver.current_url
                if "upload" in current_url:
                    print("✅ 已到达上传页面")
                    print("💡 请在浏览器中手动选择视频文件和完成上传")
                else:
                    print("🔑 需要登录 - 请在浏览器中扫码登录")
                    print("📋 登录后请手动导航到: https://member.bilibili.com/platform/upload/video/")
                
                print("\n" + "=" * 50)
                print("🔒 浏览器将保持打开状态")
                print("💡 请在浏览器中完成以下操作：")
                print("   1. 登录B站账户（如果需要）")
                print("   2. 上传视频文件")
                print("   3. 设置标题（建议: ins你的海外第6个女友:博主名）")
                print("   4. 选择合适的分区")
                print("   5. 发布视频")
                print("\n🛑 完成后请按 Ctrl+C 退出程序")
                print("=" * 50)
                
                # 保持程序运行，浏览器不关闭
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 用户退出程序")
                    print("🔒 浏览器将保持打开状态")
                    
            except Exception as e:
                print(f"⚠️ 打开页面时出错: {e}")
                print("🔒 浏览器保持打开，请手动操作")
                
                # 保持程序运行
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 用户退出程序")
        else:
            print("❌ Chrome启动失败")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    video_path = sys.argv[1] if len(sys.argv) > 1 else None
    upload_aigf8728_with_browser_keep_alive(video_path)
