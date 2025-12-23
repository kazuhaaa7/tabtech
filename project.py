import csv
import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import time
import numpy as np
import psycopg2
from psycopg2 import Error
from db.database import connect_db
from dotenv import load_dotenv 




FILE_TABUNGAN = 'tabungan.csv'

def registrasi():
    while True:
        os.system('cls')
        print(""" 
Please select the type of actor
1. User Savings
2. Admin * into maintanence
3. Back To Menu
""")
        typeActor = input('Select (1-3): ')
        while True:
            if typeActor == '1' or typeActor == 'user savings':
                regisUserSavings()
                return
            elif typeActor == '2' or typeActor == 'admin':
                print('into maintence')
                return
            elif typeActor == '3' or typeActor == 'back to menu':
                return
            else:
                print('Menu not ready')
                os.system('cls')
                return

# ------------------------ FUNGSI REGISTER ------------------------
def regisUserSavings():
    while True:
        os.system('cls')
        connection = connect_db()
        if connection is None:
            print("Koneksi tidak berhasil")
            return
        
        try:
            cursor = connection.cursor()
            print("=== REGISTER USER ===\n")

            while True:
                username = input("Isi Username: ").strip().lower()
                if username == '':
                    print('\n username tidak boleh angka')
                    input('Tekan Enter untuk kembali...')
                    return
                elif username.isdigit():
                    print('\n username tidak boleh ada unsur angka')
                    input('Tekan Enter untuk kembali...')

                    # cek user unik not duplicated
                check_query = """
                SELECT username FROM users.pengguna WHERE username = %s
                """
                cursor.execute(check_query, (username,))
                check_user = cursor.fetchone()

                if check_user:
                    print("\nUsername sudah digunakan! Silahkan gunakan username lain.")
                    input("Tekan Enter untuk kembali...")
                    continue
                else:
                    break
                
            while True:
                password = input("Isi Password: ").strip().lower()
                if password == '':
                    print('\n username tidak boleh angka')
                    input('Tekan Enter untuk kembali...')
                    continue
                else:
                    os.system('cls')
                    break
            role = "User Tabungan"

            # Query: ambl role 
            cursor.execute("SELECT roles FROM users.pengguna WHERE roles = %s", (role,))
            # row = cursor.fetchone()
            # if row:
            #     roles = role[0]
                
            
            # insert all data (for regis)
            insert_query ="""
            INSERT INTO users.pengguna (username, pw, roles)
            VALUES (%s,%s, %s)"""

            cursor.execute(insert_query,(username, password, role))
            connection.commit()

            print("\n Registrasi akun telah berhasil")
            print(f"Wellcome {username} ")

            input("Tekan Enter untuk melanjutkan...")
            cursor.close()
            connection.close()
            os.system('cls')
            return
        
        except Error as error:
            print(f"terjadi kesalahan saat registrasi {error}")
            os.system('cls')
            if connection:
                connection.close()
            
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

# ------------------------ FUNGSI LOGIN ------------------------
def validasiLogin():
    while True:
        os.system('cls')
        connection = connect_db()
        if connection is None:
            print("Koneksi database gagal!")
            return None
        
        try:
            cursor = connection.cursor()
            
            print("\n============================[ LOGIN ]============================")
            print("Ketik 1 uhntuk kembali ke halaman utama")
            
            while True:
                username = input("Masukkan username: ").strip().lower()

                if username == '1':
                    os.system('cls')
                    connection.close()
                    cursor.close()
                    time.sleep("Thanks a lot")
                    return
                if username == '':
                    print("\nUsername tidak boleh kosong")
                    return None
                else:break
            
            while True:
                password = input("Masukkan password: ").strip()
                if password == '':
                    print("\nPassword tidak boleh kosong")
                    return None
                else:break
            # Query: ambil username dan pw untuk validasi login
            check_query = """
            SELECT pengguna.username, pengguna.pw, pengguna.roles FROM users.pengguna
            WHERE username = %s AND pw = %s
            """
            cursor.execute(check_query, (username, password))
            check_user = cursor.fetchone()


            if check_user:
                # login sukses -> ambil data dan arahkan hslaman sesuai role
                os.system('cls')
                name = check_user[0]
                role = check_user[2]
                print(f"\nbro {name} as {role}Login berhasil")
                input("Tekan Enter untuk melanjutkan...")


                cursor.close()
                connection.close()
                os.system('cls')

                if role == 'User Tabungan':
                    menu_user1(username)
                elif role == 'admin':
                    input("masih maintanence")
                else:
                    # role tidak dikenali -> arahkan ke menu utama
                    print("Role tidak dikenali")
                    validasiLogin()
                return
                
            else:
                os.system('cls')
                print('Username or Pw is wrong')
                input('Hold Enter for try again...')
                cursor.close()
                connection.close()
                os.system('cls')    
                return 

        except Error as error:
            print(f"\Terjadi kesalahan saat login: {error}")
            input("Tekan Enter untuk melanjutkan...")
            if connection:
                connection.close()
            connection
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# ------------------------ MENU ADMIN ------------------------
def menu_user1(username):
    while True:
        os.system('cls')
        print(f"=== MENU ADMIN ===\nHalo {username}")
        print("1. Tambah Saldo")
        print("2. Tambah Kredit")
        print("3. Riwayat Tabungan")
        print("5. Keluar")

        pilihan = input("Silahkan pilih menu: ")

        if pilihan == '1':
            tambahSaldo(username)
        elif pilihan == '2':
            tambahKredit(username)
        elif pilihan == '3':
            daftarRiwayat()
        elif pilihan == '5':
            return
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter...")

# ------------------------ Tambah Saldo -- UserTabungan ------------------------
def tambahSaldo(username):
    while True: 
        os.system('cls')
        print('Halaman Tabungan')

        if not os.path.exists(FILE_TABUNGAN):
            with open(FILE_TABUNGAN, 'w', newline= '' ) as file_saldo :
                csv.writer(file_saldo).writerow(['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username'])
        
        df_tabungan = pd.read_csv(FILE_TABUNGAN)

        print(tabulate(df_tabungan, headers='keys', tablefmt='fancy_grid', showindex=False))
        tambahSaldo = input("Masukkan saldo yang ingin ditambahkan: ")
        # pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
        if not tambahSaldo :
            print('Form saldo yang akan dimasukkan tidak boleh kosong ')
            input('Ketik Enter untuk melanjutkan...')
            return
        else:
            try:
                tambahSaldo == int(tambahSaldo)
                print("angka yg dimasukkan:", tambahSaldo)
            except:
                input("input harus berupa angka ya...")
                return
            
        try:
            verif = input(f'Kamu yakin untuk menambah saldo sebesar {tambahSaldo}? [y]/[n] ').strip().lower()
            if verif == 'y':
                keterangan = input("Masukkan kepentingan anda: ")
                if not keterangan:
                    print('Form keterangan yang akan dimasukkan tidak boleh kosong ')
                    input('Ketik Enter untuk melanjutkan')
                    return

            elif verif == 'n':
                print("Penambahan saldo dibatalkan")
                input('Ketik Enter untuk kembali...')
                return
            else:
                print("Masukkan abjad dengan sesuai ya...")
                input('Ketik Enter untuk kembali...')
                return
        except ValueError:
            print("Error verifikasi saldo")
            input("Ketik Enter untuk kembali...")


        if not df_tabungan.empty:
            no = df_tabungan['No'].max() + 1
        else:
            no = df_tabungan['No'] = 1

        # df_saldo['Debet'] = df_saldo['Debet'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))
        # df_saldo['Kredit'] = df_saldo['Kredit'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))
        # df_saldo['Saldo'] = df_saldo['Saldo'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))

        if df_tabungan['Saldo'].empty:
            saldoTerakhir = 0
        else:
            saldoTerakhir = df_tabungan['Saldo'].iloc[-1]

        kredit = 0
        saldoSum = saldoTerakhir + tambahSaldo


        newrow = {
            'No' : no,
            'Tanggal' : datetime.now().strftime('%d-%m-%Y'),
            'Debet' : tambahSaldo,
            'Kredit' : kredit,
            'Saldo' : saldoSum,
            'Keterangan' : keterangan,
            'Username': username
            }



        with open(FILE_TABUNGAN, 'a', newline= '') as newline:
            writer = csv.writer(newline)
            writer.writerow([[newrow['No'], newrow['Tanggal'], newrow['Debet'], newrow['Kredit'], newrow['Saldo'], newrow['Keterangan']]])
        
        df_tabungan = pd.concat([df_tabungan, pd.DataFrame([newrow])], ignore_index=True)
        df_tabungan.to_csv(FILE_TABUNGAN, index=False)

        print(f"\nUser {username} berhasil menambahkan saldo)")
        input("\nKetik Enter untuk lanjut...")
        return

# ------------------------ Tambah Kredit -- UserTabungan ------------------------
def tambahKredit(username):
    os.system('cls')
    print('Halaman Tabungan')

    if not os.path.exists(FILE_TABUNGAN):
        with open(FILE_TABUNGAN, 'w', newline= '' ) as file_transaksi :
            csv.writer(file_transaksi).writerow(['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username'])
    
    df_transksi = pd.read_csv(FILE_TABUNGAN)
    print(tabulate(df_transksi, headers='keys', tablefmt='fancy_grid', showindex=False))

    tambahTransaksi = input("Masukkan kredit yang ingin ditambahkan: ")
# pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
    if not tambahTransaksi :
            print('Form kredit yang akan dimasukkan tidak boleh kosong ')
            input('Ketik Enter untuk melanjutkan...')
            return
    else:
            try:
                tambahTransaksi == int(tambahTransaksi)
                print("angka yg dimasukkan:", tambahTransaksi)
            except:
                input("input harus berupa angka ya...")
                return

    try:
        verif = input(f'Kamu yakin untuk menambah kredit sebesar {tambahTransaksi}? [y]/[n] ').strip().lower()
        if verif == 'y':
            keterangan = input("Masukkan kepentingan anda: ")

            if not keterangan:
                print('Form keterangan yang akan dimasukkan tidak boleh kosong ')
                input('Ketik Enter untuk melanjutkan')
                return
        elif verif == 'n':
            print("Penambahan saldo dibatalkan")
            input('Ketik Enter untuk kembali...')
            return
        else:
            print("Masukkan abjad dengan sesuai ya...")
            input('Ketik Enter untuk kembali...')
            return tambahKredit()
    except ValueError:
        print("Error verifikasi kredit")
        input("Ketik Enter untuk kembali...")


    if not df_transksi.empty:
        no = df_transksi['No'].max() + 1
    else:
        no = df_transksi['No'] = 1

    # df_transksi['Debet'] = df_transksi['Debet'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))
    # df_transksi['Kredit'] = df_transksi['Kredit'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))
    # df_transksi['Saldo'] = df_transksi['Saldo'].apply(lambda x: f"Rp {x:,.0f}".replace(',', '.').replace('.', ',', 1))

    if df_transksi['Saldo'].empty:
        saldoTerakhir = 0
    else:
        saldoTerakhir = df_transksi['Saldo'].iloc[-1]

    debet = 0
    saldoSum = saldoTerakhir - tambahTransaksi


    newrow = {
        'No' : no,
        'Tanggal' : datetime.now().strftime('%d-%m-%Y'),
        'Debet' : debet,
        'Kredit' : tambahTransaksi,
        'Saldo' : saldoSum,
        'Keterangan' : keterangan,
        'Username': username
        }


    with open(FILE_TABUNGAN, 'a', newline= '') as newline:
        writer = csv.writer(newline)
        writer.writerow([[newrow['No'], newrow['Tanggal'], newrow['Debet'], newrow['Kredit'], newrow['Saldo'], newrow['Keterangan']]])
    
    df_transksi = pd.concat([df_transksi, pd.DataFrame([newrow])], ignore_index=True)
    df_transksi.to_csv(FILE_TABUNGAN, index=False)

    print(f"\nUser {username} berhasil menambahkan saldo)")
    input("\nKetik Enter untuk lanjut...")
    return

# ------------------------ Daftar Riwayat --  UserTabungan ------------------------
def daftarRiwayat():
    os.system('cls')
    print("Halaman Daftar Riwayat Tabungan")

    if not os.path.exists(FILE_TABUNGAN):
        with open(FILE_TABUNGAN, 'w', newline='') as file_tabungan:
            csv.writer(file_tabungan).writerow(['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan'])

    df_tabungan = pd.read_csv(FILE_TABUNGAN)
    print(tabulate(df_tabungan, headers='keys', tablefmt='fancy_grid', showindex=False))
    input("neext")
    sumSaldo = df_tabungan['Saldo'].iloc[-1]
    sumDebet = df_tabungan['Debet'].sum()
    sumKredit = df_tabungan['Kredit'].sum()

    print("Rangkuman:")
    print("Total Saldo: " f"Rp {sumSaldo:,}")
    print("Total Uang Masuk: " f"Rp {sumDebet:,}")
    print("Total Uang Keluar: " f"Rp {sumKredit:,}")
    input("next")


# # ------------------------ MENU UTAMA ------------------------
def main_menu():
    while True:
        os.system('cls')
        print("===================================================================")
        print("    TABUNGAN SEDERHANA    ")
        print("===================================================================")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        print("===================================================================")
        pilihan = input("Pilih menu (1/2/3): ").strip()

        if pilihan == '1':
            print('Tunggu sebentar')
            result = validasiLogin()
            if result :
                role = result
                if role == "User Tabungan":
                    menu_user1()
        elif pilihan == '2':
            print('Tunggu sebentar')
            registrasi()
            return

        elif pilihan == '3':
            print("Terima kasih telah menggunakan sistem ==marketplace ini!")
            exit()
        else:
            input("Pilihan tidak valid! Tekan Enter untuk mencoba lagi...")

# ------------------------ JALANKAN PROGRAM ------------------------

main_menu()