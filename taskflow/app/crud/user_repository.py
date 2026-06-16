from fastapi import Depends, HTTPException
import psycopg2

from taskflow.app.api.dependencies import get_db

def get_users_db(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
    """)

    users = cur.fetchall()
    cur.close()
    # conn.close()

    return users

def verify_exists_user(email: str):
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
        WHERE email = %s
    """, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

def create_user_db(username, email, password_hash, role_ids, conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users(username, email, password_hash)
            VALUES(%s, %s, %s)
            RETURNING id
        """, (username, email, password_hash))
        
        user_id = cur.fetchone()[0]

        for role_id in role_ids:
            cur.execute("""
                INSERT INTO user_roles(user_id, role_id)
                VALUES (%s, %s)
            """, (user_id, role_id))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    
    return user_id


def get_user_by_id(user_id: int, current_user, conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    # conn.close()

    return user

def update_user_db(user_id: int, username: str, email: str):
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

def delete_user_db(user_id: int):
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

def get_user_by_email(email: str, conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
        WHERE email = %s
    """, (email,))

    user = cur.fetchone()

    cur.close()
    # conn.close()

    return user
