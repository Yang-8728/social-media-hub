"""测试Cookie加载后的实际状态"""
import sqlite3
import shutil
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_cookie_authentication():
    # 1. 设置Chrome选项（无头模式）
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    
    # 设置User-Agent（模拟正常浏览器）
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    
    # 使用临时profile
    temp_profile = f"/tmp/test_chrome_profile"
    chrome_options.add_argument(f'--user-data-dir={temp_profile}')
    
    # 2. 启动Chrome
    print("🚀 启动Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 3. 加载Cookies
        print("\n📂 读取Cookie数据库...")
        cookies_db = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies'
        temp_cookies = '/tmp/temp_cookies.db'
        shutil.copy(cookies_db, temp_cookies)
        
        conn = sqlite3.connect(temp_cookies)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
            FROM cookies WHERE host_key LIKE '%bilibili.com%'
        """)
        
        # 4. 先访问bilibili.com
        print("🌐 访问 bilibili.com...")
        driver.get("https://www.bilibili.com")
        time.sleep(2)
        
        # 5. 添加Cookies
        print("\n🍪 添加Cookies...")
        for row in cursor.fetchall():
            host, name, value, path, expires, is_secure, is_httponly = row
            cookie_dict = {
                'name': name,
                'value': value,
                'path': path,
                'domain': host if host.startswith('.') else f".{host}",
                'secure': bool(is_secure),
                'httpOnly': bool(is_httponly)
            }
            if expires > 0:
                cookie_dict['expiry'] = int(expires / 1000000 - 11644473600)
            
            try:
                driver.add_cookie(cookie_dict)
                if name in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                    print(f"  ✅ {name}: {value[:20]}...")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
        
        conn.close()
        os.remove(temp_cookies)
        
        # 6. 验证Cookie是否成功添加到浏览器
        print("\n🔍 验证浏览器中的Cookies:")
        browser_cookies = driver.get_cookies()
        important_found = []
        for cookie in browser_cookies:
            if cookie['name'] in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                important_found.append(cookie['name'])
                print(f"  ✅ {cookie['name']}: {cookie['value'][:20]}... (domain: {cookie['domain']})")
        
        if len(important_found) < 3:
            print(f"  ⚠️ 警告：只找到 {len(important_found)}/3 个关键Cookie!")
        
        # 7. 刷新页面
        print("\n🔄 刷新页面...")
        driver.refresh()
        time.sleep(2)
        
        # 8. 检查刷新后的Cookies是否还在
        print("\n🔍 刷新后的Cookies:")
        browser_cookies_after = driver.get_cookies()
        important_after = []
        for cookie in browser_cookies_after:
            if cookie['name'] in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                important_after.append(cookie['name'])
        print(f"  关键Cookie: {len(important_after)}/3")
        
        # 9. 直接访问上传页面
        print("\n🎯 访问上传页面...")
        driver.get("https://member.bilibili.com/platform/upload/video/frame")
        time.sleep(3)
        
        # 10. 检查最终URL
        final_url = driver.current_url
        print(f"\n📍 最终URL: {final_url}")
        
        if "login" in final_url or "passport" in final_url:
            print("❌ 跳转到登录页面！认证失败！")
        else:
            print("✅ 成功停留在上传页面！认证成功！")
        
        # 11. 检查页面内容
        print("\n📄 页面标题:", driver.title)
        
        # 12. 截取最终Cookie状态
        print("\n🍪 最终浏览器Cookies:")
        final_cookies = driver.get_cookies()
        for cookie in final_cookies:
            if cookie['name'] in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                print(f"  {cookie['name']}: domain={cookie['domain']}, secure={cookie.get('secure')}")
        
    finally:
        print("\n🛑 关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    test_cookie_authentication()
