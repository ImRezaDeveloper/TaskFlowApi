import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


def get_db():
    return psycopg2.connect(
        dbname=os.getenv("db_name"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
    )