#!/usr/bin/env python3
"""
快速Chrome测试 - 带输出捕获
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== 快速Chrome测试 ===")
    uploader = None
    
    try:
        # 初始化
        uploader = BilibiliUploader("ai_vanvan")
        print("✅ 上传器初始化成功")
        
        # 启动浏览器
        print("🚀 启动Chrome...")
        uploader._init_browser()
        print("✅ Chrome启动成功")
        
        # 快速测试
        print("🌐 访问B站...")
        uploader.driver.get("https://www.bilibili.com")
        
        # 等待页面加载
        print("⏳ 等待页面加载...")
        time.sleep(5)
        
        # 获取基础信息
        title = uploader.driver.title
        url = uploader.driver.current_url
        
        print(f"📄 页面标题: {title}")
        print(f"📍 当前URL: {url}")
        
        # 简单的登录检查
        page_source = uploader.driver.page_source
        if "登录" in page_source and "扫码登录" in page_source:
            print("⚠️ 检测到登录页面，需要登录")
        elif "个人中心" in page_source or "投稿" in page_source:
            print("✅ 检测到用户功能，已登录")
        else:
            print("❓ 登录状态不明确")
        
        print("✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        print("🧹 清理浏览器...")
        try:
            if uploader and hasattr(uploader, 'driver'):
                uploader.driver.quit()
                print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️ 浏览器清理异常: {e}")

if __name__ == "__main__":
    main()
