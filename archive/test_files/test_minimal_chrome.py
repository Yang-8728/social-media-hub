"""
最简Chrome配置测试
使用最基本的WebDriver配置来测试Chrome启动
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def test_minimal_chrome():
    """使用最简配置测试Chrome启动"""
    try:
        print("开始测试最简Chrome配置...")
        
        # Chrome配置
        chrome_options = Options()
        
        # 只添加最基本的选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Chrome工具路径
        chrome_binary = r"c:\Code\social-media-hub\tools\chrome\chrome.exe"
        chromedriver_path = r"c:\Code\social-media-hub\tools\chrome\chromedriver.exe"
        
        # 验证Chrome工具存在
        if not os.path.exists(chrome_binary):
            print(f"❌ Chrome二进制文件不存在: {chrome_binary}")
            return False
            
        if not os.path.exists(chromedriver_path):
            print(f"❌ ChromeDriver不存在: {chromedriver_path}")
            return False
            
        print("✅ Chrome工具验证通过")
        
        # 设置Chrome二进制路径
        chrome_options.binary_location = chrome_binary
        
        # 创建Chrome服务
        service = Service(chromedriver_path)
        
        print("🚀 正在启动Chrome...")
        
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome启动成功！")
        
        # 导航到B站
        print("🌐 正在导航到B站...")
        driver.get("https://www.bilibili.com")
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取页面标题
        title = driver.title
        print(f"📄 页面标题: {title}")
        
        # 检查是否成功加载B站
        if "bilibili" in title.lower() or "哔哩哔哩" in title:
            print("✅ B站页面加载成功")
        else:
            print("⚠️ 页面标题异常，可能未正确加载")
            
        # 保持浏览器开启5秒
        print("⏰ 保持浏览器开启5秒...")
        time.sleep(5)
        
        # 关闭浏览器
        driver.quit()
        print("✅ 测试完成，Chrome正常关闭")
        
        return True
        
    except Exception as e:
        print(f"❌ Chrome启动失败: {e}")
        return False


if __name__ == "__main__":
    success = test_minimal_chrome()
    if success:
        print("\n🎉 最简Chrome配置测试通过！")
    else:
        print("\n💥 最简Chrome配置测试失败！")
