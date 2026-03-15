import sqlite3, shutil, os
chrome = r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies'
target = r'tools\profiles\chrome_profile_ai_vanvan_fresh\Default\Network\Cookies'
shutil.copy(chrome, 'tc.db')
c = sqlite3.connect('tc.db')
c.text_factory = bytes
rows = c.execute("SELECT * FROM cookies WHERE host_key LIKE '%bilibili%'").fetchall()
source_cols = [x[1] for x in c.execute("PRAGMA table_info(cookies)").fetchall()]
c.close()
t = sqlite3.connect(target)
t.execute("DELETE FROM cookies WHERE host_key LIKE '%bilibili%'")
target_cols = [x[1] for x in t.execute("PRAGMA table_info(cookies)").fetchall()]
success = 0
for idx, row in enumerate(rows):
    insert_cols = [scol if isinstance(scol, str) else scol.decode() for scol in source_cols]
    sql = f"INSERT INTO cookies ({','.join(insert_cols)}) VALUES ({','.join(['?' for _ in insert_cols])})"
    try:
        t.execute(sql, row)
        success += 1
    except Exception as e:
        print(f"错误: {e}")
        break
t.commit()
t.close()
os.remove('tc.db')
print(f"成功注入 {success}/{len(rows)} 个Cookie")
