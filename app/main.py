from flask import Flask, render_template, redirect, request, session, url_for
from auth import login_required, login_user, logout_user
from db import init_db, get_zones, add_zone, delete_zone, get_logs
from utils import backup_database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if login_user(request.form['username'], request.form['password']):
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    zones = get_zones()
    return render_template('dashboard.html', zones=zones)

@app.route('/add_zone', methods=['POST'])
@login_required
def add_zone_route():
    domain = request.form['domain']
    ip = request.form['ip']
    record_type = request.form['type']
    add_zone(domain, ip, record_type)
    return redirect('/dashboard')

@app.route('/delete_zone/<int:zone_id>')
@login_required
def delete_zone_route(zone_id):
    delete_zone(zone_id)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/logs')
@login_required
def view_logs():
    logs = get_logs()
    return render_template('logs.html', logs=logs)

if __name__ == "__main__":
    init_db()
    backup_database()
    app.run(host='0.0.0.0', port=5000)
