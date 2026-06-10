import sys
import psycopg2
from psycopg2 import pool
from taskflow.app.core.config import settings

try:
    # Initialize a global connection pool
    db_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,   # Minimum connections to keep alive
        maxconn=10,  # Maximum connections to scale up to under heavy load
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
    )
    print("🚀 Database connection pool created successfully, bro!")
except Exception as e:
    print(f"❌ Error creating PostgreSQL connection pool: {e}")
    sys.exit(1)