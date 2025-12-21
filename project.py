import csv
import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from time import time
import numpy as np

FILE_USER = 'user.csv'
FILE_SALDO = 'saldo.csv'
FILE_TRANSAKSI = 'transaksi.csv'
FILE_TABUNGAN = 'tabungan.csv'


# ------------------------ FUNGSI LOGIN ------------------------
def login():
    os.system('cls')
    print("============================[ LOGIN ]============================")
    username = input("Masukkan username: ").strip().lower()
    password = input("Masukkan password: ").strip().lower()

    with open(FILE_USER, 'r', newline='') as file: 
        reader = csv.DictReader(file) 
        for row in reader:
            if row['username'] == username and row['password'] == password:
                role = row['role']
                print(f"\nLogin berhasil! Selamat datang, {username} | ({role})")
                input("Tekan Enter untuk ke program selanjutnya...")
                if role == 'userTabungan1':
                    menu_user1(username)
                    return
                if role == 'userTabungan2':
                    menu_user1(username)
                    return
                # else: 
                #     print("Username atau Password salah, dimohon untuk periksa ulang")
                #     input("Ketik Enter untuk kembali...")
                #     return 

    print("\nUsername atau password salah!")
    input("Tekan Enter untuk mencoba lagi...")

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
    os.system('cls')
    print('Halaman Tabungan')


    if not os.path.exists(FILE_TABUNGAN):
        with open(FILE_TABUNGAN, 'w', newline= '' ) as file_saldo :
            csv.writer(file_saldo).writerow(['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan'])
    
    df_tabungan = pd.read_csv(FILE_TABUNGAN)

    print(tabulate(df_tabungan, headers='keys', tablefmt='fancy_grid', showindex=False))

    tambahSaldo = int(input("Masukkan saldo yang ingin ditambahkan: "))
    try:
        verif = input(f'Kamu yakin untuk menambah saldo sebesar {tambahSaldo}? [y]/[n] ').strip().lower()
        if verif == 'y':
            keterangan = input("Masukkan kepentingan anda: ")
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
        'Keterangan' : keterangan
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
            csv.writer(file_transaksi).writerow(['No', 'Tanggal', 'Debet', 'Kredit', 'Saldo', 'Keterangan'])
    
    df_transksi = pd.read_csv(FILE_TABUNGAN)
    print(tabulate(df_transksi, headers='keys', tablefmt='fancy_grid', showindex=False))

    tambahTransaksi = int(input("Masukkan kredit yang ingin ditambahkan: "))
    try:
        verif = input(f'Kamu yakin untuk menambah kredit sebesar {tambahTransaksi}? [y]/[n] ').strip().lower()
        if verif == 'y':
            keterangan = input("Masukkan kepentingan anda: ")
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
        'Keterangan' : keterangan
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
        print("2. Keluar")
        print("===================================================================")
        pilihan = input("Pilih menu (1/2): ").strip()

        if pilihan == '1':
            login()
        elif pilihan == '2':
            print("Terima kasih telah menggunakan sistem ==marketplace ini!")
            exit()
        else:
            input("Pilihan tidak valid! Tekan Enter untuk mencoba lagi...")

# ------------------------ JALANKAN PROGRAM ------------------------

main_menu()