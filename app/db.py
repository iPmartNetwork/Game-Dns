import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS zones (id INTEGER PRIMARY KEY, domain TEXT, ip TEXT, type TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, user TEXT, action TEXT, timestamp TEXT)')
    cur.execute('INSERT OR IGNORE INTO users (id, username, password) VALUES (1, "admin", "admin123")')
    conn.commit()
    conn.close()

def get_zones():
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM zones')
    zones = cur.fetchall()
    conn.close()
    return zones

def add_zone(domain, ip, record_type):
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO zones (domain, ip, type) VALUES (?, ?, ?)', (domain, ip, record_type))
    cur.execute('INSERT INTO logs (user, action, timestamp) VALUES (?, ?, ?)', ("admin", f"Added {domain} {record_type}", datetime.datetime.now()))
    conn.commit()
    conn.close()

def delete_zone(zone_id):
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM zones WHERE id=?', (zone_id,))
    cur.execute('INSERT INTO logs (user, action, timestamp) VALUES (?, ?, ?)', ("admin", f"Deleted zone {zone_id}", datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect('/app/database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM logs')
    logs = cur.fetchall()
    conn.close()
    return logs
