from db import get_connection
from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    balance = request.form.get("balance")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bank_accounts (username, password, balance) VALUES (%s, %s, %s)",
        (username, password, balance)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('dashboard', username=username))



@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bank_accounts WHERE username = %s AND password = %s",
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return redirect(url_for('dashboard', username=username))
    else:
        return "Invalid login"



@app.route('/dashboard/<username>')
def dashboard(username):
    conn = get_connection()
    cursor = conn.cursor()

  
    cursor.execute(
        "SELECT id, balance FROM bank_accounts WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        return "User not found"

    user_id = user[0]
    balance = user[1]

  
    cursor.execute(
        "SELECT balance, date FROM bank_transactions WHERE id = %s ORDER BY date DESC",
        (user_id,)
    )
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        username=username,
        balance=balance,
        transactions=transactions
    )


@app.route('/send', methods=['POST'])
def send():
    try:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        amount = request.form.get("amount")

        if not sender or not receiver or not amount:
            return "Missing form data"

        amount = float(amount)

        conn = get_connection()
        cursor = conn.cursor()

        # Get sender
        cursor.execute(
            "SELECT id, balance FROM bank_accounts WHERE username = %s",
            (sender,)
        )
        sender_data = cursor.fetchone()

        if not sender_data:
            return "Sender not found"

        sender_id = sender_data[0]
        sender_balance = sender_data[1]

        if sender_balance < amount:
            return "Not enough money"

        # Get receiver
        cursor.execute(
            "SELECT id FROM bank_accounts WHERE username = %s",
            (receiver,)
        )
        receiver_data = cursor.fetchone()

        if not receiver_data:
            return "Receiver not found"

        receiver_id = receiver_data[0]

        # Update balances
        cursor.execute(
            "UPDATE bank_accounts SET balance = balance - %s WHERE id = %s",
            (amount, sender_id)
        )

        cursor.execute(
            "UPDATE bank_accounts SET balance = balance + %s WHERE id = %s",
            (amount, receiver_id)
        )

        # Transactions
        cursor.execute(
            "INSERT INTO bank_transactions (bank_account_id, balance, date) VALUES (%s, %s, NOW())",
            (sender_id, -amount)
        )

        cursor.execute(
            "INSERT INTO bank_transactions (bank_account_id, balance, date) VALUES (%s, %s, NOW())",
            (receiver_id, amount)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard', username=sender))

    except Exception as e:
        print("ERROR:", e)
        return "Server error (check terminal)"

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)