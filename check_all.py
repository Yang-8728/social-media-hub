import sqlite3
c = sqlite3.connect('/tmp/source_cookies.db')
rows = c.execute("SELECT name, host_key FROM cookies WHERE host_key LIKE '%bilibili%'").fetchall()
print(f'找到 {len(rows)} 个B站cookies:')
domains = {}
for r in rows:
    domain = r[1]
    if domain not in domains:
        domains[domain] = []
    domains[domain].append(r[0])
for domain in sorted(domains.keys()):
    print(f'\n域名: {domain}')
    for name in domains[domain]:
        print(f'  - {name}')
c.close()
