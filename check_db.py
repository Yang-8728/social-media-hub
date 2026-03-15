import sqlite3
c = sqlite3.connect('/tmp/source_cookies.db')
total = c.execute("SELECT COUNT(*) FROM cookies").fetchone()[0]
bili = c.execute("SELECT COUNT(*) FROM cookies WHERE host_key LIKE '%bilibili%'").fetchone()[0]
print(f'总Cookie数: {total}')
print(f'B站Cookies: {bili}')
if total > 0:
    sample = c.execute("SELECT name, host_key FROM cookies LIMIT 10").fetchall()
    print('\n前10个cookies:')
    for r in sample:
        print(f'  {r[0]} @ {r[1]}')
c.close()
