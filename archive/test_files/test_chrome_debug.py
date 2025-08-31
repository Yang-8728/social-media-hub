"""
极简Chrome配置测试 - 逐步添加选项
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def test_chrome_step_by_step():
    """逐步添加Chrome选项，找出导致崩溃的原因"""
    
    # Chrome工具路径
    chrome_binary = r"c:\Code\social-media-hub\tools\chrome\chrome.exe"
    chromedriver_path = r"c:\Code\social-media-hub\tools\chrome\chromedriver.exe"
    
    # 测试1: 最基本配置
    print("🔧 测试1: 最基本配置（无额外选项）")
    try:
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ 基本配置成功")
        driver.quit()
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ 基本配置失败: {e}")
        return False
    
    # 测试2: 添加基本稳定性选项
    print("\n🔧 测试2: 添加基本稳定性选项")
    try:
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ 基本稳定性选项成功")
        driver.quit()
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ 基本稳定性选项失败: {e}")
        return False
    
    # 测试3: 添加更多稳定性选项
    print("\n🔧 测试3: 添加更多稳定性选项")
    try:
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ 更多稳定性选项成功")
        driver.quit()
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ 更多稳定性选项失败: {e}")
        return False
    
    # 测试4: 测试临时目录
    print("\n🔧 测试4: 使用临时配置目录")
    try:
        temp_profile = r"c:\Code\social-media-hub\temp\test_profile"
        os.makedirs(temp_profile, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--user-data-dir={temp_profile}")
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ 临时配置目录成功")
        driver.quit()
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ 临时配置目录失败: {e}")
        return False
    
    # 测试5: 测试实际配置文件
    print("\n🔧 测试5: 使用实际ai_vanvan配置文件")
    try:
        profile_path = r"c:\Code\social-media-hub\tools\profiles\chrome_profile_ai_vanvan"
        
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ 实际配置文件成功")
        
        # 简单测试导航
        driver.get("https://www.bilibili.com")
        time.sleep(3)
        print(f"📄 页面标题: {driver.title}")
        
        driver.quit()
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"❌ 实际配置文件失败: {e}")
        return False


if __name__ == "__main__":
    print("开始逐步Chrome配置测试...\n")
    success = test_chrome_step_by_step()
    
    if success:
        print("\n🎉 所有测试通过！Chrome配置正常")
    else:
        print("\n💥 测试失败，需要进一步调试")
