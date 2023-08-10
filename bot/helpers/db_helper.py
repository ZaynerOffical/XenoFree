import sqlite3

import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "database",
                             "database.db")

def is_prohibited(user_id: int) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def add_user_to_blacklist(user_id: int) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM blacklist")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result is not None else 0


def remove_user_from_blacklist(user_id: int) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM blacklist")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result is not None else 0


def get_all_blacklisted_users() -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM blacklist")
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]


def clear_blacklist() -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklist")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM blacklist")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result is not None else 0
