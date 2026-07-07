from consumer import GroceryStore
from admin import Admin


class MainStore:
# -------- MAIN PROGRAM --------     
        role = input("Are you a consumer, admin or new user?\n> ").lower().strip()
            
            
        store = GroceryStore()
        admin = Admin()

        if role == "consumer":
            store.shop()
            

        elif role == "admin":
            admin.login()
            
            
        elif role == "new user":
            admin.register()
            
            
        else:
            print("Not a valid response!")