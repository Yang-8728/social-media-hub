"""
测试配置文件修复方案
"""
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def create_clean_profile():
    """创建一个干净的Chrome配置文件目录"""
    clean_profile = r"c:\Code\social-media-hub\tools\profiles\chrome_profile_clean"
    
    # 删除现有目录
    if os.path.exists(clean_profile):
        shutil.rmtree(clean_profile)
    
    # 创建新目录
    os.makedirs(clean_profile, exist_ok=True)
    print(f"✅ 创建干净配置目录: {clean_profile}")
    
    return clean_profile


def test_clean_profile():
    """测试干净的配置文件"""
    try:
        print("🧹 创建干净的Chrome配置文件...")
        clean_profile = create_clean_profile()
        
        # Chrome配置
        chrome_options = Options()
        chrome_options.binary_location = r"c:\Code\social-media-hub\tools\chrome\chrome.exe"
        
        # 基本稳定性选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # 使用干净的配置目录
        chrome_options.add_argument(f"--user-data-dir={clean_profile}")
        
        # 创建服务
        service = Service(r"c:\Code\social-media-hub\tools\chrome\chromedriver.exe")
        
        print("🚀 启动Chrome with 干净配置...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome启动成功！")
        
        # 导航到B站
        print("🌐 导航到B站...")
        driver.get("https://www.bilibili.com")
        time.sleep(5)
        
        title = driver.title
        print(f"📄 页面标题: {title}")
        
        # 保持开启10秒
        print("⏰ 保持浏览器开启10秒...")
        time.sleep(10)
        
        driver.quit()
        print("✅ 测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def copy_essential_files():
    """只复制必要的登录文件"""
    try:
        print("📂 复制必要的登录文件...")
        
        source_profile = r"c:\Code\insDownloader\chrome_profile_ai_vanvan"
        clean_profile = r"c:\Code\social-media-hub\tools\profiles\chrome_profile_clean"
        
        # 确保目标目录存在
        os.makedirs(f"{clean_profile}\\Default\\Network", exist_ok=True)
        
        # 只复制关键的登录文件
        essential_files = [
            "Default\\Network\\Cookies",
            "Default\\Login Data",
            "Default\\Preferences",
            "Default\\Web Data",
            "Local State"
        ]
        
        for file_path in essential_files:
            source_file = os.path.join(source_profile, file_path)
            target_file = os.path.join(clean_profile, file_path)
            
            if os.path.exists(source_file):
                # 确保目标目录存在
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)
                print(f"✅ 复制: {file_path}")
            else:
                print(f"⚠️ 文件不存在: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 复制文件失败: {e}")
        return False


def test_minimal_profile():
    """测试最小化配置文件"""
    try:
        print("\n🔧 测试最小化配置文件...")
        
        clean_profile = r"c:\Code\social-media-hub\tools\profiles\chrome_profile_clean"
        
        # Chrome配置
        chrome_options = Options()
        chrome_options.binary_location = r"c:\Code\social-media-hub\tools\chrome\chrome.exe"
        
        # 基本选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        
        # 使用最小化配置目录
        chrome_options.add_argument(f"--user-data-dir={clean_profile}")
        
        service = Service(r"c:\Code\social-media-hub\tools\chrome\chromedriver.exe")
        
        print("🚀 启动Chrome with 最小化配置...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome启动成功！")
        
        # 导航到B站
        print("🌐 导航到B站...")
        driver.get("https://www.bilibili.com")
        time.sleep(5)
        
        title = driver.title
        print(f"📄 页面标题: {title}")
        
        # 检查登录状态
        page_source = driver.page_source
        if "登录" in page_source and "用户中心" not in page_source:
            print("❌ 未登录状态")
        elif "用户中心" in page_source or "个人中心" in page_source:
            print("✅ 已登录状态")
        else:
            print("⚠️ 登录状态不明确")
        
        # 保持开启10秒
        print("⏰ 保持浏览器开启10秒...")
        time.sleep(10)
        
        driver.quit()
        print("✅ 测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    print("开始配置文件修复测试...\n")
    
    # 测试1: 干净配置文件
    if test_clean_profile():
        print("\n🎉 干净配置文件测试通过")
        
        # 测试2: 复制必要文件
        if copy_essential_files():
            print("\n📂 必要文件复制完成")
            
            # 测试3: 最小化配置测试
            if test_minimal_profile():
                print("\n🎉 最小化配置测试通过！可能已保留登录状态")
            else:
                print("\n💥 最小化配置测试失败")
        else:
            print("\n💥 文件复制失败")
    else:
        print("\n💥 干净配置文件测试失败")
