from unittest import result
from flask import Flask, request, render_template, url_for, session, flash, jsonify, redirect, current_app
from markupsafe import escape
import csv
import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import time
from psycopg2 import Error
from db.database import connect_db
from dotenv import load_dotenv 


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('FLASK_KEY')

@app.route('/')
def home_menu():
    """menampilkan halaman utama dengan menu"""
    # while True:
    #     os.system('cls')
    #     print("===================================================================")
    #     print("    TABUNGAN SEDERHANA    ")
    #     print("===================================================================")
    #     print("1. Login")
    #     print("2. Registrasi")
    #     print("3. Keluar")
    #     print("===================================================================")

    #     pilihan = input("Pilih menu (1-3): ").strip()
    #     if pilihan == '1':
    #         print('Tunggu sebentar')
    #         time.sleep(0.5)
    #         result = validasiLogin()
    #         if result :
    #             role = result
    #             if role == "User Tabungan":
    #                 menu_user1()
    #     elif pilihan == '2':
    #         print('Tunggu sebentar')
    #         time.sleep(0.5)
    #         menu_registrasi()
    #         return

    #     elif pilihan == '3':
    #         print("Terima kasih telah menggunakan sistem ini!")
    #         exit()
    #     else:
    #         input("Pilihan tidak valid! Tekan Enter untuk mencoba lagi...")
    return render_template("home.html")


@app.route("/menu_registrasi/")
def menu_registrasi():
    """API untuk mendapatkan dara menu home"""
#     while True:
#         os.system('cls')
#         print(""" 
# Please select the type of actor
# 1. User Savings
# 2. Admin * into maintanence
# 3. Back To Menu
# """)
#         typeActor = input('Select (1-3): ')
#         while True:
#             if typeActor == '1' or typeActor == 'User Savings':
#                 regisUserSavings()
#                 return
#             elif typeActor == '2' or typeActor == 'admin':
#                 print('into maintence')
#                 return
#             elif typeActor == '3' or typeActor == 'back to menu':
#                 return
#             else:
#                 print('Menu not ready')
#                 os.system('cls')
    return render_template('menu_registrasi.html')
            
@app.route('/api/menu/', methods = ['POST'])
def api_menu():
    """API untuk memproses pilihan menu"""
    data =  request.get_json()
    pilihan = data.get('pilihan')

    if pilihan == '1':
        return jsonify({'redirect': '/registrasi_user/'})
    elif pilihan == '2':
        return jsonify({'redirect': '/admin'})
    elif pilihan == '3':
        return jsonify({'message' : 'Terima kasih telah mengguanakan sistem ini'})
    else:
        return jsonify({'error': 'Pilihan tidak valid'}), 400 # ui jika menginputkan nomor yg tidak ada di perkondisian
    # Error 400 (Bad Request) artinya server tidak bisa memproses permintaan dari browser karena ada kesalahan di sisi klien
    



# ================ REGISTRASI ===================
@app.route("/registrasi_user/")
def regisUserSavings():
    """halaman pemilihan tipe registrasi"""
    # while True:
    #     os.system('cls')
    #     connection = connect_db()
    #     if connection is None:
    #         print("Koneksi tidak berhasil")
    #         return
        
    #     try:
    #         cursor = connection.cursor()
    #         print("=== REGISTER USER ===\n")

    #         while True:
    #             username = input("Isi Username: ").strip().lower()
    #             if username == '':
    #                 print('\n username tidak boleh angka')
    #                 input('Tekan Enter untuk kembali...')
    #                 return
    #             elif username.isdigit():
    #                 print('\n username tidak boleh ada unsur angka')
    #                 input('Tekan Enter untuk kembali...')

    #                 # cek user unik not duplicated
    #             check_query = """
    #             SELECT username FROM users.pengguna WHERE username = %s
    #             """
    #             cursor.execute(check_query, (username,))
    #             check_user = cursor.fetchone()

    #             if check_user:
    #                 print("\nUsername sudah digunakan! Silahkan gunakan username lain.")
    #                 input("Tekan Enter untuk kembali...")
    #                 continue
    #             else:
    #                 break
                
    #         while True:
    #             password = input("Isi Password: ").strip().lower()
    #             if password == '':
    #                 print('\n username tidak boleh angka')
    #                 input('Tekan Enter untuk kembali...')
    #                 continue
    #             else:
    #                 os.system('cls')
    #                 break
    #         role = "User Tabungan"

    #         # Query: ambl role 
    #         cursor.execute("SELECT roles FROM users.pengguna WHERE roles = %s", (role,))
    #         # row = cursor.fetchone()
    #         # if row:
    #         #     roles = role[0]
                
            
    #         # insert all data (for regis)
    #         insert_query ="""
    #         INSERT INTO users.pengguna (username, pw, roles)
    #         VALUES (%s,%s, %s)"""

    #         cursor.execute(insert_query,(username, password, role))
    #         connection.commit()

    #         print("\n Registrasi akun telah berhasil")
    #         print(f"Wellcome {username} ")

    #         input("Tekan Enter untuk melanjutkan...")
    #         cursor.close()
    #         connection.close()
    #         os.system('cls')
    #         return home_menu()
        
    #     except Error as error:
    #         print(f"terjadi kesalahan saat registrasi {error}")
    #         os.system('cls')
    #         if connection:
    #             connection.close()
            
    #     finally:
    #         if cursor:
    #             try:
    #                 cursor.close()
    #             except:
    #                 pass
    return render_template("registrasi_user.html")


@app.route("/api_registrasi_user/", methods=['POST'])  
def api_registrasi_user():
    #  1. Validasi Content-Type
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Content-Type must be application/json'}), 400
    """API untuk registrasi user baru"""
    data = request.get_json()
    username = data.get('username').lower().strip()  
    password = data.get('password').lower()  

    #validasi input
    if not username or not password:
        return jsonify({'error': 'Username dan password harus diisi'}), 400 
    # Error 4" adalah kode kesalahan umum, tetapi artinya sangat bergantung pada konteks atau perangkat spesifik yang menampilkannya. Kode ini tidak memiliki satu arti tunggal yang universal di semua sistem

    if username.isdigit():
        return jsonify({'error' : 'Username tidak boleh berisi angka'}), 400
    # Error 40 artinya da masalah teknis yang mencegah sistem berfungsi normal,

    # koneksi database
    connection = connect_db()
    if connection is None:
        return jsonify({'error' : 'Koneksi database gagal!'}), 500 
    # Error 500 (Internal Server Error) artinya server mengalami masalah tak terduga yang mencegahnya memenuhi permintaan Anda

    try:
        cursor = connection.cursor()
        
        # cek username unik
        check_query = """
SELECT username 
FROM users.pengguna 
WHERE username = %s
"""     
        cursor.execute(check_query, (username,))
        check_user = cursor.fetchone()

        if check_user:
            return jsonify({'error': 'Username telah digunakan!'}), 400
        
        # insert user baru
        role = 'User Tabungan'
        insert_query = """
        INSERT INTO users.pengguna  (username, pw, roles)
        VALUES (%s, %s, %s)
"""
        cursor.execute(insert_query, (username, password, role))
        connection.commit()

        return jsonify({
            'success' : True,
            'message' : f'Registrasi berhasil! Selamat datang {username}. Silahkan login...',
            'redierect': '/menu_registrasi/',
            'username' : username,
            'pasword' : password
        })
    
    except Error as error:
        return jsonify({'error': f'Terjadi kesalahan saat registrasi: {error}'}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ================ VALIDASI LOGIN ===================
@app.route("/login/")
def validasiLogin():
    """Halaman login"""
    # while True:
    #     os.system('cls')
    #     connection = connect_db()
    #     if connection is None:
    #         print("Koneksi database gagal!")
    #         return None
        
    #     try:
    #         cursor = connection.cursor()
            
    #         print("\n============================[ LOGIN ]============================")
    #         print("Ketik 1 uhntuk kembali ke halaman utama")
            
    #         while True:
    #             username = input("Masukkan username: ").strip().lower()

    #             if username == '1':
    #                 os.system('cls')
    #                 connection.close()
    #                 cursor.close()
    #                 print("Thanks a lot")
    #                 time.sleep(1)
    #                 return
    #             if username == '':
    #                 print("\nUsername tidak boleh kosong")
    #                 return None
    #             else:break
            
    #         while True:
    #             password = input("Masukkan password: ").strip()
    #             if password == '':
    #                 print("\nPassword tidak boleh kosong")
    #                 return None
    #             else:break
    #         # Query: ambil username dan pw untuk validasi login
    #         check_query = """
    #         SELECT pengguna.username, pengguna.pw, pengguna.roles FROM users.pengguna
    #         WHERE username = %s AND pw = %s
    #         """
    #         cursor.execute(check_query, (username, password))
    #         check_user = cursor.fetchone()


    #         if check_user:
    #             # login sukses -> ambil data dan arahkan hslaman sesuai role
    #             os.system('cls')
    #             name = check_user[0]
    #             role = check_user[2]
    #             print(f"\nbro {name} as {role}Login berhasil")
    #             input("Tekan Enter untuk melanjutkan...")


    #             cursor.close()
    #             connection.close()
    #             os.system('cls')

    #             if role == 'User Tabungan':
    #                 menu_user1(username)
    #             elif role == 'admin':
    #                 input("masih maintanence")
    #             else:
    #                 # role tidak dikenali -> arahkan ke menu utama
    #                 print("Role tidak dikenali")
    #                 validasiLogin()
    #             return
                
    #         else:
    #             os.system('cls')
    #             print('Username or Pw is wrong')
    #             input('Hold Enter for try again...')
    #             cursor.close()
    #             connection.close()
    #             os.system('cls')    
    #             return 

    #     except Error as error:
    #         print(f"\Terjadi kesalahan saat login: {error}")
    #         input("Tekan Enter untuk melanjutkan...")
    #         if connection:
    #             connection.close()
    #         connection
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         if connection:
    #             connection.close()
    return render_template('login_user.html')


@app.route("/api_login/", methods=['POST'])
def api_login_user():
    """API untuk proses login"""
     # 1. Validasi Content-Type
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # validasi input
    if not username or not password:
        return jsonify({'error': 'Username dan password harus diisi!'}), 400
    
    # koneks db
    connection = connect_db()
    if connection is None:
        return jsonify({'error': 'Koneksi database gagal!'}), 500
    
    try:
        cursor = connection.cursor()

        check_query = """
        SELECT username, pw, roles 
        FROM users.pengguna 
        WHERE username = %s AND pw =  %s
"""
        cursor.execute(check_query, (username, password))
        check_user = cursor.fetchone()

        if check_user:
            # simpan session
            session['username'] = check_user[0]
            session['roles'] = check_user[2]

        
        # tentukan redirect based role
            # if check_user['roles'] == 'User Tabungan':
            #     redirect_url = '/menu_user/'
            # elif check_user['roles'] == 'admin':
            #     redirect_url = '/admin'
            # else:
            #     redirect_url = '/'


            return jsonify({
                'success' : True,
                'message' : f'Login berhasil! Selamat datang {check_user[0]}',
                'redirect' : '/menu_user/' if check_user[2] == 'User Tabungan' else '/admin',
                'username' : check_user[0],
                'role': check_user[2]
                # 'redirect' :  redirect_url
            })
        else:
            return jsonify({'error': f'username atau password salah'}), 401
            # Error 401 "Unauthorized" artinya permintaan Anda ditolak karena tidak ada kredensial autentikasi yang valid atau belum login untuk mengakses sumber daya yang diminta
        
        # baca data atau query untuk validasi login
    except Exception as error:
        return jsonify({'error': f'Terjadi kesalahan saat login{error}'}),500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ================ MENU USER ===================
@app.route("/menu_user/")
def menu_user1():
    """Halaman menu user (harus login)"""
    # while True:
    #     os.system('cls')
    #     print(f"=== MENU User Tabungan ===\nHalo {username}")
    #     print("1. Tambah Saldo")
    #     print("2. Tambah Kredit")
    #     print("3. Riwayat Tabungan")
    #     print("5. Keluar")

    #     pilihan = input("Silahkan pilih menu: ")

    #     if pilihan == '1':
    #         tambahSaldo(username)
    #     elif pilihan == '2':
    #         tambahKredit(username)
    #     elif pilihan == '3':
    #         daftarRiwayat()
    #     elif pilihan == '5':
    #         return
    #     else:
    #         print("Pilihan tidak valid!")
    #         input("Tekan Enter...")
    #         return 
        
    return render_template("menu_user.html")


@app.route("/api_menu_user/", methods=['POST'])
def api_menu_user():
    """API untuk menu user"""
    if 'username' not in session:
        return jsonify({'error': 'Silahkan login terlebih dahulu!'}), 401
    

    data = request.get_json()
    pilihan =  data.get('pilihan')

    if pilihan == '1':
        return jsonify({'redirect': '/tambah_saldo/'})
    elif pilihan == '2':
        return jsonify({'redirect' : '/tambah_kredit/'})
    elif pilihan == '3':
        return  jsonify({'redirect': '/daftar_riwayat/'})
    elif pilihan == '5':
        session.clear()
        return jsonify({'redirect': '/'})
    # APA ITU session? kok sering dipanggil fungsiinya
    else:
        return jsonify({'error': 'Pilihan tidak sesuai'}), 400


# ==================== TAMBAH SALDO ====================
# @app.route("/tambah_saldo/")
# def tambahSaldo(username):
#     while True: 
#         os.system('cls')
#         print('Halaman Tabungan')
#         # db
#         connection = connect_db()
#         if connection is None:
#             print("Koneksi tidak berhasil...")
#             return
        
#         try:
#             cursor= connection.cursor()
#             # tampilin tabel 
#             query_colum = """
#             SELECT 
#             tabungan.no,
#             tabungan.datee,
#             tabungan.debit,
#             tabungan.credit,
#             tabungan.balance,
#             tabungan.information,
#             tabungan.username
#             FROM tabungan.tabungan
#             """
#             cursor.execute(query_colum)
#             table = cursor.fetchall()

#             if table:
#                 os.system('cls')
#                 print("page add saldo")
#                 headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
#                 print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
#             else:
#                 print('\n blm ada transaksi')
#                 input()


# #                 # mulai menginput data
#             tambahIsiSaldo = input("Masukkan saldo yang ingin ditambahkan: ")
#             # pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
#             if not tambahIsiSaldo :
#                 print('\nForm saldo yang akan dimasukkan tidak boleh kosong ')
#                 input('Ketik Enter untuk melanjutkan...')
#                 os.system('cls')
#                 connection.close()
#                 cursor.close()
#                 continue
#             else:
#                 try:
#                     tambahIsiSaldo = int(tambahIsiSaldo)
#                     if tambahIsiSaldo <= 0:
#                         print("Nominal harus lebih dari 0")
#                         continue
#                     print("angka yg dimasukkan:", tambahIsiSaldo)
#                 except:
#                     input("input harus angka!!!!")
#                     os.system('cls')
#                     connection.close()
#                     cursor.close()
#                     break
#         # verifikasi 
#             verif = input(f'Kamu yakin untuk menambah saldo sebesar {tambahIsiSaldo}? [y]/[n] ').strip().lower()
#             if verif == 'y':
#                 keterangan = input("Masukkan kepentingan anda: ")
#                 if not keterangan:
#                     print("\nForm keterangan yang akan dimasukkan tidak boleh kosong ")
#                     input('Ketik Enter untuk melanjutkan')
#                     return

#             elif verif == 'n':
#                 print("Penambahan saldo dibatalkan")
#                 input('Ketik Enter untuk kembali...')
#                 os.system('cls')
#                 connection.close()
#                 cursor.close()
#                 return
#             else:
#                 print("Masukkan abjad dengan sesuai kocak...")
#                 input('Ketik Enter untuk kembali...')
#                 os.system('cls')
#                 connection.close()
#                 cursor.close()
#                 return

#             cursor.execute("""
#                         SELECT MAX(no)
#                         FROM tabungan.tabungan
#                         """)
#             idx = cursor.fetchone()[0]
#             no = (idx or 0) + 1

#             isi_saldo = """
#                         SELECT
#                         t.balance
#                         FROM tabungan.tabungan t
#                         ORDER BY no 
#                         DESC LIMIT 1 
#                         """
#             cursor.execute(isi_saldo)
#             saldo = cursor.fetchone()
#             if saldo:
#                 saldoTerakhir = saldo[-1]
#             else:
#                 saldoTerakhir = 0

#             saldoSum = saldoTerakhir + tambahIsiSaldo
#             tanggal = datetime.now().strftime('%Y-%m-%d')

#             final_saldo = """
#                             INSERT INTO tabungan.tabungan (no, datee, debit, credit, balance, information, username)
#                             VALUES (%s, %s, %s, %s, %s, %s, %s) 
#                             """
#             cursor.execute(final_saldo, (no, tanggal, tambahIsiSaldo, 0, saldoSum, keterangan, username))
#             connection.commit()

#             print(f"\nUser {username} berhasil menambahkan saldo)")
#             input("Ketik Enter untuk lanjut...")
#             return
        
        
#         except Error as error:
#             print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
#             os.system('cls')
#             connection.close()
#             cursor.close()
#             return
        
#         finally:
#             connection.close()
#             cursor.close()      
    return render_template("tambah_saldo.html")


@app.route('/tambah_saldo/')
def tambah_saldo_page():
    """halaman tambah saldo"""
    if 'username' not in session:
        return redirect('/login/')
    
    # ambil data riwayat untuk ditampilkan
    connection = connect_db()
    if connection is None:
        return render_template("tambah_saldo.html", history=[], error= "koneksi database gagal!")
    
    try:
        cursor =  connection.cursor()
        query = """
        SELECT no,
        datee,
        debit, 
        credit,
        balance,
        information,
        username
        FROM tabungan.tabungan 
        WHERE username = %s 
        ORDER BY no DESC
"""
        cursor.execute(query, (session['username'],)) 
        history = cursor.fetchall()

        # format data untuk ditampilkan 
        formatted_history = []
        for row in history:
            formatted_history.append({
                'no': row[0],
                'tanggal': row[1].strftime('%Y,%m,%d') if row [1] else '',
                'debit' : f"Rp {row[2]:,}" if row[2] else "Rp 0",
                'credit' : f'Rp {row[3]:,}' if row[3] else 'Rp 0',
                'balance' : f"Rp {row[4]:,}" if row[4] else f"Rp 0",
                'information' : row[5] or '',
                'username': row[6] or ''
})
        return render_template('tambah_saldo.html',username = session['username'],
        history = formatted_history)
    
    except Error as error:
        return render_template('tambah_saldo.html', history = [],
        error = f'Terjadi kesalahan :{error}')
    

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/api_get_saldo/', methods=['GET'])
def api_get_saldo():
    """API untuk ambil saldo terakhir dan summary transaksi bulan ini"""
    username = request.args.get('username')
    
    if not username:
        return jsonify({'error': 'Parameter username tidak ada'}), 400
    
    try:
            # Koneksi ke database
            connection = connect_db()
            if connection is None:
                return jsonify({'error': 'Koneksi database gagal!'}), 500

            cursor = connection.cursor()
            
            # Query saldo terakhir
            cursor.execute("""
                SELECT balance FROM tabungan.tabungan
                ORDER BY no DESC
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            saldo_terakhir = float(result[0]) if result else 0

            # Query summary transaksi bulan ini (semua user)
            cursor.execute("""
                SELECT
                    COALESCE(SUM(debit), 0) as total_debit,
                    COALESCE(SUM(credit), 0) as total_credit
                FROM tabungan.tabungan
                WHERE DATE_TRUNC('month', datee) = DATE_TRUNC('month', CURRENT_DATE)
            """)

            summary_result = cursor.fetchone()
            total_debit_bulan = summary_result[0] if summary_result else 0
            total_credit_bulan = summary_result[1] if summary_result else 0

            return jsonify({
                "saldo": saldo_terakhir,
                "total_debit_bulan": total_debit_bulan,
                "total_credit_bulan": total_credit_bulan,
                "total_transactions": None  # Will be calculated if needed
            }), 200

    except Exception as e:
        current_app.logger.error(f"Error di api_get_saldo: {str(e)}")
        return jsonify({'error': 'Gagal mengambil saldo terakhir'}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()





@app.route('/api_tambah_saldo/', methods=['POST'])
def api_tambah_saldo():
    """API untuk tambah saldo"""


    if not request.is_json:
        return jsonify({"error": "Request harus berupa JSON"}), 400
    
    data = request.get_json()
    jumlah = data.get('jumlah')
    keterangan = data.get('keterangan', '')

    # validasi
    if not jumlah or not keterangan:
        return jsonify({'error': 'Jumlah dan keterangan harus diisi!'}), 400
    try:
        jumlah = int(jumlah)
        if jumlah < 1000:
            return jsonify({'error':'Nominal harus lebih dari 1000!'}),400
    except ValueError:
        return jsonify({'error': 'Jumlah harus berupa angka '}), 400
    
    # proses penambahan ke database
    
    try:
        connection = connect_db()
        if connection is None:
            return jsonify({'error': 'Koneksi database gagal!1'}), 500
        cursor = connection.cursor()

        # ambil nomer transaksi paling akhir | logic idx
        cursor.execute("SELECT MAX(no) FROM tabungan.tabungan")
        idx = cursor.fetchone()
        no = (idx[0] if idx and idx[0] is not None else 0) + 1


        # pilih lalu ambil 1 baris saldo paling akhir
        cursor.execute("""
        SELECT balance FROM tabungan.tabungan 
        ORDER BY no DESC
        LIMIT 1
""")
        result = cursor.fetchone()
        saldo_terakhir = result[0] if result else 0


        # hitung saldo baru
        saldo_baru = saldo_terakhir + jumlah
        tanggal = datetime.now().strftime('%Y-%m-%d')
 
        # insert  atau simpan transaksi
        insert_query = """
        INSERT INTO tabungan.tabungan
        (no, datee, debit, credit, balance, information, username)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
        print(f"DEBUG: Inserting with username = {session['username']}")  # Debug log
        cursor.execute(insert_query, (no, tanggal, jumlah, 0, saldo_baru, keterangan, session['username']))
        connection.commit()


        return jsonify({
            'success': True,
            'message': f'Berhasil menambahkan saldo sebesar Rp {jumlah:,}',
            'saldo_baru' : saldo_baru
        })
    

    except Error as error:
        return jsonify({'error': f'Terjadi kesalahan {error}'}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ==================== TAMBAH KREDIT ====================
# @app.route("/tambah_kredit/")
# def tambahKredit(username):
#     # while True:
#     #     os.system('cls')
#     #     print('Halaman Tabungan')
#     #     # db
#     #     connection = connect_db()
#     #     if connection is None:
#     #         print("Koneksi tidak berhasil...")
#     #         return

#     #     try:
#     #         cursor = connection.cursor()

#     #         # tampilin tabel
#     #         query_colum = """
#     #             SELECT 
#     #             tabungan.no,
#     #             tabungan.datee,
#     #             tabungan.debit,
#     #             tabungan.credit,
#     #             tabungan.balance,
#     #             tabungan.information,
#     #             tabungan.username
#     #             FROM tabungan.tabungan
#     #             """
#     #         cursor.execute(query_colum)
#     #         table = cursor.fetchall()
            
#     #         if table:
#     #             os.system('cls')
#     #             print("page add kredit")
#     #             headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
#     #             print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
#     #         else:
#     #             print('\n blm ada transaksi')
#     #             input()

#     #         tambahTransaksi = input("Masukkan kredit yang ingin ditambahkan: ")
#     #     # pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
#     #         if not tambahTransaksi :
#     #                 print('\nForm kredit yang akan dimasukkan tidak boleh kosong ')
#     #                 input('Ketik Enter untuk melanjutkan...')
#     #                 os.system('cls')
#     #                 connection.close()
#     #                 cursor.close()
#     #                 continue
#     #         else:
#     #             try:
#     #                 tambahTransaksi = int(tambahTransaksi)
#     #                 if tambahTransaksi <= 0:
#     #                     print("Nominal harus lebih dari 0")
#     #                     continue
#     #             except:
#     #                 input("input harus angka!!!!")
#     #                 os.system('cls')
#     #                 connection.close()
#     #                 cursor.close()
#     #                 break

#     #         # verifikasi
#     #         verif = input(f'Kamu yakin untuk menambah kredit sebesar {tambahTransaksi}? [y]/[n] ').strip().lower()
#     #         if verif == 'y':
#     #             keterangan = input("Masukkan kepentingan anda: ")
#     #             if not keterangan:
#     #                 print('\nForm keterangan yang akan dimasukkan tidak boleh kosong ')
#     #                 input('Ketik Enter untuk melanjutkan')
#     #                 return
#     #         elif verif == 'n':
#     #             print("Penambahan saldo dibatalkan")
#     #             input('Ketik Enter untuk kembali...')
#     #             os.system('cls')
#     #             connection.close()
#     #             cursor.close()
#     #             return
#     #         else:
#     #             print("Masukkan abjad dengan sesuai ya...")
#     #             input('Ketik Enter untuk kembali...')
#     #             os.system('cls')
#     #             connection.close()
#     #             cursor.close()
#     #             return tambahKredit()
            

#     #         cursor.execute("""
#     #                         SELECT MAX(no)
#     #                         FROM tabungan.tabungan                           
#     #                         """)
#     #         idx = cursor.fetchone()[0]
#     #         no = (idx or 0) + 1

#     #         isi_saldo = """
#     #                     SELECT
#     #                     t.balance
#     #                     FROM tabungan.tabungan t
#     #                     ORDER BY no 
#     #                     DESC LIMIT 1 
#     #                         """
#     #         cursor.execute(isi_saldo)
#     #         saldo = cursor.fetchone()
#     #         if saldo:
#     #             saldoTerakhir = saldo[-1]
#     #         else:
#     #             saldoTerakhir = 0

#     #         saldoSum = saldoTerakhir - tambahTransaksi
#     #         tanggal = datetime.now().strftime('%Y-%m-%d')

#     #         final_saldo = """
#     #         INSERT INTO tabungan.tabungan 
#     #         (no, datee, debit, credit, balance, information, username)
#     #         VALUES (%s,%s,%s,%s,%s,%s,%s)
#     #         """
#     #         cursor.execute(final_saldo, (no, tanggal, 0, tambahTransaksi, saldoSum,keterangan, username))
#     #         connection.commit()

#     #         print(f"\nUser {username} berhasil menambahkan saldo)")
#     #         input("\nKetik Enter untuk lanjut...")
#     #         return
        

#     #     except Error as error:
#     #         print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
#     #         os.system('cls')
#     #         connection.close()
#     #         cursor.close()
#     #         return

#     #     finally:
#     #         connection.close()
#     #         cursor.close()
#     return render_template("tambah_kredit.html")

@app.route('/tambah_kredit/')
def tambah_kredit_page():
    """Halaman tambah kredit"""
    if 'username' not in session:
        return redirect('/login/')
    
    
   # ambil data riwayat untuk ditampilkan
    connection = connect_db()
    if connection is None:
        return render_template("tambah_kredit.html", history=[], error= "koneksi database gagal!")
    
    try:
        cursor =  connection.cursor
        query = """
        SELECT no,
        datee,
        debit, 
        credit,
        balance,
        information,
        username
        FROM tabungan.tabungan 
        WHERE usename = %s 
        ORDER BY no DESC
"""
        cursor.execute(query, (session['username'],)) 
        history = cursor.fetchall()

        # format data untuk ditampilkan 
        formatted_history = []
        for row in history:
            formatted_history.append({
                'no': row[0],
                'tanggal': row[1].strftime('%Y,%m,%d') if row [1] else '',
                'debit' : f"Rp {row[2]:,}" if row[2] else "Rp 0",
                'credit' : f'Rp {row[3]:,}' if row[3] else 'Rp 0',
                'balance' : f"Rp {row[4]:,}" if row[4] else f"Rp 0",
                'information' : row[5] or '',
                'username': row[6] or ''
})
        return render_template('tambah_kredit.html',username = session['username'],
        history = formatted_history)
    
    except Error as error:
        return render_template('tambah_kredit.html', history = [],
        error = f'Terjadi kesalahan :{error}')
    

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/api_tambah_kredit/', methods=['POST'])
def api_tambah_kredit():
    """API untuk tambah kredit"""
    data = request.get_json()
    jumlah = data.get('jumlah')
    keterangan = data.get('keterangan', '')

    if not request.is_json:
        return jsonify({"error": "Request harus berupa JSON"}), 400

    # validasi
    if not jumlah or not keterangan:
        return jsonify({'error': 'Jumlah dan keterangan harus diisi!'}), 400
    
    try:
        jumlah = int(jumlah)
        if jumlah <= 0:
            return jsonify({'error':'Nominal harus lebih dari 1000!'}),400
    except ValueError:
        return jsonify({'error': 'Jumlah harus berupa angka '}), 400
    
    # proses penambahan ke database
    connection = connect_db()
    if connection is None:
        return jsonify({'error': 'Koneksi database gagal!1'}), 500
    
    try:
        cursor = connection.cursor()

        # ambil nomer transaksi paling akhir | logic idx
        cursor.execute("SELECT MAX(no) FROM tabungan.tabungan")
        idx = cursor.fetchone()
        no = (idx[0] if idx and idx[0] is not None else 0) + 1


        # pilih lalu ambil 1 baris saldo paling akhir
        cursor.execute("""
        SELECT balance FROM tabungan.tabungan 
        ORDER BY no DESC
        LIMIT 1
""")
        result = cursor.fetchone()
        saldo_terakhir = result[0] if result else 0


        # hitung saldo baru
        saldo_baru = saldo_terakhir - jumlah
        tanggal = datetime.now().strftime('%Y-%m-%d')

        # insert transaksi
        insert_query = """
        INSERT INTO tabungan.tabungan
        (no, datee, debit, credit, balance, information, username)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
        print(f"DEBUG: Inserting kredit with username = {session['username']}")  # Debug log
        cursor.execute(insert_query, (no, tanggal, 0, jumlah, saldo_baru, keterangan, session['username']))
        connection.commit()


        return jsonify({
            'success': True,
            'message': f'Berhasil menambahkan kredit sebesar Rp {jumlah:,}',
            'saldo_baru' : saldo_baru,
            'resul_baris_akhir': result[0]
        })
    

    except Error as error:
        return jsonify({'error': f'Terjadi kesalahan {error}'}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route("/daftar_riwayat/")
def daftar_riwayat_page():
    # while True: 
    #     os.system('cls')
    #     print("Halaman Daftar Riwayat Tabungan")
    #     connection = connect_db()
    #     if connection is None:
    #         print("Koneksi tidak berhasil...")
    #         return
    #     try:
    #         cursor = connection.cursor()
    #         query_column = """
    #         SELECT
    #         t.no,
    #         t.datee,
    #         t.debit,
    #         t.credit,
    #         t.balance,
    #         t.information,
    #         t.username
    #         FROM tabungan.tabungan t
    #         """
    #         cursor.execute(query_column)
    #         table = cursor.fetchall()

    #         if table:
    #             os.system('cls')
    #             print("halaman keseluruhan")
    #             headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
    #             print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
    #         else:
    #             print('\n blm ada transaksi')
    #             input()
    #         while True:

    #             quer_2 = """
    #             SELECT 
    #             COALESCE(SUM(t.debit), 0),
    #             COALESCE(SUM(t.credit), 0)
    #             FROM tabungan.tabungan t
    #             """
    #             cursor.execute(quer_2)
    #             sumDebet, sumKredit = cursor.fetchone()


    #             query = """
    #             SELECT
    #             t.balance
    #             FROM tabungan.tabungan t
    #             ORDER BY no DESC
    #             LIMIT 1
    #             """
    #             cursor.execute(query)
    #             last = cursor.fetchone()
    #             if last:
    #                 saldoAkhir = last[-1]
    #             else:
    #                 saldoAkhir = 0

    #             print("Rangkuman:")
    #             print("Total Saldo: " f"Rp {saldoAkhir:,}")
    #             print("Total Uang Masuk: " f"Rp {sumDebet:,}")
    #             print("Total Uang Keluar: " f"Rp {sumKredit:,}")
    #             input('Tekan Enter untuk kembali...')
    #             return

    #     except Error as error:
    #         print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
    #         os.system('cls')
    #         connection.close()
    #         cursor.close()
    #         return

    #     finally:
    #         connection.close()
    #         cursor.close()
        if 'username' not in session:
            return redirect('/login/')
        return render_template("daftar_riwayat.html",username = session['username'])

@app.route('/api_get_transaksi/', methods=['GET'])
def api_get_transaksi():
    """API untuk mendapatkan ringkasan transaksi debit dan credit user"""

    try:
        connection = connect_db()
        if connection is None:
            return jsonify({'error': 'Koneksi database gagal!'}), 500

        cursor = connection.cursor()

        # Query untuk menampilkan semua transaksi dari semua user (tabungan bersama)
        cursor.execute("""
            SELECT no, datee, debit, credit, balance, information, username
            FROM tabungan.tabungan
            ORDER BY no DESC
        """,)

        transactions = cursor.fetchall()

        # Format data transaksi
        formatted_transactions = []
        for row in transactions:
            # Pastikan username tidak null
            formatted_transactions.append({
                'no': row[0],
                'tanggal': row[1].strftime('%Y-%m-%d') if row[1] else '-',
                'debit': f"Rp {row[2]:,}" if row[2] and row[2] > 0 else '-',
                'credit': f"Rp {row[3]:,}" if row[3] and row[3] > 0 else '-',
                'balance': f"Rp {row[4]:,}" if row[4] else 'Rp 0',
                'information': row[5] or '-',
                'username': row [6] if row[6] else session.get('username')
            })

        # Query untuk total debit dan credit bulan ini (semua user)
        cursor.execute("""
            SELECT
                COALESCE(SUM(debit), 0) as total_debit,
                COALESCE(SUM(credit), 0) as total_credit
            FROM tabungan.tabungan
            WHERE DATE_TRUNC('month', datee) = DATE_TRUNC('month', CURRENT_DATE)
        """,)

        summary_result = cursor.fetchone()
        total_debit_bulan = summary_result[0] if summary_result else 0
        total_credit_bulan = summary_result[1] if summary_result else 0

                # Query saldo terakhir
        cursor.execute("""
                SELECT balance FROM tabungan.tabungan
                ORDER BY no DESC
                LIMIT 1
            """,)

        result = cursor.fetchone()
        saldo_terakhir = result[0] if result else 0
        # saldo_terakhir = total_debit_bulan - total_credit_bulan

        return jsonify({
            'success': True,
            'transactions': formatted_transactions,
            'summary': {
                'total_debit_bulan': total_debit_bulan,
                'total_credit_bulan': total_credit_bulan,
                'total_saldo': saldo_terakhir
            }
        }), 200
        




    except Exception as e:
        current_app.logger.error(f"Error di api_get_transaksi_summary: {str(e)}")
        return jsonify({'success': False,
            'error': 'Gagal mengambil data transaksi'}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api_daftar_riwayat/')
def api_daftar_riwayat():
    """API untuk daftar riwayat"""
    if 'username' not in session:
        return jsonify({'error': 'Silahkan login terlebi dahulu!'}),401

    connection = connect_db()
    if connection is None:
        return jsonify({"error": "Koneksi database gagal!"}),500

    try:
        cursor =  connection.cursor()

        # ambil riwayat transaksi
        query = """
        SELECT
        no,
        datee,
        debit,
        credit,
        balance, 
        information, 
        username FROM tabungan.tabungan
        WHERE username = %s
        ORDER BY no DESC
"""
        cursor.execute(query, (session['username']))
        history = cursor.fetchall()

        # format data
        formatted_history = []
        for row in history:
            formatted_history.append({
                'no' : row[0],
                'tanggal': row[1].strftime('%Y-%m-%d') if row[1] else '',
                'debit' : f"Rp {row[2]:,}" if row[2] else 'Rp 0',
                'credit' : f"Rp {row[3]:,}" if row[3] else 'Rp 0',
                'balance' : f"Rp {row[4]:,}" if row[4] else 'Rp 0',
                'information' : row[5] or '',
                'username' : row[6] or ''
            })

        # hitung total kolom credit dan debit
        query_total = """
        SELECT 
        COALESCE(SUM(debit), 0),
        COALESCE(SUM(credit), 0)
        FROM tabungan.tabungan
        WHERE username = %s
""", (session['username'],)
        cursor.execute(query_total, (session['username']))
        total_debit, total_credit = cursor.fetchone()

        # ambil saldo akhir
        query_total_saldo = """
        SELECT balance FROM tabungan.tabungan
        WHERE username = %s
        ORDER BY no DESC LIMIT 1
""", (session['username'],)
        result = cursor.fetchone()
        saldo_akhir = result[0] if result else 0 

        return jsonify({
            'success': True,
            'history': formatted_history,
            'summary' : {
                'saldo_akhir': saldo_akhir,
                'total_debit': total_debit,
                'total_credit': total_credit
            }
        })

    except Error as error:
        return jsonify({'error': f'Terjadi kesalahan: {error}'}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()  


  # ==================== LOGOUT ====================


@app.route('/logout/')
def logout():
    """Logout dan hapus session"""
    return redirect('/')

@app.route('/api_get_username/', methods=['GET'])
def get_username():
    """Endpoint untuk mengambil username dari session"""
    username = session.get('username', 'User Tabungan')
    print(f"DEBUG: get_username - username dari session: {username}")
    return jsonify({
        'username': username,
        'logged_in': username != 'User Tabungan'
    })

@app.route("/api_check_username/", methods=['GET'])
def api_check_username():
    """API untuk mengecek status login"""
    username  = request.args.get('username')
    if not username:
        return jsonify({'success': False,
                        'message': 'ussername tidak diberikan'})

    connection = connect_db()
    if connection is None:
        return jsonify({'success': False,
                        'message': 'koneksi database gagal!'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT username
        FROM users.pengguna WHERE username = %s
        """, (username,))
        exists = cursor.fetchone() is not None
        return jsonify({"success": not exists,
                        'data': username if not exists else ''})


    except Exception as e:
        current_app.logger.error(f"Error cek username {str(e)}")
        return jsonify({'success': False,
                        'message': 'terjadi kesalahan server'}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
# Pastikan endpoint ini ada dan benar


if __name__ == '__main__':
    app.run(debug=True)