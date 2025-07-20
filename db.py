import sqlite3
import hashlib

DB_NAME = 'url_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE,
            visits INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def insert_url(long_url):
    short_code = hashlib.md5(long_url.encode()).hexdigest()[:6]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM urls WHERE long_url = ?', (long_url,))
    result = cursor.fetchone()
    if result:
        return result[2]  # existing short_code

    cursor.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    conn.commit()
    conn.close()
    return short_code

def get_long_url(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def increment_visit(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE urls SET visits = visits + 1 WHERE short_code = ?', (short_code,))
    conn.commit()
    conn.close()

def get_visits(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT visits FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def save_to_db(long_url, short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    conn.commit()
    conn.close()
