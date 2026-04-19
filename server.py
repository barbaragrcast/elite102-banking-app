from db import get_connection
from flask import Flask, render_template, request, redirect
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
        "INSERT INTO accounts (username, password, balance) VALUES (%s, %s, %s)",
        (username, password, balance)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE username = %s AND password = %s",
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return f"Welcome {username}"
    else:
        return "Invalid username or password"
    
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)