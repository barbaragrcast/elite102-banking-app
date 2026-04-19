import mysql.connector
from .env import conn

print("Starting program...")



cursor = conn.cursor()

print("Connected!")

# Query your table (CHANGE NAME IF NEEDED)
cursor.execute("SELECT * FROM bank_accounts")  # <-- change if your table name is different

rows = cursor.fetchall()

print("Rows:", rows)

for row in rows:
    print(row)

conn.close()

print("Done.")