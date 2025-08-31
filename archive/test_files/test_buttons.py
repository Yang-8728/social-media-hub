#!/usr/bin/env python3
"""
专门测试B站上传页面的提交按钮
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== B站上传页面按钮检测 ===")
    
    try:
        uploader = BilibiliUploader("ai_vanvan")
        uploader._init_browser()
        
        # 访问上传页面
        print("📤 访问上传页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup")
        time.sleep(5)
        
        print("🔍 检测页面上的所有按钮...")
        
        # 查找所有按钮
        buttons = uploader.driver.find_elements("tag name", "button")
        print(f"📊 找到 {len(buttons)} 个按钮:")
        
        for i, button in enumerate(buttons):
            try:
                text = button.text.strip()
                classes = button.get_attribute("class") or ""
                visible = button.is_displayed()
                enabled = button.is_enabled()
                
                if text or "submit" in classes.lower() or "publish" in classes.lower():
                    print(f"  {i+1}. 文本: '{text}' | 类名: '{classes}' | 可见: {visible} | 可用: {enabled}")
            except:
                continue
        
        # 专门查找提交相关的按钮
        print("\n🎯 查找提交相关按钮:")
        submit_selectors = [
            "button[class*='submit']",
            "button[class*='publish']", 
            "button[class*='upload']",
            ".btn-publish",
            ".submit-btn"
        ]
        
        for selector in submit_selectors:
            try:
                elements = uploader.driver.find_elements("css selector", selector)
                if elements:
                    print(f"  ✅ {selector}: 找到 {len(elements)} 个元素")
                    for elem in elements:
                        text = elem.text.strip()
                        visible = elem.is_displayed()
                        enabled = elem.is_enabled()
                        print(f"    - 文本: '{text}' | 可见: {visible} | 可用: {enabled}")
            except Exception as e:
                print(f"  ❌ {selector}: {e}")
        
        # 使用XPath查找包含特定文本的按钮
        print("\n📝 查找包含特定文本的按钮:")
        text_buttons = uploader.driver.find_elements("xpath", "//button[contains(text(), '立即投稿') or contains(text(), '发布') or contains(text(), '提交') or contains(text(), '投稿')]")
        if text_buttons:
            print(f"  ✅ 找到 {len(text_buttons)} 个包含投稿相关文本的按钮:")
            for btn in text_buttons:
                text = btn.text.strip()
                visible = btn.is_displayed()
                enabled = btn.is_enabled()
                print(f"    - '{text}' | 可见: {visible} | 可用: {enabled}")
        else:
            print("  ❌ 没有找到包含投稿相关文本的按钮")
        
        # 截图保存
        screenshot_path = os.path.join("logs", "screenshots", f"buttons_check_{int(time.time())}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        uploader.driver.save_screenshot(screenshot_path)
        print(f"\n📸 页面截图已保存: {screenshot_path}")
        
        print("\n⏸️ 浏览器将保持打开10秒供检查...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 检测失败: {e}")
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
