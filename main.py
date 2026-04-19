import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

print("Starting program...")



conn = get_connection()
cursor = conn.cursor()

print("Connected!")

# Query your table (CHANGE NAME IF NEEDED)
cursor.execute("SELECT * FROM bank_accounts")  # <-- change if your table name is different

rows = cursor.fetchall()


for row in rows:
    print(row)

conn.close()

print("Done.")