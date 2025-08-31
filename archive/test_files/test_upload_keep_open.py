#!/usr/bin/env python3
"""
B站上传测试 - 点击立即投稿后保持浏览器打开
"""
import os
import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata

def main():
    print("=== B站上传测试 - 完整流程 ===")
    
    # 使用真实的合并视频文件
    test_video = r"c:\Code\social-media-hub\videos\merged\ai_vanvan\ai_vanvan_2025-08-29_10-18-52_merged_10videos.mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ 视频文件不存在: {test_video}")
        return
    
    # 获取文件大小
    file_size = os.path.getsize(test_video) / (1024 * 1024)
    print(f"📹 选择视频: {os.path.basename(test_video)}")
    print(f"📊 文件大小: {file_size:.1f} MB")
    
    # 创建视频元数据
    metadata = VideoMetadata(
        title="AI助手自动合集测试 2025-08-29",
        description="这是AI助手自动下载并合并的10个视频的合集，包含最新的内容更新。\n\n自动化工具生成，完整上传流程测试。",
        tags=["AI助手", "自动化", "视频合集", "完整测试"],
        category="科技"
    )
    
    print(f"📋 视频信息:")
    print(f"  标题: {metadata.title}")
    print(f"  描述: {metadata.description[:50]}...")
    print(f"  标签: {', '.join(metadata.tags)}")
    
    # 初始化上传器
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print("✅ 上传器初始化成功")
    except Exception as e:
        print(f"❌ 上传器初始化失败: {e}")
        return
    
    # 开始上传流程
    print("\n🚀 开始完整上传流程...")
    try:
        # 初始化浏览器
        uploader._init_browser()
        print("✅ 浏览器启动成功")
        
        # 导航到上传页面
        print("📤 访问上传页面...")
        uploader.driver.get("https://member.bilibili.com/york/videoup")
        time.sleep(5)
        
        # 检查是否成功到达上传页面
        current_url = uploader.driver.current_url
        if "videoup" not in current_url:
            print(f"❌ 无法访问上传页面，当前URL: {current_url}")
            return
        print("✅ 成功访问上传页面")
        
        # 查找文件上传区域
        print("🔍 寻找文件上传区域...")
        upload_input = None
        upload_selectors = [
            "input[type='file']",
            "[class*='upload']",
            "[class*='file']",
            ".upload-box",
            "#upload-box"
        ]
        
        for selector in upload_selectors:
            try:
                elements = uploader.driver.find_elements("css selector", selector)
                for element in elements:
                    if element.is_displayed() or element.get_attribute("type") == "file":
                        upload_input = element
                        print(f"✅ 找到上传元素: {selector}")
                        break
                if upload_input:
                    break
            except:
                continue
        
        if not upload_input:
            print("❌ 未找到文件上传控件")
            return
        
        # 上传文件
        print("📁 开始上传文件...")
        upload_input.send_keys(os.path.abspath(test_video))
        print("✅ 文件已选择")
        
        # 等待文件上传
        print("⏳ 等待文件上传...")
        time.sleep(10)
        
        # 填写视频信息
        print("📝 填写视频信息...")
        
        # 填写标题
        try:
            title_input = uploader.driver.find_element("css selector", "input[placeholder*='标题'], input[placeholder*='title']")
            title_input.clear()
            title_input.send_keys(metadata.title)
            print(f"✅ 已填写标题: {metadata.title}")
        except Exception as e:
            print(f"⚠️ 标题填写失败: {e}")
        
        # 填写描述
        try:
            desc_selectors = ["textarea[placeholder*='描述']", "textarea[placeholder*='简介']", ".ql-editor"]
            for selector in desc_selectors:
                try:
                    desc_element = uploader.driver.find_element("css selector", selector)
                    desc_element.clear()
                    desc_element.send_keys(metadata.description)
                    print("✅ 已填写描述")
                    break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ 描述填写失败: {e}")
        
        # 填写标签
        try:
            tag_text = ", ".join(metadata.tags)
            tag_selectors = ["input[placeholder*='标签']", "input[placeholder*='tag']"]
            for selector in tag_selectors:
                try:
                    tag_input = uploader.driver.find_element("css selector", selector)
                    tag_input.clear()
                    tag_input.send_keys(tag_text)
                    print(f"✅ 已填写标签: {tag_text}")
                    break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ 标签填写失败: {e}")
        
        # 等待页面更新
        print("⏳ 等待视频处理...")
        time.sleep(5)
        
        # 查找并点击发布按钮
        print("🔍 寻找立即投稿按钮...")
        
        # 先用XPath查找包含文本的按钮
        publish_button = None
        text_buttons = uploader.driver.find_elements("xpath", "//button[contains(text(), '立即投稿') or contains(text(), '发布') or contains(text(), '提交')]")
        if text_buttons:
            publish_button = text_buttons[0]
            print(f"✅ 找到投稿按钮(文本匹配): '{publish_button.text.strip()}'")
        else:
            # 备用选择器
            publish_selectors = [
                "button[class*='submit']",
                "button[class*='publish']", 
                "button[class*='upload']",
                ".btn-publish",
                ".submit-btn"
            ]
            
            for selector in publish_selectors:
                try:
                    elements = uploader.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            publish_button = element
                            print(f"✅ 找到发布按钮: {selector}")
                            break
                    if publish_button:
                        break
                except:
                    continue
        
        if publish_button:
            try:
                print("🚀 即将点击立即投稿按钮...")
                print(f"按钮文本: '{publish_button.text.strip()}'")
                print(f"按钮可见: {publish_button.is_displayed()}")
                print(f"按钮可用: {publish_button.is_enabled()}")
                
                # 滚动到按钮位置
                uploader.driver.execute_script("arguments[0].scrollIntoView();", publish_button)
                time.sleep(1)
                
                # 点击按钮
                publish_button.click()
                print("✅ 已点击立即投稿按钮!")
                
                # 等待页面响应
                time.sleep(5)
                
                # 检查是否跳转到成功页面
                current_url = uploader.driver.current_url
                print(f"📍 点击后的URL: {current_url}")
                
                if "manage" in current_url or "success" in current_url:
                    print("🎉 看起来投稿成功了!")
                else:
                    print("❓ 页面未跳转，检查是否有错误提示")
                
            except Exception as e:
                print(f"❌ 点击投稿按钮失败: {e}")
        else:
            print("❌ 未找到立即投稿按钮")
        
        # 保持浏览器打开
        print("\n🖥️ 浏览器将保持打开，请手动检查结果...")
        print("可以检查:")
        print("1. 投稿是否成功")
        print("2. 视频是否在处理中")
        print("3. 是否有错误提示")
        print("\n按 Ctrl+C 退出并关闭浏览器")
        
        try:
            while True:
                time.sleep(10)
                print("⏳ 浏览器保持打开中... (Ctrl+C 退出)")
        except KeyboardInterrupt:
            print("\n✅ 用户退出")
            
    except Exception as e:
        print(f"❌ 上传过程异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理浏览器
        try:
            if hasattr(uploader, 'driver') and uploader.driver:
                uploader.driver.quit()
                print("🧹 浏览器已关闭")
        except:
            pass

if __name__ == "__main__":
    main()
