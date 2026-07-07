import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="products",
        user="postgres",
        password="admin",
        port=5432
    )