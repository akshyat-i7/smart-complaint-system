from flask import Flask, render_template, request, redirect, session
import sqlite3
from model import predict_priority

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("complaint.db")

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        if user == "admin" and pwd == "admin":
            session['user'] = user
            return redirect('/dashboard')
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# HOME REDIRECT
@app.route('/')
def home():
    return redirect('/login')

# ADD COMPLAINT
@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    title = request.form['title']
    desc = request.form['description']

    priority = predict_priority(desc)

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        priority TEXT,
        status TEXT
    )
    """)

    cur.execute("INSERT INTO complaints (title, description, priority, status) VALUES (?, ?, ?, ?)",
                (title, desc, priority, "Pending"))

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM complaints")
    data = cur.fetchall()
    conn.close()

    return render_template("dashboard.html", data=data)

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)