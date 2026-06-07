import psycopg2

from taskflow.app.db.db import get_db

def get_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
    """)

    users = cur.fetchall()
    cur.close()
    conn.close()

    return users

def create_user(username: str, email: str, password_hash: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email
    """, (username, email, password_hash))

    user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return user

def get_user_by_id(user_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

def update_user(user_id: int, username: str, email: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET username = %s,
            email = %s
        WHERE id = %s
        RETURNING id, username, email
    """, (username, email, user_id))

    user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return user

def delete_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE id = %s
        RETURNING id
    """, (user_id,))

    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return deleted