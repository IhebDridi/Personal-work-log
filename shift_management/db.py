import sqlite3

import sqlite3

def init_db():
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            start TEXT,
            scheduled_end TEXT,
            actual_end TEXT,
            hours_worked REAL,
            overtime REAL,
            is_vacation INTEGER DEFAULT 0,
            is_unpaid_vacation INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            username TEXT PRIMARY KEY,
            default_start TEXT,
            default_end TEXT,
            time_mode TEXT,
            vacation_days INTEGER DEFAULT 20
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password_hash):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def get_password_hash(username):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def user_exists(username):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE username=?', (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_shift(username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, is_unpaid_vacation):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO shifts (
            username, date, start, scheduled_end, actual_end,
            hours_worked, overtime, is_vacation, is_unpaid_vacation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, is_unpaid_vacation))
    conn.commit()
    conn.close()

def update_shift(shift_id, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        UPDATE shifts SET date=?, start=?, scheduled_end=?, actual_end=?, hours_worked=?, overtime=?, is_vacation=?
        WHERE id=?
    ''', (date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, shift_id))
    conn.commit()
    conn.close()

def get_user_shifts(username):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation, is_unpaid_vacation
        FROM shifts
        WHERE username=?
        ORDER BY date DESC
    ''', (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_shift_by_id(shift_id):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('SELECT id, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation FROM shifts WHERE id=?', (shift_id,))
    row = c.fetchone()
    conn.close()
    return row

def remove_user_fully(username):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    # Remove all user data from all related tables
    c.execute('DELETE FROM users WHERE username=?', (username,))
    c.execute('DELETE FROM shifts WHERE username=?', (username,))
    c.execute('DELETE FROM user_settings WHERE username=?', (username,))
    conn.commit()
    conn.close()