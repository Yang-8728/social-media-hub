import sqlite3
c = sqlite3.connect('/tmp/source_cookies.db')
rows = c.execute("SELECT name, host_key FROM cookies WHERE name='SESSDATA'").fetchall()
print(f'找到 {len(rows)} 个 SESSDATA:')
for r in rows:
    print(f'  {r[0]} @ {r[1]}')
c.close()
