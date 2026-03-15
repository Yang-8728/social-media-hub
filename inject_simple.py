import sqlite3
import shutil

source_db = '/tmp/chrome_cookies.db'
target_db = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies'

print(" 从Chrome提取cookies...")
shutil.copy(source_db, '/tmp/temp.db')
c = sqlite3.connect('/tmp/temp.db')
c.text_factory = bytes
rows = c.execute("SELECT * FROM cookies WHERE host_key LIKE '%bilibili%'").fetchall()
source_cols = [x[1] for x in c.execute("PRAGMA table_info(cookies)").fetchall()]
c.close()

print(f"找到 {len(rows)} 个B站cookies")

print("注入到Profile...")
t = sqlite3.connect(target_db)
t.execute("DELETE FROM cookies WHERE host_key LIKE '%bilibili%'")
t.commit()

success = 0
for row in rows:
    cols = [scol if isinstance(scol, str) else scol.decode() for scol in source_cols]
    sql = f"INSERT OR REPLACE INTO cookies ({','.join(cols)}) VALUES ({','.join(['?' for _ in cols])})"
    try:
        t.execute(sql, row)
        success += 1
    except Exception as e:
        print(f"错误: {e}")
        break

t.commit()
t.close()
print(f"成功: {success}/{len(rows)}")

# 验证
v = sqlite3.connect(target_db)
count = v.execute("SELECT COUNT(*) FROM cookies WHERE host_key LIKE '%bilibili%'").fetchone()[0]
sessdata = v.execute("SELECT COUNT(*) FROM cookies WHERE name='SESSDATA' AND host_key LIKE '%bilibili%'").fetchone()[0]
v.close()
print(f"验证: {count} 个cookies, {sessdata} 个SESSDATA")
