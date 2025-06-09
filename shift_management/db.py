import sqlite3

def init_db():
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
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

def save_shift(username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO shifts (username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, date, start, scheduled_end, actual_end, hours_worked, overtime, is_vacation))
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