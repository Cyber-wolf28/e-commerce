import tkinter as tk
from backend.db import DataBase
from tkinter import ttk
from .add_products import AddProducts
from .add_users import AddUsers

class ViewUsers:
    
    FONT = ("Segoe UI", 13)
    ENTRY_WIDTH = 40
    BG_COLOR_BEIGE = "#e5c0b3"
    
    COLUMNS = (
                "ID",
                "Name",
                "Surname",
                "Username",
                "Role",
                "Email",
                "Date",
                "Time"
                )
    
        
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.db = DataBase()
        self.edit_entry = None
        self.build_page()
        
        
    def build_page(self):
        
        self.clear_page()
            
        title = tk.Label(
                        self.content_frame,
                        text = "View Users",
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
                                font=("Segoe UI", 10)
                                )
        
        self.search_entry.pack(side = "left", padx =(5,10))
        
        search_button = tk.Button(
                                    search_frame,
                                    text = "Search",
                                    command = self.search_users
                                )
        search_button.pack(side ="left")
        
        refresh_button = tk.Button(
                                    search_frame,
                                    text = "Refresh",
                                    width = 10,
                                    command = self.load_users
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
                                                      "ID",
                                                      "Name",
                                                      "Surname",
                                                      "Username",
                                                      "Role",
                                                      "Email",
                                                      "Date",
                                                      "Time",
                                                      ],
                                            state = "readonly",
                                            width = 20
                                            )
        
        self.category_combo.current(0)
        self.category_combo.pack(side = "left", padx = 10)
        
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill = "both", expand = True, padx = 20, pady = 10)
                                            

        
        self.users_table = ttk.Treeview(
                                            table_frame,
                                            columns = self.COLUMNS,
                                            show = "headings"
                                            )
        self.setup_table()
        
        scrollbar = ttk.Scrollbar(
                                    table_frame,
                                    orient="vertical",
                                    command=self.users_table.yview
                                )

        self.users_table.configure(
                                    yscrollcommand=scrollbar.set
                                    )

        scrollbar.pack(side="right", fill="y")
        self.users_table.pack(fill="both", expand=True)
        
        button_frame = tk.Frame(
                                self.content_frame,
                                bg=self.BG_COLOR_BEIGE
                                )
        button_frame.pack(pady=10)

        tk.Button(
                    button_frame,
                    text="Add User",
                    width=15,
                    command = self.open_add_user).pack(side="left", padx=5)

        tk.Button(
                    button_frame,
                    text="Delete User",
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
        

        
        self.users_table.bind(
                                "<Double-1>",
                                self.edit_cell
                                )
        
        self.category_combo.bind(
            "<<ComboboxSelected>>",
            self.filter_users
        )
        
        self.load_users()
        
    def clear_page(self):
        for widget in self.content_frame.winfo_children():
                    widget.destroy()
        
    def populate_table(self, products):
        
        self.users_table.delete(*self.users_table.get_children())

        for product in products:
            self.users_table.insert("", tk.END, values=product)

        self.product_count.config(
            text=f"Showing {len(products)} Products"
            )
    
    
    def setup_table(self):
        
        for col in self.COLUMNS:
            self.users_table.heading(col, text = col)
            
        self.users_table.column("ID", width = 50, anchor = "center")
        self.users_table.column("Name", width = 80, anchor = "center")
        self.users_table.column("Surname", width = 80, anchor = "center")
        self.users_table.column("Username", width = 80, anchor = "center")
        self.users_table.column("Role", width = 80, anchor = "center")
        self.users_table.column("Email", width = 150, anchor = "center")
        self.users_table.column("Date", width = 100, anchor = "center")
        self.users_table.column("Time", width = 100, anchor = "center")
    
    def open_add_user(self):
        AddUsers(self.content_frame)
    
    def filter_users(self, event):
        
        category = self.category_combo.get()
        print(category)
        
    def search_users(self):
        
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            self.load_users()
            return
        print(search_text)
        
    def load_users(self):
        
        users = self.db.get_all_users()
        self.populate_table(users)


    def view_product(self, event):
        selected = self.users_table.selection()

        if not selected:
            return

        values = self.users_table.item(selected[0], "values")

        print(values)
        
    def edit_cell(self, event):
        
        #Remove any existing edit boxes
        if self.edit_entry is not None:
            self.edit_entry.destroy()
            self.edit_entry = None
        
        row_id = self.users_table.identify_row(event.y)
        column_id = self.users_table.identify_column(event.x)
        
        if not row_id or not column_id:
            return
        
        #only Columns 2, 3, 4, 5 and 6 can be edited
        editable_columns = {
            "#2" : "Name",
            "#3" : "Surname",
            "#4" : "Username",
            "#5" : "Email",
        }
        
        if column_id not in editable_columns:
            return
        
        column_name = editable_columns[column_id]
        
        values = self.users_table.item(row_id, "values")
        column_index = int(column_id[1:]) - 1
        current_value = values[column_index]
        
        #get the position and size of the cell
        bbox = self.users_table.bbox(row_id, column_id)
        
        if not bbox:
            return
        
        x, y, width, height = bbox
        
        #Create  an Entry over the cell
        self.edit_entry = tk.Entry(
                        self.users_table,
                        font =  ("Segoe UI", 10)
                        )
        
        self.edit_entry.place(
                    x=x,
                    y=y,
                    width = width,
                    height = height
                    )
        
        self.edit_entry.insert(0, current_value)
        self.edit_entry.select_range(0, tk.END)
        self.edit_entry.focus()
        
        #Save when Enter is pressed
        self.edit_entry.bind(
            "<Return>",
            lambda event: self.save_cell(
                row_id,
                column_name,
                column_index
            )
        )
        
        #Cancel when Escape is pressed
        self.edit_entry.bind(
            "<Escape>",
            lambda event: self.cancel_edit()
        )
        
    def save_cell(self, row_id, column_name, column_index):

        new_value = self.edit_entry.get().strip()

        if not new_value:
            print("Value cannot be empty.")
            return

        values = list(
            self.users_table.item(row_id, "values")
        )

        user_id = values[2]

        # Update database
        self.db.update_user(
            user_id,
            column_name,
            new_value
        )

        # Remove edit box
        self.edit_entry.destroy()
        self.edit_entry = None
        
        # Reload table
        self.load_users()
        
    def cancel_edit(self):

        if self.edit_entry is not None:
            self.edit_entry.destroy()
            self.edit_entry = None