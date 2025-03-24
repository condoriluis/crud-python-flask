import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return db
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)
        return None
