import tkinter as tk
from tkinter import messagebox
import sqlite3
import customtkinter as ctk
from ..database.db_config import get_db_connection
from ..interfaces.hub import MainWindow


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Create main frame with padding
        self.configure(fg_color="transparent")

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Login",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("black", "white"),
        )
        title_label.pack(pady=(40, 30))

        # Username
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=(0, 20))

        # Password
        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password", width=300, show="●"
        )
        self.password_entry.pack(pady=(0, 30))

        # Login button
        login_button = ctk.CTkButton(self, text="Login", command=self.login, width=200)
        login_button.pack(pady=(0, 20))

        # Forgot password link
        forgot_password_link = ctk.CTkLabel(
            self,
            text="Forgot Password?",
            text_color=("blue", "light blue"),
            cursor="hand2",
            font=ctk.CTkFont(size=12, underline=True),
        )
        forgot_password_link.pack()
        forgot_password_link.bind("<Button-1>", lambda e: self.show_forgot_password())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        print(f"Attempting login with username: {username}")  # Debug print

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, username, role 
                    FROM admin 
                    WHERE username = ? AND password = ?
                """,
                    (username, password),
                )
                user = cursor.fetchone()

                if user:
                    # Store user info in the controller
                    self.controller.current_user = {
                        "id": user[0],
                        "username": user[1],
                        "role": user[2],
                    }

                    # Login successful
                    messagebox.showinfo("Success", f"Welcome {username}!")
                    self.open_main_window()
                else:
                    messagebox.showerror("Error", "Invalid username or password")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Could not connect to database")

    def show_forgot_password(self):
        # Implement forgot password functionality
        messagebox.showinfo(
            "Info", "Please contact administrator to reset your password"
        )

    def open_main_window(self):
        # Hide login window
        self.controller.withdraw()

        # Create and show main window
        main_window = MainWindow()

        # Configure main window based on user role
        if hasattr(self.controller, "current_user"):
            main_window.current_user = self.controller.current_user

        # Set up close handler
        def on_main_window_close():
            main_window.destroy()
            self.controller.deiconify()

        main_window.protocol("WM_DELETE_WINDOW", on_main_window_close)
        main_window.run()

    def on_main_window_close(self, main_window):
        # Destroy the main window
        main_window.destroy()

        # Show the login window again
        self.controller.deiconify()

        # Clear the login fields
        self.clear_fields()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
