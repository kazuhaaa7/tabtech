# Sistem Tabungan Sederhana

## Deskripsi
Sistem tabungan sederhana berbasis console yang memungkinkan pengguna untuk mendaftar, login, menambah saldo (debit), menambah kredit, dan melihat riwayat tabungan. Sistem ini menggunakan PostgreSQL sebagai database dan dirancang untuk operasi dasar tabungan.

## Struktur Proyek
```
.
├── .env
├── .gitignore
├── .txt
├── main.py
├── README.md
├── __pycache__/
├── Logic-database/
│   ├── .env
│   ├── .gitignore
│   ├── project.py
│   └── db/
│       ├── database.py
│       └── __pycache__/
└── virtual/
    ├── CACHEDIR.TAG
    ├── pyvenv.cfg
    ├── Lib/
    │   └── site-packages/
    │       ├── _virtualenv.pth
    │       ├── _virtualenv.py
    │       ├── pip-25.3.virtualenv
    │       ├── __pycache__/
    │       ├── blinker/
    │       ├── blinker-1.9.0.dist-info/
    │       ├── click/
    │       ├── click-8.3.1.dist-info/
    │       ├── colorama/
    │       └── ...
    └── Scripts/
        ├── activate
        ├── activate_this.py
        ├── activate.bat
        ├── activate.fish
        ├── activate.nu
        ├── activate.ps1
        ├── deactivate.bat
        ├── pydoc.bat
        └── python3
```

## Fitur
- Registrasi pengguna dengan role "User Tabungan"
- Login dengan validasi username dan password
- Menu pengguna untuk menambah saldo, menambah kredit, dan melihat riwayat
- Penyimpanan data transaksi di database PostgreSQL
- Tampilan tabel riwayat menggunakan tabulate
- Perhitungan saldo otomatis berdasarkan debit dan kredit

## Prasyarat
- Python 3.x
- PostgreSQL
- Library Python: psycopg2, python-dotenv, tabulate, pandas, numpy

## Instalasi
1. Clone repositori ini.
2. Install dependencies:
   ```sh
   pip install psycopg2-binary python-dotenv tabulate pandas numpy
   ```
3. Setup database PostgreSQL dan buat schema `users` dan `tabungan` sesuai dengan kode.
4. Buat file `.env` dengan kredensial database:
   ```
   DB_HOST=your_host
   DB_NAME=your_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   ```

## Penggunaan
Jalankan program utama:
```sh
python project.py
```
Ikuti menu untuk registrasi, login, dan operasi tabungan.

## Setup Database
Pastikan PostgreSQL berjalan dan buat tabel:
- `users.pengguna` dengan kolom: username, pw, roles
- `tabungan.tabungan` dengan kolom: no, datee, debit, credit, balance, information, username

## To Copilot
@workspace generate a readme document that can be used as a repo description