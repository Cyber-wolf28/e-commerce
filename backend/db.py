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
        
        
    @staticmethod  
    def get_user(username):
        connection = DataBase.get_connection()
            
        if connection is None:
            return None
            
        try:
            cursor = connection.cursor()
            

            cursor.execute(
                        """SELECT id, name, surname, username, role, email, password
                        FROM users_admin 
                        WHERE username = %s""",
                        (username,)
                        )
            
            
            user = cursor.fetchone()
            
            return user
        
        finally: 
            cursor.close()
            connection.close()
            
            
        
        
    @staticmethod
    def add_user(name, surname, username, role, email, hashed_password):
        connection = DataBase.get_connection()
        
        if connection is None:
            return None
        try:
            cursor = connection.cursor()
        
            cursor.execute(
                 """
                 INSERT INTO users_admin (name, surname, username, role, email, password) 
                 VALUES (%s, %s, %s, %s, %s, %s)
                 """,
                (name, surname, username, role, email, hashed_password)
                )
            connection.commit()
            return True
        
        except Exception as e:
            if connection:
                connection.rollback()
                print(f"Error: {e}")
                return False
                
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod     
    def add_product(fruit, price, stock, image_path):
        connection = None
        cursor = None
        
        try:
            connection = DataBase.get_connection()
            cursor = connection.cursor()
        
            cursor.execute(
                """INSERT INTO fruits (fruit, price, stock, image_path)
                VALUES (%s, %s, %s, %s)
                """,
                (fruit, price, stock, image_path)
                )
        
            connection.commit()
            return True
        except Exception as e:
             if connection:
                connection.rollback()
                
                print(f"Error: {e}")
                return False
            
        finally:
            if cursor:
                cursor.close()
                
            if connection:
                connection.close()
                
    @staticmethod          
    def get_all_products():
        connection = None
        cursor = None
        try:
            connection = DataBase.get_connection()
            cursor = connection.cursor()
        
            cursor.execute("""SELECT fruit, price, id, stock, date, time FROM fruits""")
            
            rows = cursor.fetchall()
            return rows
        
        except Exception as e:
            print(f"Error: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
           
    @staticmethod
    def update_product(product_id, column_name, new_value):
        
        allowed_columns = {
            "Fruit": "fruit",
            "Price": "price",
            "Stock":  "stock"
        }
        
        if column_name not in allowed_columns:
            return False
        
        database_column = allowed_columns[column_name]
        
        conn = DataBase.get_connection()
        
        try:
            cursor = conn.cursor()
            
            query = f"""
                    UPDATE fruits
                    SET {database_column} = %s
                    WHERE id = %s
                    """
                    
            cursor.execute(
                query,
                (new_value, product_id)
            )
            
            conn.commit()
            
            return True
        
        except Exception as error:
            conn.rollback()
            print("Database error:", error)
            return False
        
        finally:
            cursor.close()
            conn.close()