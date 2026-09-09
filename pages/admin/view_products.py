import tkinter as tk
from backend.db import DataBase
from tkinter import ttk
from .add_products import AddProducts

class ViewProducts:
    
    FONT = ("Segoe UI", 13)
    ENTRY_WIDTH = 40
    BG_COLOR_BEIGE = "#e5c0b3"
    
    COLUMNS = (
                "Fruit",
                "Price",
                "ID",
                "Stock",
                "Date",
                "Time"
                )
    
        
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.db = DataBase()
        self.build_page()
        
    def build_page(self):
        
        self.clear_page()
            
        title = tk.Label(
                        self.content_frame,
                        text = "View Products",
                        font=("Segoe UI", 22, "bold"),
                        bg = self.BG_COLOR_BEIGE
                        )
        title.pack(pady = 15)
        
        search_frame = tk.Frame(
                                self.content_frame,
                                bg = self.BG_COLOR_BEIGE
                                )
        search_frame.pack(fill="x", padx = 20)
        
        self.search_entry = tk.Entry(
                                search_frame,
                                width = 25,
                                font=self.FONT
                                )
        
        self.search_entry.pack(side = "left", padx =(0,10))
        
        search_button = tk.Button(
                                    search_frame,
                                    text = "Search",
                                    command = self.search_products
                                )
        search_button.pack(side ="left")
        
        refresh_button = tk.Button(
                                    search_frame,
                                    text = "Refresh",
                                    width = 10,
                                    command = self.load_products
                                    )
        refresh_button.pack(side = "left", padx = 10)
        
        filter_frame = tk.Frame(
                                self.content_frame,
                                bg = self.BG_COLOR_BEIGE
                                )
        filter_frame.pack(fill = "x", padx = 20, pady = 10)
        
        tk.Label(
                filter_frame,
                text = "Category",
                bg = self.BG_COLOR_BEIGE,
                font = self.FONT
                ).pack(side = "left")
        
        self.category_combo = ttk.Combobox(
                                            filter_frame,
                                            values = ["All",
                                                      "Electronics",
                                                      "Accessories",
                                                      "Storage"],
                                            state = "readonly",
                                            width = 20
                                            )
        
        self.category_combo.current(0)
        self.category_combo.pack(side = "left", padx = 10)
        
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill = "both", expand = True, padx = 20, pady = 10)
                                            

        
        self.products_table = ttk.Treeview(
                                            table_frame,
                                            columns = self.COLUMNS,
                                            show = "headings"
                                            )
        self.setup_table()
        
        scrollbar = ttk.Scrollbar(
                                    table_frame,
                                    orient="vertical",
                                    command=self.products_table.yview
                                )

        self.products_table.configure(
                                    yscrollcommand=scrollbar.set
                                    )

        scrollbar.pack(side="right", fill="y")
        self.products_table.pack(fill="both", expand=True)
        
        button_frame = tk.Frame(
                                self.content_frame,
                                bg=self.BG_COLOR_BEIGE
                                )
        button_frame.pack(pady=10)

        tk.Button(
                    button_frame,
                    text="Add Product",
                    width=15,
                    command = self.open_add_products).pack(side="left", padx=5)

        tk.Button(
                    button_frame,
                    text="Edit",
                    width=15).pack(side="left", padx=5)

        tk.Button(
                    button_frame,
                    text="Delete",
                    width=15).pack(side="left", padx=5)

        tk.Button(
                    button_frame,
                    text="View Details",
                    width=15).pack(side="left", padx=5)
        
        self.product_count = tk.Label(
                                        self.content_frame,
                                        text="Showing 0 Products",
                                        bg=self.BG_COLOR_BEIGE,
                                        font=("Segoe UI", 10)
                                    )

        self.product_count.pack(pady=(0,10))
        
        self.products_table.bind(
                        "<Double-1>",
                        self.view_product
                        )
        
        self.category_combo.bind(
            "<<ComboboxSelected>>",
            self.filter_products
        )
        
        self.load_products()
        
    def clear_page(self):
        for widget in self.content_frame.winfo_children():
                    widget.destroy()
        
    def populate_table(self, products):
        
        self.products_table.delete(*self.products_table.get_children())

        for product in products:
            self.products_table.insert("", tk.END, values=product)

        self.product_count.config(
            text=f"Showing {len(products)} Products"
            )
    
    
    def setup_table(self):
        
        for col in self.COLUMNS:
            self.products_table.heading(col, text = col)
            
        self.products_table.column("Fruit", width = 180, anchor = "center")
        self.products_table.column("Price", width = 80, anchor = "center")
        self.products_table.column("ID", width = 80, anchor = "center")
        self.products_table.column("Stock", width = 80, anchor = "center")
        self.products_table.column("Date", width = 100, anchor = "center")
        self.products_table.column("Time", width = 100, anchor = "center")
    
    def open_add_products(self):
        AddProducts(self.content_frame)
    
    def filter_products(self, event):
        
        category = self.category_combo.get()
        print(category)
        
    def search_products(self):
        
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            self.load_products()
            return
        print(search_text)
        
    def load_products(self):
        
        products = self.db.get_all_products()
        self.populate_table(products)

        
        
    def view_product(self, event):
        selected = self.products_table.selection()

        if not selected:
            return

        values = self.products_table.item(selected[0], "values")

        print(values)