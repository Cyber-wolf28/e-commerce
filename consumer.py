from db import get_connection

class GroceryStore:


    def shop(self):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT fruit, price FROM fruits;")
        products = dict(cur.fetchall()) #convert to dictionary
        
        
        consumer_choice = input("What fruits would you like?\n> ").lower().split()
        

        total_cost = 0
        valid_item_found = False

        for fruit in consumer_choice:
            if fruit in products:
                valid_item_found = True
                
                price = products[fruit]
                print(f"{fruit}: R{price}")

                quantity = int(input(f"How many {fruit} would you like?\n> "))

                total_cost += price * quantity

            else:
                print(f"{fruit} is not available.")

        if not valid_item_found:
            print("That is not a valid fruit!\n Please try again")

        print(f"\nYour total is: R{total_cost}")
        
        conn.close()