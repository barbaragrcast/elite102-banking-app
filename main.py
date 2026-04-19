from db import get_connection

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