from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ----------------- DATABASE SETUP -----------------
def init_db():
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wellness (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    last_period TEXT,
                    cycle_length INTEGER,
                    water_glasses INTEGER,
                    mood TEXT,
                    sleep_hours INTEGER
                )''')
    conn.commit()
    conn.close()

init_db()

# ----------------- ROUTES -----------------
@app.route('/')
def home():
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM wellness ORDER BY id DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_period = request.form.get('lastPeriod')
    cycle_length = request.form.get('cycleLength')
    water_glasses = request.form.get('glasses')
    mood = request.form.get('mood')
    sleep_hours = request.form.get('sleepHours')

    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('''INSERT INTO wellness (date, last_period, cycle_length, water_glasses, mood, sleep_hours)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (date, last_period, cycle_length, water_glasses, mood, sleep_hours))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
