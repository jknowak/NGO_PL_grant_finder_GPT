import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # minimum number of connections
    20,  # maximum number of connections
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


def get_db_connection():
    return connection_pool.getconn()

def release_db_connection(conn):
    connection_pool.putconn(conn)

def execute_query(query, params=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        release_db_connection(conn)