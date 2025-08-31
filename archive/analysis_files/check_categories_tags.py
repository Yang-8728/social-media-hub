#!/usr/bin/env python3
"""
检查B站上传页面的分区和标签选项
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader

def main():
    print("=== B站分区和标签选项检查 ===")
    
    try:
        uploader = BilibiliUploader("ai_vanvan")
        uploader._init_browser()
        
        # 访问上传页面
        print("📤 访问B站上传页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup")
        time.sleep(5)
        
        print("\n🏷️ 检查分区选项...")
        
        # 查找分区选择器
        try:
            # 寻找分区相关的元素
            category_selectors = [
                "[class*='category']", 
                "[class*='分区']",
                "select[name*='category']",
                ".select-category",
                "[data-v*] select",
                "select"
            ]
            
            print("查找分区选择器...")
            for selector in category_selectors:
                try:
                    elements = uploader.driver.find_elements("css selector", selector)
                    if elements:
                        print(f"✅ 找到分区相关元素: {selector} ({len(elements)}个)")
                        
                        for i, elem in enumerate(elements):
                            if elem.is_displayed():
                                # 尝试获取选项
                                try:
                                    options = elem.find_elements("tag name", "option")
                                    if options:
                                        print(f"  分区选项 ({len(options)}个):")
                                        for opt in options:
                                            text = opt.text.strip()
                                            value = opt.get_attribute("value")
                                            if text:
                                                print(f"    - {text} (value: {value})")
                                except:
                                    pass
                except Exception as e:
                    continue
        except Exception as e:
            print(f"分区检查失败: {e}")
        
        print("\n🏷️ 检查标签相关选项...")
        
        # 查找标签输入框和推荐标签
        try:
            # 查找标签输入框
            tag_selectors = [
                "input[placeholder*='标签']",
                "input[placeholder*='tag']",
                "[class*='tag']",
                ".tag-input"
            ]
            
            for selector in tag_selectors:
                try:
                    elements = uploader.driver.find_elements("css selector", selector)
                    if elements:
                        print(f"✅ 找到标签输入框: {selector}")
                        for elem in elements:
                            placeholder = elem.get_attribute("placeholder")
                            if placeholder:
                                print(f"  占位符: {placeholder}")
                except:
                    continue
            
            # 查找推荐标签
            print("\n🔍 查找推荐标签...")
            tag_suggestion_selectors = [
                "[class*='recommend']",
                "[class*='suggest']",
                "[class*='hot']",
                ".tag-list",
                "[data-v*=''] .tag",
                "span[class*='tag']"
            ]
            
            for selector in tag_suggestion_selectors:
                try:
                    elements = uploader.driver.find_elements("css selector", selector)
                    if elements:
                        print(f"✅ 找到推荐标签区域: {selector} ({len(elements)}个)")
                        
                        for elem in elements[:10]:  # 只显示前10个
                            text = elem.text.strip()
                            if text and len(text) < 20:  # 过滤掉太长的文本
                                print(f"  推荐标签: {text}")
                except:
                    continue
                    
        except Exception as e:
            print(f"标签检查失败: {e}")
        
        print("\n📝 检查页面源码中的分区信息...")
        
        # 在页面源码中查找分区相关信息
        try:
            page_source = uploader.driver.page_source
            
            # 查找常见的B站分区
            common_categories = [
                "生活", "游戏", "知识", "科技", "运动", "汽车", "时尚", "娱乐",
                "影视", "动画", "音乐", "舞蹈", "美食", "动物圈", "鬼畜",
                "时政", "科学科普", "数码", "手工", "绘画", "摄影"
            ]
            
            found_categories = []
            for category in common_categories:
                if category in page_source:
                    found_categories.append(category)
            
            if found_categories:
                print("📊 页面中发现的分区关键词:")
                for cat in found_categories:
                    print(f"  - {cat}")
                    
        except Exception as e:
            print(f"源码检查失败: {e}")
        
        # 截图保存
        screenshot_path = os.path.join("logs", "screenshots", f"categories_tags_{int(time.time())}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        uploader.driver.save_screenshot(screenshot_path)
        print(f"\n📸 页面截图已保存: {screenshot_path}")
        
        print("\n⏸️ 浏览器将保持打开20秒，请手动查看分区和标签选项...")
        time.sleep(20)
        
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
