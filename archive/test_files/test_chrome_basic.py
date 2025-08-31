#!/usr/bin/env python3
"""
最简单的Chrome启动测试
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== 最简单Chrome测试 ===")
    
    # 初始化上传器
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("✅ 上传器初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 启动浏览器
    try:
        print("🚀 启动Chrome...")
        uploader._init_browser()
        print("✅ Chrome启动成功")
        
        # 访问B站首页
        print("🌐 访问B站首页...")
        uploader.driver.get("https://www.bilibili.com")
        time.sleep(3)
        
        title = uploader.driver.title
        url = uploader.driver.current_url
        print(f"📄 页面标题: {title}")
        print(f"📍 当前URL: {url}")
        
        # 检查登录状态
        try:
            # 查找用户头像或用户名
            user_info = uploader.driver.find_elements("css selector", ".header-avatar-wrap")
            if user_info:
                print("✅ 检测到用户头像，已登录")
            else:
                print("⚠️ 未检测到用户头像")
                
            # 查找登录按钮
            login_btn = uploader.driver.find_elements("css selector", ".header-login-entry")
            if login_btn:
                print("⚠️ 检测到登录按钮，未登录")
            else:
                print("✅ 未检测到登录按钮，可能已登录")
                
        except Exception as e:
            print(f"⚠️ 登录状态检查异常: {e}")
        
        print("✅ 测试完成，5秒后关闭浏览器")
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭浏览器
        try:
            if hasattr(uploader, 'driver'):
                uploader.driver.quit()
                print("🧹 浏览器已关闭")
        except:
            print("⚠️ 浏览器关闭异常")

if __name__ == "__main__":
    main()
