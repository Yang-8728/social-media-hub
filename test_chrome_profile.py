#!/usr/bin/env python3
"""测试 Chrome 配置文件兼容性"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_chrome_with_temp_profile():
    """测试使用临时复制的配置文件"""
    print("测试1: 使用临时配置文件...")
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--user-data-dir=/tmp/test_profile')
    
    try:
        driver = webdriver.Chrome(options=opts)
        print('✅ Chrome启动成功（临时配置）')
        driver.quit()
        return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        return False

def test_chrome_with_remote_debugging():
    """测试使用 remote-debugging-port"""
    print("\n测试2: 使用 remote-debugging-port...")
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--user-data-dir=/app/chrome/profiles/chrome_profile_ai_vanvan')
    opts.add_argument('--remote-debugging-port=9222')
    
    try:
        driver = webdriver.Chrome(options=opts)
        print('✅ Chrome启动成功（remote debugging）')
        driver.quit()
        return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        return False

def test_chrome_with_disable_features():
    """测试禁用某些特性"""
    print("\n测试3: 禁用可能导致冲突的特性...")
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--user-data-dir=/app/chrome/profiles/chrome_profile_ai_vanvan')
    opts.add_argument('--disable-features=VizDisplayCompositor')
    opts.add_argument('--disable-software-rasterizer')
    
    try:
        driver = webdriver.Chrome(options=opts)
        print('✅ Chrome启动成功（禁用特性）')
        driver.quit()
        return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Chrome 配置文件兼容性测试")
    print("=" * 60)
    
    results = []
    results.append(("临时配置", test_chrome_with_temp_profile()))
    results.append(("Remote Debugging", test_chrome_with_remote_debugging()))
    results.append(("禁用特性", test_chrome_with_disable_features()))
    
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print("=" * 60)
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{name}: {status}")
