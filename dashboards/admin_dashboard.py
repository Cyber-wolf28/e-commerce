import tkinter as tk
from backend.auth_service import AuthService
from PIL import Image, ImageTk
from backend.db import DataBase
from tkinter import messagebox
from tkinter_pages.admin.add_products import AddProducts
from tkinter_pages.admin.view_products import ViewProducts
from tkinter_pages.admin.add_users import AddUsers
from tkinter_pages.admin.view_users import ViewUsers
from pathlib import Path

class AdminPage:
    

    BACKGROUND_COLOR_BROWN = "#795548"
    TEXT_COLOR_BEIGE = "#e5c0b3"
    CONTENT_PAGE_GREY = "#797778"

    ENTRY_WIDTH = 30
    BUTTON_WIDTH = 20
    BUTTON_PADDING = 10
    
    FONT = ("Segoe UI", 11)
    TITLE_FONT = ("Segoe UI", 40, "bold")


    def __init__(self, root, role, show_login_callback):
        
        self.menu_centered = True
        self.animation_running = False
        self.root = root
        self.role = role
        self.show_login_callback = show_login_callback
        self.auth = AuthService()
        

        self.root.title("E-commerce Store")
        self.root.geometry("800x700")
        self.root.minsize(800, 700)

        image = Image.open("Assets/Images/ecommerce.wolf.jpg")
        image = image.resize((100, 100))
        self.logo = ImageTk.PhotoImage(image)
        
        self.add_products_icon = self.load_icon("add_products.png")
        self.add_users_icon = self.load_icon("add_user.png")
        self.delete_products_icon = self.load_icon("delete_products.png")
        self.delete_users_icon = self.load_icon("delete_user.png")
        self.view_products_icon = self.load_icon("view_products.png")
        self.view_users_icon = self.load_icon("view_users.png")


        self.create_widgets()
        self.load_dashboard()

        self.place_widgets()
        
        self.root.bind("<Configure>", self.on_resize)
        self.root.update_idletasks()

        
    def create_widgets(self):
        self.body_frame()
        self.header_frame()

        
    def header_frame(self):

        self.title = tk.Label(
            self.admin_frame,
            text="WolfHaus",
            font=self.TITLE_FONT,
            bg=self.BACKGROUND_COLOR_BROWN,
            fg=self.TEXT_COLOR_BEIGE
        )

        self.title.pack(pady=20)

        self.logo_label = tk.Label(
            self.menu_frame,
            image=self.logo,
            bd=0,
            bg=self.BACKGROUND_COLOR_BROWN
        )

        self.logo_label.image = self.logo
            
    def body_frame(self):
        

        self.admin_frame = tk.Frame(
                                    self.root,
                                    bg=self.BACKGROUND_COLOR_BROWN
                                    )

        self.admin_frame.pack(fill="both", expand=True)

        self.back_button = tk.Button(
                                    self.admin_frame,
                                    text = "Back",
                                    command = self.go_back,
                                    cursor = "hand2",
                                    bg = self.TEXT_COLOR_BEIGE
                                    )

        self.back_button.place(x=10, y=10)
        self.back_button.lift()
        
        
        self.menu_frame = tk.Frame(
                                    self.admin_frame,
                                    bg=self.BACKGROUND_COLOR_BROWN
                                  )
        
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = tk.Frame(
                                    self.admin_frame,
                                    bg = self.TEXT_COLOR_BEIGE,
                                    highlightthickness=1,
                                    highlightbackground="#C0C0C0"
                                    )
        

    def place_widgets(self):

        # Menu starts in the middle
        self.root.update_idletasks()

        menu_width = 300
        menu_height = self.menu_frame.winfo_reqheight()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        menu_x = (window_width // 2) - (menu_width // 2)
        menu_y = (window_height - menu_height) // 2

        self.menu_frame.place(
                            x=menu_x,
                            y=menu_y,
                            width=menu_width,
                            )
        self.root.update_idletasks()

        self.menu_x = self.menu_frame.winfo_x()
        self.menu_y = self.menu_frame.winfo_y()
        

        self.content_frame.place_forget()
                                
         

    def show_page(self, page):

        # Don't animate twice
        if self.menu_centered:
            
            self.menu_centered = False
            self.animation_running = True

            self.content_frame.place(
                x=self.root.winfo_width(),
                y=120,
                width=self.root.winfo_width() - 310,
                height=self.root.winfo_height() - 130
            )

            self.page_to_load = page
            self.animate_dashboard()
        
        else:
            page(self.content_frame)
        
    def animate_dashboard(self):
        self.root.update_idletasks()
        
        menu_target_x = 125
        menu_width = 300
        spacing = 20
        
        panel_target_x = menu_target_x + menu_width + spacing 

        menu_speed = 3
        panel_speed = 6

        menu_x = self.menu_frame.winfo_x()
        panel_x = self.content_frame.winfo_x()

        finished = True

        if menu_x > menu_target_x:

            menu_x -= menu_speed

            if menu_x < menu_target_x:
                menu_x = menu_target_x

            self.menu_frame.place(
                x=menu_x,
                y=self.menu_y,
                width=menu_width,
                height=self.menu_frame.winfo_reqheight()
            )

            finished = False

        if panel_x > panel_target_x:

            panel_x -= panel_speed

            if panel_x < panel_target_x:
                panel_x = panel_target_x

            self.content_frame.place(
                x=panel_x,
                y=120,
                width=self.root.winfo_width() - panel_target_x - 20,
                height=self.root.winfo_height() - 130
            )

            finished = False

        if not finished:
            self.root.after(15, self.animate_dashboard)
        else:
            self.animation_running = False
            self.page_to_load(self.content_frame)
            
            
    def add_hover(self, button):
        button.bind(
                    "<Enter>",
                    lambda event: button.config(bg="#9C7A6B")
                    )

        button.bind(
                    "<Leave>",
                    lambda event: button.config(bg=self.TEXT_COLOR_BEIGE)
                    )
        
        
    def on_resize(self, event):

    # Don't interfere while the animation is running
        if self.animation_running:
            return

        self.root.update_idletasks()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        if self.menu_centered:

            menu_width = 300

            menu_x = (window_width - menu_width) // 2
            menu_y = (window_height - self.menu_frame.winfo_reqheight()) // 2

            self.menu_frame.place(
                x=menu_x,
                y=menu_y,
                width=menu_width
            )

            self.menu_x = menu_x
            self.menu_y = menu_y

        else:
            # Keep the menu where it finished animating
            menu_target_x = 125
            menu_width = 300
            spacing = 20

            panel_target_x = menu_target_x + menu_width + spacing

            self.menu_frame.place(
                x=menu_target_x,
                y=self.menu_y,
                width=menu_width
            )

            self.content_frame.place(
                x=panel_target_x,
                y=120,
                width=window_width - panel_target_x - 20,
                height=window_height - 130
            )
            
            
    def load_icon(self, filename, size=(20, 20)):
        
        icon_path = Path("Assets") / "Icons" / filename
        
        image = Image.open(icon_path)
        image = image.resize(size)
        
        return ImageTk.PhotoImage(image)
        
        
    def superuser_dashboard(self):
        self.logo_label.grid(
                            row=0,
                            column=0,
                            pady=(20, 30)
                            )
        self.create_common_menu()
        self.view_products.grid(row = 1, column = 0, pady = self.BUTTON_PADDING)
        self.add_products.grid(row = 2, column = 0, pady = self.BUTTON_PADDING)
        self.delete_products.grid(row = 3, column = 0, pady = self.BUTTON_PADDING)
        self.view_users.grid(row = 4, column = 0, pady = self.BUTTON_PADDING)
        self.add_users.grid(row = 5, column = 0, pady = self.BUTTON_PADDING)
        self.delete_users.grid(row = 6, column = 0, pady = self.BUTTON_PADDING)
        
        
    def manager_dashboard(self):
        self.logo_label.grid(
                            row=0,
                            column=0,
                            pady=(0, 20)
                            )
        self.create_common_menu()
        self.view_products.grid(row = 1, column = 0, pady = 5)
        self.add_products.grid(row = 2, column = 0, pady = 5)
        self.delete_products.grid(row = 3, column = 0, pady = 5)
        self.view_users.grid(row = 4, column = 0, pady = 5)
        self.add_users.grid(row = 5, column = 0, pady = 5)
        
        
    def worker_dashboard(self):
        self.create_common_menu()
        self.view_products.grid(row = 1, column = 0, pady = 5)
        self.add_products.grid(row = 2, column = 0, pady = 5)
        self.delete_products.grid(row = 3, column = 0, pady = 5)

    def create_common_menu(self):
        self.view_products = tk.Button(self.menu_frame, 
                                       text = "View Products", 
                                       bg = self.TEXT_COLOR_BEIGE, 
                                       image = self.view_products_icon,
                                       compound="left",
                                       command=lambda: self.show_page(ViewProducts),
                                       padx = 5,
                                       pady = 5,
                                       anchor="w",
                                       width=140
                                        )                               
        self.add_products = tk.Button(self.menu_frame, text = " Add products",  
                                      bg = self.TEXT_COLOR_BEIGE, 
                                      image = self.add_products_icon,
                                      compound = "left",
                                      command=lambda: self.show_page(AddProducts),
                                      padx = 5,
                                      pady = 5,
                                      anchor="w",
                                      width=140
                                      )               
        self.delete_products = tk.Button(self.menu_frame, 
                                         text = "Delete Products",  
                                         bg = self.TEXT_COLOR_BEIGE, 
                                         image = self.delete_products_icon,
                                         compound = "left",
                                         command=lambda: self.show_page(AddProducts),
                                         padx = 5,
                                         pady = 5,
                                         anchor="w",
                                         width=140
                                         )
        self.view_users = tk.Button(self.menu_frame, 
                                    text = "View Users", 
                                    bg = self.TEXT_COLOR_BEIGE, 
                                    image = self.view_users_icon,
                                    compound = "left",
                                    command=lambda: self.show_page(ViewUsers),
                                    padx = 5,
                                    pady = 5,
                                    anchor="w",
                                    width=140
                                    )
        self.add_users = tk.Button(self.menu_frame, 
                                    text = "Add Users",  
                                    image = self.add_users_icon,
                                    compound = "left",
                                    bg = self.TEXT_COLOR_BEIGE, 
                                    command=lambda: self.show_page(AddUsers),
                                    padx = 5,
                                    pady = 5,
                                    anchor="w",
                                    width=140
                                   )
        self.delete_users = tk.Button(self.menu_frame, 
                                      text = "Delete Users", 
                                      image = self.delete_users_icon,
                                      compound = "left", 
                                      bg = self.TEXT_COLOR_BEIGE, 
                                      command=lambda: self.show_page(AddUsers),
                                      padx = 5,
                                      pady = 5,
                                      anchor="w",
                                      width=140
                                      )
        

        
        self.add_hover_to_buttons([
            self.view_products,
            self.add_products,
            self.delete_products,
            self.view_users,
            self.add_users,
            self.delete_users
        ])
        
    
    def add_hover_to_buttons(self, buttons):
        for button in buttons:
            self.add_hover(button)
        
    def open_add_products(self, content_frame):
        AddProducts(content_frame)

    def go_back(self):
        self.root.unbind("<Configure>")
        self.show_login_callback()
    
    def load_dashboard(self):
        if self.role == "consumer":
            print("consumer dashboard")
        elif self.role == "manager":
            self.manager_dashboard()
        elif self.role == "worker":
            return self.worker_dashboard()
        elif self.role == "superuser":
           return self.superuser_dashboard() 
        else:
            messagebox.showerror(
                    "Invalid login")
            
