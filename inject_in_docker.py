import sqlite3
import shutil
import os

# 源：你的Chrome Cookies
source_db = '/tmp/chrome_cookies.db'
# 目标：容器内的Profile Cookies
target_db = '/app/chrome/profiles/chrome_profile_ai_vanvan/Default/Network/Cookies'

print(" 步骤1: 从Chrome提取B站cookies...")
# 复制一份源数据库（避免锁定）
shutil.copy(source_db, '/tmp/temp_chrome.db')
c = sqlite3.connect('/tmp/temp_chrome.db')
c.text_factory = bytes

# 提取所有B站cookies
rows = c.execute("SELECT * FROM cookies WHERE host_key LIKE '%bilibili%'").fetchall()
source_cols = [x[1] for x in c.execute("PRAGMA table_info(cookies)").fetchall()]
c.close()

print(f"   找到 {len(rows)} 个B站cookies")

# 显示SESSDATA
sessdata_count = sum(1 for r in rows if b'SESSDATA' in r)
print(f"   其中 {sessdata_count} 个是SESSDATA")

print("\n  步骤2: 清空目标数据库的B站cookies...")
t = sqlite3.connect(target_db)
deleted = t.execute("DELETE FROM cookies WHERE host_key LIKE '%bilibili%'").rowcount
t.commit()
print(f"   删除了 {deleted} 个旧cookies")

print("\n 步骤3: 注入新cookies...")
success = 0
failed = 0
for idx, row in enumerate(rows):
    insert_cols = [scol if isinstance(scol, str) else scol.decode() for scol in source_cols]
    sql = f"INSERT INTO cookies ({','.join(insert_cols)}) VALUES ({','.join(['?' for _ in insert_cols])})"
    try:
        t.execute(sql, row)
        success += 1
    except Exception as e:
        failed += 1
        if failed <= 3:
            print(f"     跳过第 {idx+1} 个: {e}")

t.commit()
t.close()
os.remove('/tmp/temp_chrome.db')

print(f"\n 完成！成功注入 {success}/{len(rows)} 个cookies")
if failed > 0:
    print(f"  失败 {failed} 个")

# 验证
print("\n 验证注入结果...")
v = sqlite3.connect(target_db)
v.text_factory = bytes
verify_rows = v.execute("SELECT name, host_key FROM cookies WHERE host_key LIKE '%bilibili%' ORDER BY host_key").fetchall()
print(f"目标数据库现在有 {len(verify_rows)} 个B站cookies:")

domains = {}
for r in verify_rows:
    domain = r[1].decode() if isinstance(r[1], bytes) else r[1]
    if domain not in domains:
        domains[domain] = []
    name = r[0].decode() if isinstance(r[0], bytes) else r[0]
    domains[domain].append(name)

for domain in sorted(domains.keys()):
    has_sessdata = 'SESSDATA' in domains[domain]
    marker = '' if has_sessdata else '  '
    print(f"{marker} {domain}: {len(domains[domain])} cookies", end='')
    if has_sessdata:
        print(" (含SESSDATA)")
    else:
        print()

v.close()
