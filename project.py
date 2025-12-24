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
            return main_menu()
        
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
                    print("Thanks a lot")
                    time.sleep(1)
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
        print(f"=== MENU User Tabungan ===\nHalo {username}")
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
            return

# ------------------------ Tambah Saldo -- UserTabungan ------------------------
def tambahSaldo(username):
    while True: 
        os.system('cls')
        print('Halaman Tabungan')
        # db
        connection = connect_db()
        if connection is None:
            print("Koneksi tidak berhasil...")
            return
        
        try:
            cursor= connection.cursor()
            # tampilin tabel 
            query_colum = """
            SELECT 
            tabungan.no,
            tabungan.datee,
            tabungan.debit,
            tabungan.credit,
            tabungan.balance,
            tabungan.information,
            tabungan.username
            FROM tabungan.tabungan
            """
            cursor.execute(query_colum)
            table = cursor.fetchall()

            if table:
                os.system('cls')
                print("page add saldo")
                headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
                print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
            else:
                print('\n blm ada transaksi')
                input()


#                 # mulai menginput data
            tambahIsiSaldo = input("Masukkan saldo yang ingin ditambahkan: ")
            # pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
            if not tambahIsiSaldo :
                print('\nForm saldo yang akan dimasukkan tidak boleh kosong ')
                input('Ketik Enter untuk melanjutkan...')
                os.system('cls')
                connection.close()
                cursor.close()
                continue
            else:
                try:
                    tambahIsiSaldo = int(tambahIsiSaldo)
                    if tambahIsiSaldo <= 0:
                        print("Nominal harus lebih dari 0")
                        continue
                    print("angka yg dimasukkan:", tambahIsiSaldo)
                except:
                    input("input harus angka!!!!")
                    os.system('cls')
                    connection.close()
                    cursor.close()
                    break
        # verifikasi 
            verif = input(f'Kamu yakin untuk menambah saldo sebesar {tambahIsiSaldo}? [y]/[n] ').strip().lower()
            if verif == 'y':
                keterangan = input("Masukkan kepentingan anda: ")
                if not keterangan:
                    print("\nForm keterangan yang akan dimasukkan tidak boleh kosong ")
                    input('Ketik Enter untuk melanjutkan')
                    return

            elif verif == 'n':
                print("Penambahan saldo dibatalkan")
                input('Ketik Enter untuk kembali...')
                os.system('cls')
                connection.close()
                cursor.close()
                return
            else:
                print("Masukkan abjad dengan sesuai kocak...")
                input('Ketik Enter untuk kembali...')
                os.system('cls')
                connection.close()
                cursor.close()
                return

            cursor.execute("""
                        SELECT MAX(no)
                        FROM tabungan.tabungan
                        """)
            idx = cursor.fetchone()[0]
            no = (idx or 0) + 1

            isi_saldo = """
                        SELECT
                        t.balance
                        FROM tabungan.tabungan t
                        ORDER BY no 
                        DESC LIMIT 1 
                        """
            cursor.execute(isi_saldo)
            saldo = cursor.fetchone()
            if saldo:
                saldoTerakhir = saldo[-1]
            else:
                saldoTerakhir = 0

            saldoSum = saldoTerakhir + tambahIsiSaldo
            tanggal = datetime.now().strftime('%Y-%m-%d')

            final_saldo = """
                            INSERT INTO tabungan.tabungan (no, datee, debit, credit, balance, information, username)
                            VALUES (%s, %s, %s, %s, %s, %s, %s) 
                            """
            cursor.execute(final_saldo, (no, tanggal, tambahIsiSaldo, 0, saldoSum, keterangan, username))
            connection.commit()

            print(f"\nUser {username} berhasil menambahkan saldo)")
            input("Ketik Enter untuk lanjut...")
            return
        
        
        except Error as error:
            print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
            os.system('cls')
            connection.close()
            cursor.close()
            return
        
        finally:
            connection.close()
            cursor.close()

# ------------------------ Tambah Kredit -- UserTabungan ------------------------
def tambahKredit(username):
    while True:
        os.system('cls')
        print('Halaman Tabungan')
        # db
        connection = connect_db()
        if connection is None:
            print("Koneksi tidak berhasil...")
            return

        try:
            cursor = connection.cursor()

            # tampilin tabel
            query_colum = """
                SELECT 
                tabungan.no,
                tabungan.datee,
                tabungan.debit,
                tabungan.credit,
                tabungan.balance,
                tabungan.information,
                tabungan.username
                FROM tabungan.tabungan
                """
            cursor.execute(query_colum)
            table = cursor.fetchall()
            
            if table:
                os.system('cls')
                print("page add kredit")
                headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
                print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
            else:
                print('\n blm ada transaksi')
                input()

            tambahTransaksi = input("Masukkan kredit yang ingin ditambahkan: ")
        # pemeriksaan int empty tidak bisa, so... perlu perlu convert dri str ke int
            if not tambahTransaksi :
                    print('\nForm kredit yang akan dimasukkan tidak boleh kosong ')
                    input('Ketik Enter untuk melanjutkan...')
                    os.system('cls')
                    connection.close()
                    cursor.close()
                    continue
            else:
                try:
                    tambahTransaksi = int(tambahTransaksi)
                    if tambahTransaksi <= 0:
                        print("Nominal harus lebih dari 0")
                        continue
                except:
                    input("input harus angka!!!!")
                    os.system('cls')
                    connection.close()
                    cursor.close()
                    break

            # verifikasi
            verif = input(f'Kamu yakin untuk menambah kredit sebesar {tambahTransaksi}? [y]/[n] ').strip().lower()
            if verif == 'y':
                keterangan = input("Masukkan kepentingan anda: ")
                if not keterangan:
                    print('\nForm keterangan yang akan dimasukkan tidak boleh kosong ')
                    input('Ketik Enter untuk melanjutkan')
                    return
            elif verif == 'n':
                print("Penambahan saldo dibatalkan")
                input('Ketik Enter untuk kembali...')
                os.system('cls')
                connection.close()
                cursor.close()
                return
            else:
                print("Masukkan abjad dengan sesuai ya...")
                input('Ketik Enter untuk kembali...')
                os.system('cls')
                connection.close()
                cursor.close()
                return tambahKredit()
            

            cursor.execute("""
                            SELECT MAX(no)
                            FROM tabungan.tabungan                           
                            """)
            idx = cursor.fetchone()[0]
            no = (idx or 0) + 1

            isi_saldo = """
                        SELECT
                        t.balance
                        FROM tabungan.tabungan t
                        ORDER BY no 
                        DESC LIMIT 1 
                            """
            cursor.execute(isi_saldo)
            saldo = cursor.fetchone()
            if saldo:
                saldoTerakhir = saldo[-1]
            else:
                saldoTerakhir = 0

            saldoSum = saldoTerakhir - tambahTransaksi
            tanggal = datetime.now().strftime('%Y-%m-%d')

            final_saldo = """
            INSERT INTO tabungan.tabungan 
            (no, datee, debit, credit, balance, information, username)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(final_saldo, (no, tanggal, 0, tambahTransaksi, saldoSum,keterangan, username))
            connection.commit()

            print(f"\nUser {username} berhasil menambahkan saldo)")
            input("\nKetik Enter untuk lanjut...")
            return
        

        except Error as error:
            print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
            os.system('cls')
            connection.close()
            cursor.close()
            return

        finally:
            connection.close()
            cursor.close()

# ------------------------ Daftar Riwayat --  UserTabungan ------------------------
def daftarRiwayat():
    while True: 
        os.system('cls')
        print("Halaman Daftar Riwayat Tabungan")
        connection = connect_db()
        if connection is None:
            print("Koneksi tidak berhasil...")
            return
        try:
            cursor = connection.cursor()
            query_column = """
            SELECT
            t.no,
            t.datee,
            t.debit,
            t.credit,
            t.balance,
            t.information,
            t.username
            FROM tabungan.tabungan t
            """
            cursor.execute(query_column)
            table = cursor.fetchall()

            if table:
                os.system('cls')
                print("halaman keseluruhan")
                headers = ['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Username']
                print(tabulate(table, headers= headers, tablefmt='fancy_grid'))
            else:
                print('\n blm ada transaksi')
                input()
            while True:

                quer_2 = """
                SELECT 
                COALESCE(SUM(t.debit), 0),
                COALESCE(SUM(t.credit), 0)
                FROM tabungan.tabungan t
                """
                cursor.execute(quer_2)
                sumDebet, sumKredit = cursor.fetchone()


                query = """
                SELECT
                t.balance
                FROM tabungan.tabungan t
                ORDER BY no DESC
                LIMIT 1
                """
                cursor.execute(query)
                last = cursor.fetchone()
                if last:
                    saldoAkhir = last[-1]
                else:
                    saldoAkhir = 0

                print("Rangkuman:")
                print("Total Saldo: " f"Rp {saldoAkhir:,}")
                print("Total Uang Masuk: " f"Rp {sumDebet:,}")
                print("Total Uang Keluar: " f"Rp {sumKredit:,}")
                input('Tekan Enter untuk kembali...')
                return

        except Error as error:
            print(f"\nTerjadi kesalahan saat proses penambahan saldo: {error}")
            os.system('cls')
            connection.close()
            cursor.close()
            return

        finally:
            connection.close()
            cursor.close()



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

        pilihan = input("Pilih menu (1-3): ").strip()
        if pilihan == '1':
            print('Tunggu sebentar')
            time.sleep(0.5)
            result = validasiLogin()
            if result :
                role = result
                if role == "User Tabungan":
                    menu_user1()
        elif pilihan == '2':
            print('Tunggu sebentar')
            time.sleep(0.5)
            registrasi()
            return

        elif pilihan == '3':
            print("Terima kasih telah menggunakan sistem ==marketplace ini!")
            exit()
        else:
            input("Pilihan tidak valid! Tekan Enter untuk mencoba lagi...")

# ------------------------ JALANKAN PROGRAM ------------------------

main_menu()