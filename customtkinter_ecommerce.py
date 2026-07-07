import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("My First CustomTkinter App")

label = ctk.CTkLabel(app, text="Hello, Keanu!")
label.pack(pady=20)

button = ctk.CTkButton(app, text="Click Me")
button.pack(pady=10)

app.mainloop()