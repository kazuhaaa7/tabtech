from flask import Flask

# === untuk memanggil instancec flask
app = Flask(__name__) # bawaan flask
# ===

# karna flask ini pemograman berbasis web dan itu memrelukan page web. route yg akan menjadi penghubungnya
@app.route('/') # -> bawaan flask | home page

def hp():
    return '<h1> Hello cantik </h1>' 

app.run(debug=True)
# adanya parameter <debug=True> bertujuan untuk menguodate ouput code secara otomatis tanpa pencet tombol running or ketik 'python .py', dan tinggal refresh di webnya.


