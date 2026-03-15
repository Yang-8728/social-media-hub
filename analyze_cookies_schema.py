import sqlite3

conn = sqlite3.connect('temp_analyze_cookies.db')
cursor = conn.cursor()

# 查看表结构
cursor.execute("PRAGMA table_info(cookies)")
columns = cursor.fetchall()

print("=" * 70)
print("Cookies 表结构:")
print("=" * 70)
for col in columns:
    cid, name, type_, notnull, default, pk = col
    required = " [必需]" if notnull else ""
    print(f"{cid:2d}. {name:30s} {type_:15s}{required}")

# 查看现有的 B站 Cookie（如果有）
cursor.execute("SELECT name, host_key FROM cookies WHERE host_key LIKE '%bilibili%' LIMIT 5")
existing = cursor.fetchall()

print("\n" + "=" * 70)
print(f"现有 B站 Cookies: {len(existing)} 个")
print("=" * 70)
for cookie in existing:
    print(f"  {cookie[0]:30s} @ {cookie[1]}")

conn.close()
