from db import get_connection
from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

# Home page
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

    return f"""
    <h2>Account Created Successfully</h2>
    <p><b>Username:</b> {username}</p>
    <p><b>Password:</b> {password}</p>
    <p><b>Balance:</b> {balance}</p>
    <a href="/">Go back</a>
    """


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
        "SELECT balance FROM bank_accounts WHERE username = %s",
        (username,)
    )

    balance = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template("dashboard.html", username=username, balance=balance)

@app.route('/send', methods=['POST'])
def send():
    sender = request.form.get("sender")
    receiver = request.form.get("receiver")
    amount = float(request.form.get("amount"))

    conn = get_connection()
    cursor = conn.cursor()

 
    cursor.execute(
        "SELECT balance FROM bank_accounts WHERE username = %s",
        (sender,)
    )
    sender_balance = cursor.fetchone()[0]

    if sender_balance < amount:
        return "Not enough money"


    cursor.execute(
        "SELECT balance FROM bank_accounts WHERE username = %s",
        (receiver,)
    )
    receiver_data = cursor.fetchone()

    if not receiver_data:
        return "Receiver does not exist"


    cursor.execute(
        "UPDATE bank_accounts SET balance = balance - %s WHERE username = %s",
        (amount, sender)
    )

    cursor.execute(
        "UPDATE bank_accounts SET balance = balance + %s WHERE username = %s",
        (amount, receiver)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard', username=sender))

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)