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