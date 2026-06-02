import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return psycopg2.connect(
        dbname=os.getenv("db_name"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=os.getenv("port"),
        host=os.getenv("host", "localhost")
    )