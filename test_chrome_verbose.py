#!/usr/bin/env python3
"""启用详细日志测试 Chrome"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_with_verbose_logging():
    """启用 ChromeDriver 详细日志"""
    print("启动 Chrome 并查看详细日志...")
    
    service = Service(log_output='/tmp/chromedriver.log')
    service.service_args = ['--verbose', '--log-path=/tmp/chromedriver.log']
    
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--user-data-dir=/tmp/test_profile')
    opts.add_argument('--enable-logging')
    opts.add_argument('--v=1')
    
    try:
        driver = webdriver.Chrome(service=service, options=opts)
        print('✅ Chrome启动成功')
        driver.quit()
    except Exception as e:
        print(f'❌ 失败: {e}')
        print("\n=== ChromeDriver 日志 ===")
        try:
            with open('/tmp/chromedriver.log', 'r') as f:
                print(f.read())
        except:
            print("无法读取日志文件")

if __name__ == '__main__':
    test_with_verbose_logging()
