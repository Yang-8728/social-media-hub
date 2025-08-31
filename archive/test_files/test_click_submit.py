#!/usr/bin/env python3
"""
专门测试点击立即投稿按钮
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== 测试点击立即投稿按钮 ===")
    
    try:
        uploader = BilibiliUploader("ai_vanvan")
        uploader._init_browser()
        
        # 直接访问当前的上传页面(假设你已经在上传页面)
        print("📤 访问上传页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup")
        time.sleep(5)
        
        print("🔍 查找所有按钮...")
        all_buttons = uploader.driver.find_elements("tag name", "button")
        print(f"找到 {len(all_buttons)} 个按钮:")
        
        target_button = None
        for i, btn in enumerate(all_buttons):
            try:
                text = btn.text.strip()
                classes = btn.get_attribute("class") or ""
                visible = btn.is_displayed()
                enabled = btn.is_enabled()
                
                print(f"  按钮 {i+1}: '{text}' | 可见:{visible} | 可用:{enabled}")
                
                # 查找立即投稿按钮
                if "立即投稿" in text and visible and enabled:
                    target_button = btn
                    print(f"  ✅ 找到目标按钮: '{text}'")
                    
            except Exception as e:
                print(f"  ❌ 按钮 {i+1} 检查失败: {e}")
        
        if target_button:
            print(f"\n🎯 准备点击立即投稿按钮...")
            try:
                # 滚动到按钮位置
                uploader.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_button)
                time.sleep(2)
                
                print("📍 按钮位置信息:")
                location = target_button.location
                size = target_button.size
                print(f"  位置: x={location['x']}, y={location['y']}")
                print(f"  尺寸: width={size['width']}, height={size['height']}")
                
                # 高亮按钮
                uploader.driver.execute_script("arguments[0].style.border='3px solid red';", target_button)
                time.sleep(1)
                
                print("🚀 点击按钮...")
                target_button.click()
                print("✅ 按钮已点击!")
                
                # 等待页面响应
                time.sleep(5)
                
                # 检查页面变化
                current_url = uploader.driver.current_url
                page_title = uploader.driver.title
                print(f"📍 当前URL: {current_url}")
                print(f"📄 页面标题: {page_title}")
                
                if "manage" in current_url:
                    print("🎉 跳转到管理页面，投稿可能成功!")
                elif "success" in current_url:
                    print("🎉 显示成功页面!")
                else:
                    print("❓ 页面未明显变化，检查是否有其他反馈")
                
            except Exception as e:
                print(f"❌ 点击失败: {e}")
                # 尝试JavaScript点击
                try:
                    print("🔄 尝试JavaScript点击...")
                    uploader.driver.execute_script("arguments[0].click();", target_button)
                    print("✅ JavaScript点击完成!")
                    time.sleep(3)
                except Exception as js_e:
                    print(f"❌ JavaScript点击也失败: {js_e}")
        else:
            print("❌ 没有找到立即投稿按钮")
            
            # 尝试其他可能的投稿按钮
            print("\n🔍 寻找其他可能的投稿按钮...")
            for btn in all_buttons:
                try:
                    text = btn.text.strip()
                    if ("投稿" in text or "发布" in text or "提交" in text) and btn.is_displayed() and btn.is_enabled():
                        print(f"  可能的按钮: '{text}'")
                        target_button = btn
                        break
                except:
                    continue
            
            if target_button:
                print(f"🔄 尝试点击: '{target_button.text.strip()}'")
                try:
                    target_button.click()
                    print("✅ 备用按钮点击成功!")
                except Exception as e:
                    print(f"❌ 备用按钮点击失败: {e}")
        
        # 保持浏览器打开
        print("\n🖥️ 浏览器保持打开，请检查结果...")
        print("按 Ctrl+C 退出")
        
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n✅ 退出")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
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
