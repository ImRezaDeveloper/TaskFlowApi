import psycopg2, os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

conn = psycopg2.connect(
    f"dbname={os.getenv("db_name")} user={os.getenv("user")} password={os.getenv("password")} port={os.getenv("port")}"
)

cur = conn.cursor()

cur.execute("select * from users")

print(cur.fetchall())

conn.close()