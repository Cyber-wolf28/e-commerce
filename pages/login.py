import tkinter as tk    
from backend.auth_service import AuthService
from PIL import Image, ImageTk
from pages.register import RegisterPage
from dashboards.admin_dashboard import AdminPage
from tkinter import messagebox

class LoginPage:

    BACKGROUND_COLOR_BROWN = "#795548"
    TEXT_COLOR_BEIGE = "#e5c0b3"
    BUTTON_COLOR_CEMENTGREY = "#797778"

    ENTRY_WIDTH = 30

    FONT = ("Segoe UI", 12)
    TITLE_FONT = ("Segoe UI", 40, "bold")


    

    
    def __init__(self, root):

        self.root = root
        self.auth = AuthService()

        self.root.title("E-commerce Store")
        self.root.geometry("800x600")

        image = Image.open("Assets/Images/ecommerce.wolf.jpg")
        image = image.resize((100, 100))
        self.logo = ImageTk.PhotoImage(image)

        self.create_widgets()
        
        self.root.bind("<Return>", self.login)
        
        
    def create_widgets(self):
        self.login_frame = tk.Frame(self.root, 
                                    bg = self.BACKGROUND_COLOR_BROWN,
                                    padx=20, 
                                    pady=20
                                    )

        self.title = tk.Label(
                              self.login_frame,
                              text = "WolfHaus",
                              font = self.TITLE_FONT,
                              bg = self.BACKGROUND_COLOR_BROWN,
                              fg = self.TEXT_COLOR_BEIGE
                              )

        self.logo_label = tk.Label(
                             self.login_frame,
                             image = self.logo,
                             bg = self.BACKGROUND_COLOR_BROWN
                             )
        
        self.username_label = tk.Label(self.login_frame, text="Username: ", bg = self.BACKGROUND_COLOR_BROWN, font = self.FONT)
        self.username_entry = tk.Entry(self.login_frame, width = self.ENTRY_WIDTH)
        self.password_label = tk.Label(self.login_frame, text="Password: ", bg = self.BACKGROUND_COLOR_BROWN, font = self.FONT)
        self.password_entry = tk.Entry(self.login_frame, width = self.ENTRY_WIDTH, show ="*")

        self.register_label = tk.Label(self.login_frame, 
                            text = "Don't have an account?",
                            relief = "flat",
                            borderwidth = 0,
                            highlightthickness = 0,
                            bg = self.BACKGROUND_COLOR_BROWN,
                            )
        self.register_button = tk.Button(self.login_frame, 
                                text = "Register",
                                command = self.open_register_page,
                                cursor = "hand2",
                                bg = self.TEXT_COLOR_BEIGE,
                                )

        self.login_button = tk.Button(self.login_frame, 
                                text = "Login", 
                                command = self.login, 
                                cursor = "hand2", 
                                bg = self.TEXT_COLOR_BEIGE,
                                )

        self.title.pack(pady=15)
        self.logo_label.pack(pady = 5)
        self.username_label.pack(pady = 5)
        self.username_entry.pack(pady = 5)
        self.password_label.pack(pady = 5)
        self.password_entry.pack(pady = 5)
        self.login_button.pack(pady = 5 )
        
        
        self.register_label.pack(pady = (30, 5))
        self.register_button.pack(pady = 5)
        
        self.login_frame.pack(fill="both", expand=True)
        
    def login(self, event = None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
            
        role = self.auth.login(
            username,
            password
            )
            
        if role:
            self.login_frame.destroy()
            AdminPage(self.root, role)
        else:
            messagebox.showerror
            ("Login failed",
             "Invalid Credentials")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
        
    def open_register_page(self):
        self.login_frame.destroy()
        
        RegisterPage(self.root)