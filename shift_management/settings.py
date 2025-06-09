import sqlite3

def get_user_settings(username):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('SELECT default_start, default_end, time_mode, vacation_days FROM user_settings WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'default_start': row[0], 'default_end': row[1], 'time_mode': row[2], 'vacation_days': row[3] if row[3] is not None else 20}
    else:
        return None

def set_user_settings(username, default_start, default_end, time_mode, vacation_days):
    conn = sqlite3.connect('worklogs.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_settings (username, default_start, default_end, time_mode, vacation_days)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET default_start=excluded.default_start, default_end=excluded.default_end, time_mode=excluded.time_mode, vacation_days=excluded.vacation_days
    ''', (username, default_start, default_end, time_mode, vacation_days))
    conn.commit()
    conn.close()