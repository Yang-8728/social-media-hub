import sqlite3

cookies_db = r'tools\profiles\chrome_profile_ai_vanvan_fresh\Default\Network\Cookies'

try:
    conn = sqlite3.connect(cookies_db)
    cursor = conn.cursor()
    
    # 查找所有 Cookie
    cursor.execute("SELECT name, value, host_key FROM cookies WHERE host_key LIKE '%bilibili%'")
    cookies = cursor.fetchall()
    
    print(f"本地 Profile 中找到 {len(cookies)} 个 B站 Cookie:")
    has_sessdata = False
    for name, value, host in cookies:
        if name == 'SESSDATA':
            print(f"  🔑 {name}: {value[:30]}... @ {host}")
            has_sessdata = True
        elif name in ['bili_jct', 'DedeUserID']:
            print(f"  🔑 {name}: {value[:20]}... @ {host}")
        else:
            print(f"  • {name} @ {host}")
    
    print(f"\n{'✅' if has_sessdata else '❌'} SESSDATA: {'存在' if has_sessdata else '不存在'}")
    
    conn.close()
except Exception as e:
    print(f"错误: {e}")
