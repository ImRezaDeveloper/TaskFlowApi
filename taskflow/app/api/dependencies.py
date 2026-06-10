from typing import Generator
from taskflow.app.db.database import db_pool

def get_db() -> Generator:
    connection = None
    try:
        # Rent a connection from the pool
        connection = db_pool.getconn()
        yield connection  # Pass the connection to your endpoint code
    finally:
        if connection:
            # ALWAYS put the connection back into the pool when the request ends
            db_pool.putconn(connection)