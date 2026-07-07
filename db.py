import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DataBase:
    
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
            )
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            return None