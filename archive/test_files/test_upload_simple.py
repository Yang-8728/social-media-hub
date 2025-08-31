#!/usr/bin/env python3
"""
简单的B站上传测试脚本
专注于诊断上传问题
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== 简单B站上传测试 ===")
    
    # 测试视频文件
    test_video = r"c:\Code\social-media-hub\temp\test_upload.mp4"
    if not os.path.exists(test_video):
        print(f"❌ 测试视频不存在: {test_video}")
        return
    
    print(f"✅ 测试视频: {test_video}")
    
    # 初始化上传器
    print("🔧 初始化上传器...")
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("✅ 上传器初始化成功")
    except Exception as e:
        print(f"❌ 上传器初始化失败: {e}")
        return
    
    # 测试浏览器初始化
    print("🌐 测试浏览器启动...")
    try:
        # 直接调用内部方法测试
        uploader._init_browser()
        print("✅ 浏览器启动成功")
        
        # 检查当前页面
        current_url = uploader.driver.current_url
        print(f"📍 当前页面: {current_url}")
        
        # 导航到登录页面测试
        uploader.driver.get("https://www.bilibili.com")
        time.sleep(3)
        
        # 检查登录状态
        try:
            # 查找用户信息元素
            user_elements = uploader.driver.find_elements("css selector", "[data-v-6e5a8b74]")
            if user_elements:
                print("✅ 检测到用户信息，可能已登录")
            else:
                print("⚠️ 未检测到用户信息")
        except Exception as e:
            print(f"⚠️ 登录状态检查异常: {e}")
        
        # 导航到上传页面
        print("📤 尝试访问上传页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup")
        time.sleep(5)
        
        current_url = uploader.driver.current_url
        print(f"📍 上传页面URL: {current_url}")
        
        # 检查页面标题
        page_title = uploader.driver.title
        print(f"📄 页面标题: {page_title}")
        
        # 等待用户确认
        print("⏸️ 浏览器将保持打开状态10秒，请检查页面...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 浏览器测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理
        try:
            if hasattr(uploader, 'driver'):
                uploader.driver.quit()
                print("🧹 浏览器已关闭")
        except:
            pass

if __name__ == "__main__":
    main()
