from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/app/database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT, ip TEXT)''')
    conn.commit()
    conn.close()

def update_corefile():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    records = c.execute('SELECT domain, ip FROM records').fetchall()
    conn.close()

    content = ".:53 {\n    hosts {\n"
    for domain, ip in records:
        content += f"        {ip} {domain}\n"
    content += "    }\n    forward . 8.8.8.8 8.8.4.4\n    log\n    errors\n}\n"

    with open("/Corefile", "w") as f:
        f.write(content)

    os.system("kill -SIGUSR1 1")

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    records = c.execute('SELECT * FROM records').fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add():
    domain = request.form['domain']
    ip = request.form['ip']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO records (domain, ip) VALUES (?, ?)', (domain, ip))
    conn.commit()
    conn.close()
    update_corefile()
    return redirect(url_for('index'))

@app.route('/delete/<int:record_id>')
def delete(record_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM records WHERE id=?', (record_id,))
    conn.commit()
    conn.close()
    update_corefile()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)