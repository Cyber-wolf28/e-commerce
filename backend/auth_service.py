import bcrypt
from .db import DataBase


class AuthService:
    
    def register(self, name, surname, username, email, password):
        
        role = "consumer"
        
        hashed_password = self.hash_password(password)
        
        DataBase.add_user(name, 
                          surname,
                          username,
                          role,
                          email,  
                          hashed_password)
            
        return True
      
    
    def login(self, username, password):
        
        user = DataBase.get_user(username)
        
        if user is None:
            return False
        
        id, name, surname, db_username, role, email, db_password = user
        

        if not self.verify_password(password, db_password):
            return False
            
        return role
    
            
    
    @staticmethod  
    def hash_password(password):
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")
            
    @staticmethod
    def verify_password(password, stored_hash):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8")
        )