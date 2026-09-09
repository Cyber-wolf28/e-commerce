import tkinter as tk    
from backend.auth_service import AuthService
from PIL import Image, ImageTk
from backend.db import DataBase
from tkinter import messagebox

class RegisterPage:

    BACKGROUND_COLOR_BROWN = "#795548"
    TEXT_COLOR_BEIGE = "#e5c0b3"
    BUTTON_COLOR_CEMENTGREY = "#797778"

    ENTRY_WIDTH = 30

    FONT = ("Segoe UI", 11)
    TITLE_FONT = ("Segoe UI", 40, "bold")


    def __init__(self, root):

        self.root = root
        self.auth = AuthService()

        self.root.title("E-commerce Store")
        self.root.geometry("800x700")

        image = Image.open("Assets/Images/ecommerce.wolf.jpg")
        image = image.resize((100, 100))
        self.logo = ImageTk.PhotoImage(image)


        self.create_widgets()
        
        
    def create_widgets(self):
        self.register_frame = tk.Frame(self.root, 
                                        bg = self.BACKGROUND_COLOR_BROWN,
                                        padx=20, 
                                        pady=20
                                        )

        self.title = tk.Label(
                              self.register_frame,
                              text = "WolfHaus",
                              font = self.TITLE_FONT,
                              bg = self.BACKGROUND_COLOR_BROWN,
                              fg = self.TEXT_COLOR_BEIGE
                              )

        self.logo_label = tk.Label(
                            self.register_frame,
                            image=self.logo,
                            bd = 0
                            )
        self.logo_label.image = self.logo
        
        self.name_label = tk.Label(self.register_frame, text = "Name: ", bg = self.BACKGROUND_COLOR_BROWN)
        self.name_entry = tk.Entry(self.register_frame, width = self.ENTRY_WIDTH)
        self.surname_label = tk.Label(self.register_frame, text = "surname", bg = self.BACKGROUND_COLOR_BROWN)
        self.surname_entry = tk.Entry(self.register_frame, width = self.ENTRY_WIDTH)
        self.username_label = tk.Label(self.register_frame, text="Username: ", bg = self.BACKGROUND_COLOR_BROWN)
        self.username_entry = tk.Entry(self.register_frame, width = self.ENTRY_WIDTH)
        self.email_label = tk.Label(self.register_frame, text="Email: ", bg = self.BACKGROUND_COLOR_BROWN)
        self.email_entry = tk.Entry(self.register_frame, width = self.ENTRY_WIDTH, )
        self.password_label = tk.Label(self.register_frame, text="Password: ", bg = self.BACKGROUND_COLOR_BROWN)
        self.password_entry = tk.Entry(self.register_frame, width = self.ENTRY_WIDTH, show = "*")


        self.register_button = tk.Button(self.register_frame, 
                                text = "Register",
                                command = self.register,
                                cursor = "hand2",
                                bg = self.TEXT_COLOR_BEIGE,
                                )
        
        self.back_button = tk.Button(
                            self.root,
                            text="Back",
                            command=self.go_back,
                            cursor="hand2",
                            width = 5,
                            bg = self.TEXT_COLOR_BEIGE
                            )

        self.back_button.place(x=10, y=10)


        self.title.pack(pady=15)
        self.logo_label.pack(pady = 5)
        self.name_label.pack(pady = 5)
        self.name_entry.pack(pady = 5)
        self.surname_label.pack(pady = 5)
        self.surname_entry.pack(pady = 5)
        self.username_label.pack(pady = 5)
        self.username_entry.pack(pady = 5)
        self.email_label.pack(pady = 5)
        self.email_entry.pack(pady = 5)
        self.password_label.pack(pady = 5)
        self.password_entry.pack(pady = 5)
        
        
        self.register_button.pack(pady = 15 )
        
        self.register_frame.pack(fill="both", expand=True)
        
    def register(self, event = None):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        success = self.auth.register(
                        name,
                        surname,
                        username,
                        email,
                        password
                        )
        if success:
            messagebox.showinfo(
                "Success",
                "Registration Successful")
        else:
            messagebox.showerror(
                "Error",
                "Registration failed")
            
        
            
    def go_back(self):
        from .login import LoginPage

        for widget in self.root.winfo_children():
            widget.destroy()

        LoginPage(self.root)