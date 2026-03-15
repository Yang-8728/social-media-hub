import sqlite3
from datetime import datetime

db = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies'
c = sqlite3.connect(db)
c.text_factory = bytes

# 检查SESSDATA的过期时间
rows = c.execute("SELECT name, host_key, expires_utc FROM cookies WHERE name='SESSDATA'").fetchall()

print("SESSDATA Cookies:")
for r in rows:
    name = r[0].decode() if isinstance(r[0], bytes) else r[0]
    host = r[1].decode() if isinstance(r[1], bytes) else r[1]
    # Chrome的expires_utc是从1601年1月1日开始的微秒数
    expires_timestamp = r[2] / 1000000 - 11644473600  # 转换为Unix时间戳
    expires_date = datetime.fromtimestamp(expires_timestamp)
    now = datetime.now()
    
    if expires_date > now:
        status = " 有效"
        days_left = (expires_date - now).days
        print(f"{name} @ {host}: {status} (还有 {days_left} 天)")
    else:
        status = " 已过期"
        print(f"{name} @ {host}: {status}")
        
c.close()
