import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv 
import os

def connect_db():
    load_dotenv()
    try :
        # create connection
        connection = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            database = os.getenv('DB_NAME'),
            user =  os.getenv('DB_USER'),
            password = os.getenv('DB_PW')
        )
        print("Berhasil terhubung ke PostgreSQL!")
        return connection

    except Exception as e:
        print("Gagal terhubung PostgreSQL", e)
        return None

