from db import get_connection
import bcrypt


class Admin:
    
    
    def register(self):
        create_name = input("What is your name? ").strip()
        if self.navigate(create_name):
            return
        create_username = input("Create a username: ").strip()
        if self.navigate(create_username):
            return
        create_password = input("Create a password: ").strip()
        if self.navigate(create_password):
            return
        create_role = input("what is your role? ").strip().lower()
        if self.navigate(create_role):
            return
        create_email = input("what is your email address: ").strip()
        if self.navigate(create_email):
            return
        
        allowed_role = ["worker", "manager"]
        
        if create_role not in allowed_role:
            print("Invalid role")
            return
            
        
        hashed_password = self.hash_password(create_password)
        
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO users_admin (name, username, password, role, email) VALUES (%s, %s, %s, %s, %s)",
            (create_name, create_username, hashed_password, create_role, create_email,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
            
        print(f"{create_role} Registered successful!")
        print("Please wait for superuser to approve")
        
            
    
    def login(self):
        attempts = 0
        
        while attempts < 3:
            username = input("Username:\n> ").strip()
            if self.navigate(username):
                return
            password = input("Password:\n> ").strip()
            if self.navigate(password):
                return
            conn = get_connection()
            cur = conn.cursor()
        

            cur.execute(
                "SELECT username, password, name, role, status FROM users_admin WHERE username = %s",
                (username,)
                )
        
        
            user = cur.fetchone()
        
        
            cur.close()
            conn.close()
        

            if user is None:
                attempts += 1
                print(f"invalid credentials! you have {3 - attempts} attempts remaining")
                continue
        
            db_username, db_password, name, role, status = user
        
        
            if not self.verify_password(password, db_password):
                attempts += 1
                print(f"invalid credentials! You have {3 - attempts} attempts remaining.")
                continue
        

            if status == "pending":
                print("Your account is waiting for approval")
                return
        
            if status == "denied":
                print("Access denied")
                return
        
            if status != "approved":
                print(f"access blocked, Status: {status}")
                return
            
            
            #Role based access
            if role == "superuser":
                print(f"Welcome {name}😊")
                self.superuser_menu()
                return
            elif role == "manager":
                print(f"Welcome {name}😊")
                self.manager_menu()
                return
            elif role == "worker":
                print(f"Welcome {name}😊")
                self.worker_menu()
                return
            else:
                print("Please try again")
                return
    
        
    def hash_password(self, password):
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")
            

    def verify_password(self, password, stored_hash):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8")
        )
        
        
    def superuser_menu(self):
        while True:
            print("""1.View products \n2.Add products \n3.Delete products \n4.View pending users \n5.Accept user \n6.Deny user \n7.Delete user \n8.Back
                    """)
            superuser_choice = input("> ").strip().lower()
            result = self.navigate(superuser_choice)
            if result == "main menu":
                return
            if result == "back":
                return
            if result == "exit":
                return
                exit()
            if superuser_choice in ["1", "view products"]:
                self.view_products()
            elif superuser_choice in ["2", "add products"]:
                self.add_products()
            elif superuser_choice in ["3", "delete products"]:
                self.delete_products()
            elif superuser_choice in ["4", "view pending users"]:
                self.view_pending_users()
            elif superuser_choice in ["5", "accept users"]:
                self.approve_user()
            elif superuser_choice in ["6", "deny users"]:
                self.deny_user()
            elif superuser_choice in ["7", "delete user"]:
                self.delete_user()
            elif superuser_choice in ["8", "back"]:
                self.navigate(superuser_choice)
            else:
                print("please type an option!")
            
            
    def manager_menu(self):
        while True:
            print("""1.view products \n2.add products \n3.delete products \n4.view pending users \n5.main menu
                    """)
            manager_choice = input("> ").strip().lower()
            result = self.navigate(manager_choice)
            if result == "main menu":
                return
            if result == "back":
                return
            if result == "exit":
                return
                exit()
            if manager_choice in ["1", "view products"]:
                self.view_products()
            elif manager_choice in ["2", "add products"]:
                self.add_products()
            elif manager_choice in ["3", "delete products"]:
                self.delete_products()
            elif manager_choice in ["4", "view pending users"]:
                self.view_pending_users()
            elif result in ["main menu"]:
                return
            else:
                print("Invalid option")
        
        
    def worker_menu(self):
        while True:
            print("""1.view products \n2.add products \n3.delete products \n4.main menu
                  """)
            worker_choice = input("> ").strip().lower()
            result = self.navigate(worker_choice)
            if result == "main menu":
                return
            if result == "back":
                return
            if result == "exit":
                return
                exit()
            if worker_choice in ["1", "view products"]:
                self.view_products()
            elif worker_choice in ["2", "add products"]:
                self.add_products()
            elif worker_choice in ["3", "delete products"]:
                self.delete_products()
            elif result == "main menu":
                return
            else:
                print("Invalid option!")
        

    def view_products(self):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM fruits")
        
        rows = cur.fetchall()
        
        for row in rows:
            print(f"fruit: {row[0]} - price: {row[1]} - id: {row[2]}")
            
        cur.close()
        conn.close()
        
        
    def add_products(self):
        products = input("what is the name of the product: ")
        if self.navigate(products):
            return
        if not products:
            print("product cannot be empty")
            return
        
        price = input("what is the price of the product: ")
        if self.navigate(price):
            return
        try:
            price = float(price)
        except ValueError:
                print("Invalid price")
                return
        
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO fruits (fruit, price) VALUES (%s, %s)",
            (products, price,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("product added successfully")
        
    def delete_products(self):
        product_id = input("Enter the product id to delete: ")
        if self.navigate(product_id):
            return
        try:
            product_id = int(product_id)
        except ValueError:
            print("Invalid product ID")
            return
        
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT fruit FROM fruits WHERE id = %s",
                    (product_id,))
        
        fruit = cur.fetchone()
        
        if fruit is None:
            print("product not found")
            cur.close()
            conn.close()
            return
            
        
        delete_fruit = input(f"are you sure you want to delete {fruit[0]} y/n? \n>").strip().lower()
        
        if delete_fruit not in ["y", "yes"]:
            return
        
        
        cur.execute(
            "DELETE FROM fruits WHERE id = %s",
            (product_id,)
            )
        
        conn.commit()
        
        if cur.rowcount > 0:
            print("Deleted successfully")
        else:
            print("Product not found")
            
        cur.close()
        conn.close()
        
        
    def approve_user(self):
        
        admin_id = input("type the user id to confirm approval: ")
        if self.navigate(admin_id):
            return
        try:
            admin_id = int(admin_id)
        except ValueError:
            print("approval canceled")
            return
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE users_admin SET status = 'approved' WHERE admin_id = %s",
            (admin_id,)
            )
        conn.commit()
        
        if cur.rowcount > 0:
            print("user approved!")
        else:
            print("user not found")
            
        cur.close()
        conn.close()
        
    def deny_user(self):
        conn = None
        cur = None
        
        admin_id = input("Enter the user id: ")
        if self.navigate(admin_id):
            return
        try:
            admin_id = int(admin_id)
        except ValueError:
            print("Invalid user ID!")
            return
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute(
                "SELECT username, name, role FROM users_admin WHERE admin_id = %s",
                (admin_id,)
            )
            
            users = cur.fetchone()
            
            if not users:
                print("User ID not found")
                return
                
            print(f"""
                Username: {users[0]}
                Name: {users[1]}
                Role: {users[2]}
                """)
            
            if users[2] == "superuser":
                print("Superuser account cannot be denied.")
                return
                
            confirm = input(
                f"are you sure you want to deny {users[1]} y/n?"
                ).strip().lower()
            
            if confirm not in ["y", "yes"]:
                print("user status is still pending")
                return
            

            cur.execute(
                "UPDATE users_admin SET status = 'denied' WHERE admin_id = %s",
                (admin_id,)
            )
            
            conn.commit()
            
            if cur.rowcount > 0:
                print("User denied")
            else:
                print("User id not found!")
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
    def view_pending_users(self):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT admin_id, name, username, role, email, status FROM users_admin WHERE status = 'pending' ")
        
        users = cur.fetchall()
        
        for user in users:
            print(f"ID:{user[0]} | Name:{user[1]} | Username:{user[2]} | Role:{user[3]} | email:{user[4]} | status:{user[5]}")
        
        cur.close()
        conn.close()
        
    
    def delete_user(self):
        conn = None
        cur = None
        
        admin_id = input("enter user id to delete: ")
        if self.navigate(admin_id):
            return
        try:
            admin_id = int(admin_id)
        except ValueError:
            print("Please use a valid id")
            return
        
        try:
            conn = get_connection()
            cur = conn.cursor()
        
            cur.execute("SELECT username, name, role FROM users_admin WHERE admin_id = %s",
                        (admin_id,)
                        )
        
            user = cur.fetchone()
        
            if user is None:
                print("User ID not found!")
                return
            print(f"""
                    Username: {user[0]}
                    Name: {user[1]}
                    Role: {user[2]}
                    """)
        
            confirm = input(f"are you sure you want to delete {user[1]}? (y/n)").strip().lower()
        
            if confirm not in ["y", "yes"]:
                print("Delete canceled.")
                return
                

            cur.execute(
            "DELETE FROM users_admin WHERE admin_id = %s",
            (admin_id,)
            )
        
            conn.commit()
            
            if cur.rowcount > 0:
                print("User deleted!")
            else:
                print("User ID not found!")
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
                
    
    def navigate(self, value):
        value = value.strip().lower()

        if value in ["back"]:
            return "back"

        if value in ["main menu"]:
            return "main menu"

        if value in ["exit"]:
            return "exit"

        return None

    
