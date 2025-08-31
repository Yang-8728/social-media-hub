"""
测试带配置文件的Chrome启动
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def test_chrome_with_profile():
    """测试使用配置文件的Chrome启动"""
    try:
        print("开始测试带配置文件的Chrome...")
        
        # Chrome配置
        chrome_options = Options()
        
        # 基本选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 配置文件路径
        profile_path = r"c:\Code\social-media-hub\tools\profiles\chrome_profile_ai_vanvan"
        
        # 验证配置文件存在
        if not os.path.exists(profile_path):
            print(f"❌ Chrome配置文件不存在: {profile_path}")
            return False
            
        print(f"✅ Chrome配置文件验证通过: {profile_path}")
        
        # 添加配置文件选项
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        
        # Chrome工具路径
        chrome_binary = r"c:\Code\social-media-hub\tools\chrome\chrome.exe"
        chromedriver_path = r"c:\Code\social-media-hub\tools\chrome\chromedriver.exe"
        
        # 设置Chrome二进制路径
        chrome_options.binary_location = chrome_binary
        
        # 创建Chrome服务
        service = Service(chromedriver_path)
        
        print("🚀 正在启动带配置文件的Chrome...")
        
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome启动成功！")
        
        # 导航到B站
        print("🌐 正在导航到B站...")
        driver.get("https://www.bilibili.com")
        
        # 等待页面加载
        time.sleep(5)
        
        # 获取页面标题
        title = driver.title
        print(f"📄 页面标题: {title}")
        
        # 检查是否成功加载B站
        if "bilibili" in title.lower() or "哔哩哔哩" in title:
            print("✅ B站页面加载成功")
        else:
            print("⚠️ 页面标题异常，可能未正确加载")
        
        # 检查登录状态
        try:
            # 查找登录相关元素
            print("🔍 检查登录状态...")
            
            # 等待页面完全加载
            time.sleep(3)
            
            # 尝试查找用户头像或登录按钮
            page_source = driver.page_source
            
            if "登录" in page_source and "用户中心" not in page_source:
                print("❌ 未登录状态")
            elif "用户中心" in page_source or "个人中心" in page_source:
                print("✅ 已登录状态")
            else:
                print("⚠️ 登录状态不明确")
                
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
            
        # 保持浏览器开启10秒以便观察
        print("⏰ 保持浏览器开启10秒...")
        time.sleep(10)
        
        # 关闭浏览器
        driver.quit()
        print("✅ 测试完成，Chrome正常关闭")
        
        return True
        
    except Exception as e:
        print(f"❌ Chrome启动失败: {e}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    success = test_chrome_with_profile()
    if success:
        print("\n🎉 带配置文件的Chrome测试通过！")
    else:
        print("\n💥 带配置文件的Chrome测试失败！")
