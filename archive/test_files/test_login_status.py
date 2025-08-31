#!/usr/bin/env python3
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 设置路径
chrome_path = r'c:\Code\social-media-hub\tools\chrome\chrome.exe'
chromedriver_path = r'c:\Code\social-media-hub\tools\chrome\chromedriver.exe'
# 使用经过测试的干净配置文件路径
profile_path = r'c:\Code\social-media-hub\tools\profiles\chrome_profile_clean'

print(f'Chrome路径: {chrome_path}')
print(f'ChromeDriver路径: {chromedriver_path}')
print(f'配置文件路径: {profile_path}')

# 确保配置文件目录存在
if not os.path.exists(profile_path):
    print(f"创建Chrome配置目录: {profile_path}")
    os.makedirs(profile_path, exist_ok=True)

# 配置选项 - 使用经过测试的稳定配置
options = Options()
options.binary_location = chrome_path
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

# 用户目录配置
print(f"使用Chrome配置文件: {profile_path}")
options.add_argument(f'--user-data-dir={profile_path}')

# 窗口配置
options.add_argument('--window-size=960,1080')
options.add_argument('--window-position=200,100')

# 创建服务
service = Service(chromedriver_path)

# 测试启动
print('正在测试浏览器启动...')
try:
    driver = webdriver.Chrome(service=service, options=options)
    print('✅ 浏览器启动成功!')
    
    # 访问B站
    print('正在访问B站...')
    driver.get('https://www.bilibili.com')
    time.sleep(3)
    
    # 检查登录状态
    print('检查登录状态...')
    try:
        # 查找登录相关元素
        login_element = driver.find_element_by_class_name('header-login-entry')
        if login_element:
            print('❌ 未登录 - 显示登录按钮')
        else:
            print('✅ 可能已登录')
    except:
        print('✅ 可能已登录 - 未找到登录按钮')
    
    # 访问投稿页面测试
    print('正在访问投稿页面...')
    driver.get('https://member.bilibili.com/platform/upload/video/')
    time.sleep(5)
    
    current_url = driver.current_url
    page_title = driver.title
    
    print(f'当前URL: {current_url}')
    print(f'页面标题: {page_title}')
    
    if 'upload' in current_url:
        print('✅ 成功进入投稿页面，登录状态正常')
    elif 'login' in current_url or 'passport' in current_url:
        print('❌ 被重定向到登录页面，需要登录')
    else:
        print('⚠️  未知状态，请手动检查')
    
    input('按回车键关闭浏览器...')
    driver.quit()
    print('✅ 浏览器正常关闭')
    
except Exception as e:
    print(f'❌ 启动失败: {e}')
