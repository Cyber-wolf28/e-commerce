import tkinter as tk
from backend.auth_service import AuthService
from backend.db import DataBase
from tkinter import messagebox

class AddUsers:
    FONT = ("Segoe UI", 13)
    ENTRY_WIDTH = 40
    BG_COLOR_BEIGE = "#e5c0b3"
    
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.db = DataBase()
        self.build_page()
        
    def create_field(self, text, row, show = None):
            label = tk.Label(
                self.form_frame,
                text=text,
                font = self.FONT,
                bg = self.BG_COLOR_BEIGE
            )
    
            label.grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=5
            )
    
            entry = tk.Entry(self.form_frame, width = self.ENTRY_WIDTH, show = show)
    
            entry.grid(
                row=row,
                column=1,
                padx=10,
                pady=5
            )
    
            return entry
        
    def build_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.form_frame = tk.Frame(
                                    self.content_frame,
                                    bg = self.BG_COLOR_BEIGE
                                    )

        self.name_entry = self.create_field("Name: ", 0)
        self.surname_entry = self.create_field("Surname: ", 1)
        self.username_entry = self.create_field("Username: ", 2)
        self.role_entry = self.create_field("Role: ", 3)
        self.email_entry = self.create_field("Email: ", 4)
        self.password_entry = self.create_field("Password: ", 5, show = "*")
        

        self.add_button = tk.Button(
                                    self.form_frame,
                                    text = "Save",
                                    command = self.add_user
                                    )
        
        self.form_frame.pack(anchor = "nw", padx = 20, pady = 20)
        self.add_button.grid(row=6, column=1, sticky="w", padx=5, pady=10)
        
    def add_user(self):
            
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        username = self.username_entry.get().strip()
        role = self.role_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
           
        if not all([name, surname, username, role, email, password]):
                    messagebox.showerror("Error", "Please complete all fields.")
                    return   
         
        success = self.db.add_user(
                                name,
                                surname,
                                username,
                                role,
                                email,
                                password
                                )
        if success:
            self.name_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.role_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        if success:    
            messagebox.showinfo("Success", "User added successfully!")
        else:
            messagebox.showerror("Error", "Could not add user")