from sqlite3 import connect
from instaloader import Instaloader

cookiefile = r'C:\Users\USER\AppData\Roaming\Mozilla\Firefox\Profiles\370tsjzy.default-release\cookies.sqlite'
print(f'Reading cookies from: {cookiefile}')

conn = connect(f'file:{cookiefile}?immutable=1', uri=True)
cookie_data = list(conn.execute("SELECT name, value FROM moz_cookies WHERE host LIKE '%.instagram.com%'"))
print(f'Found {len(cookie_data)} Instagram cookies')

if len(cookie_data) == 0:
    print('No Instagram cookies found! Please login to Instagram in Firefox first.')
    exit(1)

loader = Instaloader()
cookies_dict = dict(cookie_data)
loader.context._session.cookies.update(cookies_dict)
loader.context.username = 'ai_vanvan'

loader.save_session_to_file('temp/ai_vanvan_session')
print('Session saved to temp/ai_vanvan_session')

print('Testing login...')
if loader.test_login():
    print('Login successful!')
else:
    print('Login failed!')
