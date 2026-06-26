from fastapi import Depends
from sqlalchemy import select
from taskflow.app.db.database import get_db
from taskflow.app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

def get_users_db(db: AsyncSession = Depends(get_db)):
    query = select(User)
    result = db.execute(query)
    tasks = result.scalars().all()
    
    return tasks

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

def create_user_db(username, email, hashed_password, full_name, is_active, is_verified, get_db: AsyncSession = Depends(get_db)):

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_active=is_active,
        is_verified=is_verified
    )
    
    get_db.add(new_user)
    get_db.commit()
    
    return new_user

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

def get_user_by_email(email: str, get_db):
    cur = get_db.cursor()

    cur.execute("""
        SELECT id, username, email
        FROM users
        WHERE email = %s
    """, (email,))

    user = cur.fetchone()

    cur.close()
    # conn.close()

    return user
