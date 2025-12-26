import requests

# cek isi post 
isi = {
    'nama': 'oci',
    'alamat' : 'mangli',
    'umur' : '19'
}
req = requests.post('http://127.0.0.1:8080/request',data=isi)
print(req.text)
