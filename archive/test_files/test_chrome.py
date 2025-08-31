#!/usr/bin/env python3
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 设置路径
chrome_path = r'c:\Code\social-media-hub\tools\chrome\chrome.exe'
chromedriver_path = r'c:\Code\social-media-hub\tools\chrome\chromedriver.exe'

print(f'Chrome路径: {chrome_path}')
print(f'ChromeDriver路径: {chromedriver_path}')
print(f'Chrome存在: {os.path.exists(chrome_path)}')
print(f'ChromeDriver存在: {os.path.exists(chromedriver_path)}')

# 配置选项
options = Options()
options.binary_location = chrome_path
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# 创建服务
service = Service(chromedriver_path)

# 测试启动
print('正在测试浏览器启动...')
try:
    driver = webdriver.Chrome(service=service, options=options)
    print('✅ 浏览器启动成功!')
    driver.get('https://www.bilibili.com')
    print(f'页面标题: {driver.title}')
    input('按回车键关闭浏览器...')
    driver.quit()
    print('✅ 浏览器正常关闭')
except Exception as e:
    print(f'❌ 启动失败: {e}')
