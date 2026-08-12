import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port="5433",
        dbname="postgres",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )