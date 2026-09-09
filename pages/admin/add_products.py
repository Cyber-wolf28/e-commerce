import tkinter as tk
from backend.auth_service import AuthService
from backend.db import DataBase
from tkinter import messagebox
from tkinter import filedialog

class AddProducts:
    
    FONT = ("Segoe UI", 13)
    ENTRY_WIDTH = 40
    BG_COLOR_BEIGE = "#e5c0b3"
    
        
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.image_path = None
        self.db = DataBase()
        self.build_page()
        
    
    def create_field(self, text, row):
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

        entry = tk.Entry(self.form_frame, width = self.ENTRY_WIDTH)

        entry.grid(
            row=row,
            column=1,
            padx=10,
            pady=5
        )

        return entry
    
    def choose_image(self):

        file_path = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file_path:
            self.image_path = file_path
            print(self.image_path)
            
    def build_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.form_frame = tk.Frame(
                                    self.content_frame,
                                    bg = self.BG_COLOR_BEIGE
                                    )

        self.product_name_entry = self.create_field("Product Name:", 0)
        self.product_price_entry = self.create_field("Price:", 1)
        self.stock_entry = self.create_field("Stock:", 2)
        
        image_label = tk.Label(
                                self.form_frame,
                                text = "Image:",
                                font = self.FONT,
                                bg = self.BG_COLOR_BEIGE
        )
        self.image_button = tk.Button(
                                        self.form_frame,
                                        text = "Choose Image",
                                        command = self.choose_image
        )
        self.add_button = tk.Button(
                                    self.form_frame,
                                    text = "Save",
                                    command = self.add_product

        )
        
        self.form_frame.pack(anchor = "nw", padx = 20, pady = 20)
        image_label.grid(row = 3, column = 0, sticky = "w", padx = 5, pady = 10)
        self.image_button.grid(row=3, column = 1, sticky = "w", pady = 10)
        self.add_button.grid(row=4, column=1, sticky="w", padx=5, pady=10)
        
        
    def add_product(self):
            
        fruit = self.product_name_entry.get().strip()
        price = self.product_price_entry.get().strip()
        stock = self.stock_entry.get().strip()
        image_path = self.image_path
            
        success = self.db.add_product(
                                fruit,
                                price,
                                stock,
                                image_path
                                )
        if success:
            self.product_name_entry.delete(0, tk.END)
            self.product_price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)
            self.image_path = None
            messagebox.showinfo("Success", "Product added successfully!")
        if not fruit:
            messagebox.showerror("Error", "Could not add product.")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number!")
            return
        
        try:
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Stock must be a whole number.")
            return
        if not self.image_path:
            messagebox.showerror("Error", "Please choose an image.")
            return

        