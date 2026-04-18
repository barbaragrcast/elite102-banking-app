import mysql.connector

print("Starting program...")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chispita2013*",   # your password
    database="banking_app"      # MUST match your DB
)

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