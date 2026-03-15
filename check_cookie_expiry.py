import sqlite3
from datetime import datetime

cookies_db = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies'
conn = sqlite3.connect(cookies_db)
cursor = conn.cursor()

# 查询关键Cookie及过期时间
cursor.execute("""
    SELECT name, value, expires_utc, host_key 
    FROM cookies 
    WHERE host_key LIKE '%bilibili.com%' AND name IN ('SESSDATA', 'bili_jct', 'DedeUserID')
""")

print("关键Cookie过期时间检查:")
print("=" * 80)

for name, value, expires_utc, host in cursor.fetchall():
    # Chrome时间戳：微秒，从1601年1月1日开始
    # Unix时间戳：秒，从1970年1月1日开始
    # 转换公式：(chrome_time / 1000000) - 11644473600
    
    if expires_utc > 0:
        unix_timestamp = (expires_utc / 1000000) - 11644473600
        expire_date = datetime.fromtimestamp(unix_timestamp)
        now = datetime.now()
        
        is_expired = expire_date < now
        status = "❌ 已过期" if is_expired else "✅ 有效"
        
        print(f"{name:20} | {status}")
        print(f"  过期时间: {expire_date}")
        print(f"  当前时间: {now}")
        if not is_expired:
            remaining = expire_date - now
            print(f"  剩余时间: {remaining.days}天")
        print()
    else:
        print(f"{name:20} | ⚠️  Session Cookie (浏览器关闭即失效)")
        print()

conn.close()
