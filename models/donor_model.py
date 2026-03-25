import sqlite3

DATABASE = "database.db"

def connect_db():
    return sqlite3.connect(DATABASE)

def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()
    return data

def search_by_blood_group(blood_group):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE blood_group=?", (blood_group,))
    data = cursor.fetchall()

    conn.close()
    return data

def get_donated_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE donated=1")
    data = cursor.fetchall()

    conn.close()
    return data