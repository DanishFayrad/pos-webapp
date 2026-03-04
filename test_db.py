import os
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

import psycopg2

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")  # Simple test query
    print("Database connection successful:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("Database connection failed!")
    print(e)