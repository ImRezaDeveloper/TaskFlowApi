from taskflow.app.db.database import get_db

def create_user(username: str, email: str, password: str):
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
               INSERT INTO users (username, email, password_hash)
               VALUES (%s, %s, %s)
               RETURNING id, username, email;
               """, (username, email, password))
    
    user = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    
    return user

def get_user_by_id(user_id: int):
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
               SELECT (id, username, email)
               FROM users
               WHERE id = %s
               """, (user_id))
    
    user = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    
    return user