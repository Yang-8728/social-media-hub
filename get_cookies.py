import sqlite3, shutil, json, os
cookie_db = r'tools\profiles\chrome_profile_ai_vanvan\Default\Network\Cookies'
temp_db = 'temp.db'
shutil.copy2(cookie_db, temp_db)
conn = sqlite3.connect(temp_db)
c = conn.cursor()
c.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%bilibili.com%'")
cookies = {n: v for n, v in c.fetchall()}
conn.close()
os.remove(temp_db)
print(len(cookies), 'cookies')
with open('config/ai_vanvan.json', 'w') as f:
    json.dump({'cookie_info': {'cookies': cookies}}, f, indent=2)
print('Done')
