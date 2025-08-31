#!/usr/bin/env python3
"""
检查B站投稿管理页面
查看上传的视频状态
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== 检查B站投稿状态 ===")
    
    try:
        uploader = BilibiliUploader("ai_vanvan")
        uploader._init_browser()
        
        # 访问投稿管理页面
        print("📋 访问投稿管理页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup/manage")
        time.sleep(5)
        
        current_url = uploader.driver.current_url
        page_title = uploader.driver.title
        
        print(f"📍 当前页面: {current_url}")
        print(f"📄 页面标题: {page_title}")
        
        # 检查是否有投稿记录
        page_source = uploader.driver.page_source
        
        if "暂无投稿" in page_source or "没有投稿" in page_source:
            print("⚠️ 页面显示暂无投稿记录")
        elif "审核中" in page_source:
            print("🔄 有视频正在审核中")
        elif "已通过" in page_source:
            print("✅ 有视频已通过审核")
        elif "未通过" in page_source:
            print("❌ 有视频审核未通过")
        else:
            print("❓ 无法确定投稿状态")
        
        # 截图保存
        screenshot_path = os.path.join("logs", "screenshots", f"manage_page_{int(time.time())}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        uploader.driver.save_screenshot(screenshot_path)
        print(f"📸 页面截图已保存: {screenshot_path}")
        
        # 检查页面上的投稿数量
        try:
            # 查找投稿列表
            video_items = uploader.driver.find_elements("css selector", "[class*='video'], [class*='item'], .list-item")
            print(f"📊 页面上找到 {len(video_items)} 个投稿项目")
        except Exception as e:
            print(f"⚠️ 无法统计投稿数量: {e}")
        
        print("⏸️ 浏览器将保持打开15秒供检查...")
        time.sleep(15)
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            if hasattr(uploader, 'driver'):
                uploader.driver.quit()
                print("🧹 浏览器已关闭")
        except:
            pass

if __name__ == "__main__":
    main()
