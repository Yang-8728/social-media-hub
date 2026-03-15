import sqlite3
from datetime import datetime

# 分析 Chrome 的 Cookies
chrome_cookies = r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies'
temp_db = 'temp_check_chrome.db'

import os
import shutil

# 复制
os.system(f'copy /Y "{chrome_cookies}" "{temp_db}" >nul 2>&1')

if os.path.exists(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    
    # 查询 SESSDATA
    cursor.execute("""
        SELECT name, value, host_key, expires_utc
        FROM cookies
        WHERE name = 'SESSDATA' AND host_key LIKE '%bilibili%'
    """)
    
    cookies = cursor.fetchall()
    conn.close()
    
    for cookie in cookies:
        name, value, host, expires_utc = cookie
        # Chrome 时间戳是微秚，从 1601-01-01 开始
        # 转换为 Unix 时间戳（秒）
        unix_timestamp = (expires_utc / 1000000) - 11644473600
        expire_time = datetime.fromtimestamp(unix_timestamp)
        
        print(f"Cookie: {name} @ {host}")
        print(f"Value: {value[:50]}...")
        print(f"过期时间: {expire_time}")
        print(f"当前时间: {datetime.now()}")
        
        if expire_time > datetime.now():
            print("✅ 未过期")
        else:
            print("❌ 已过期!")
    
    os.remove(temp_db)
else:
    print("❌ 无法复制 Chrome Cookies")
