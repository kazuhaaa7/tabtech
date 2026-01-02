import requests

url = 'http://localhost:8080/api_tambah_saldo/'
data = {'jumlah': 10000, 'keterangan': 'test'}

try:
    response = requests.post(url, json=data)
    print('Status:', response.status_code)
    print('Response:', response.text)
except Exception as e:
    print('Error:', e)