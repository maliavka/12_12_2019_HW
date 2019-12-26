import sqlite3


def exec_query(query):
    conn = sqlite3.connect('./chinook.db')
    cur = conn.cursor()
    cur.execute(query)
    record = cur.fetchall()
    return record
