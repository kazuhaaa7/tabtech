from flask import Flask

# === untuk memanggil instancec flask
app = Flask(__name__) # bawaan flask
# ===

# karna flask ini pemograman berbasis web dan itu memrelukan page web. route yg akan menjadi penghubungnya
# home page
@app.route('/') # -> bawaan flask 
def home():
    return '<h1> Hello page </h1>' 

# contact page
@app.route('/contact')
def contact():
    return '<h1> Contact page </h1>'

# about page
@app.route('/about')
def about():
    return '<h1> Abouit page </h1>'

# profile page
@app.route('/profile', defaults={'_route': 'home', 'username': 'ahmad'})
# def profil():
#     return '<h1> Profile </h1>'

# membuat user dengan input manual lewat url
@app.route('/profile/<string:username>', defaults={'_route': 'profile'})
def profil_name(username, _route):
    if _route == "home":
        return '<h1> iki home page  cak </h1>'
    elif _route == "profile":
        username = username + ", loh"
        return '<h1> Hai %s iki profile page cak</h1>' % username

app.run(debug=True)
# adanya parameter <debug=True> bertujuan untuk menguodate ouput code secara otomatis tanpa pencet tombol running or ketik 'python .py', dan tinggal refresh di webnya.


