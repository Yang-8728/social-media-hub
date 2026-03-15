import requests
r = requests.post('http://localhost:8080/api/scanner/scan', json={'account':'ai_vanvan','limit':50})
print('Status:', r.status_code)
print('Response:', r.text)
