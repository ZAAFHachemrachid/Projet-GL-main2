import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from PIL import Image

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_config import get_db_connection

class RegisterWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("NANEF-Register")
        self.geometry("800x700")
        self.resizable(False, False)
        
        # Set theme background
        self.configure(fg_color="#ffffff")

        # Create background with pattern
        self.bg_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and set background pattern
        bg_pattern_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "static", "Login (3).png")
        try:
            bg_pattern = Image.open(bg_pattern_path)
            self.bg_pattern = ctk.CTkImage(
                light_image=bg_pattern,
                dark_image=bg_pattern,
                size=(800, 700)
            )
            self.bg_label = ctk.CTkLabel(self.bg_frame, image=self.bg_pattern, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Warning: Could not load background pattern: {e}")

        # Create main frame with glass effect
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#f0f0f0",
            corner_radius=30,
            width=400,
            height=600,
            border_width=0
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome to  text
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text=" Welcome to",
            font=("Arial Black", 24, "bold"),
            text_color="#000000"
        )
        self.welcome_label.place(relx=0.5, rely=0.12, anchor="center")

        # NANEF text
        self.nanef_label = ctk.CTkLabel(
            self.main_frame,
            text="NANEF",
            font=("Arial Black", 28, "bold"),
            text_color="#6c5ce7"
        )
        self.nanef_label.place(relx=0.5, rely=0.22, anchor="center")

        # Hardware Store text
        self.store_label = ctk.CTkLabel(
            self.main_frame,
            text="Hardware Store",
            font=("Arial", 14),
            text_color="#666666"
        )
        self.store_label.place(relx=0.5, rely=0.27, anchor="center")
         #Create account text
        self.create_account_label = ctk.CTkLabel(
            self.main_frame,
            text=" Create Account",
            font=("Arial Black", 20, "bold"),
            text_color="#000000"
        )
        self.create_account_label.place(relx=0.5, rely=0.33, anchor="center")

        # Username label
        self.username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.username_label.place(relx=0.15, rely=0.35)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="Username",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999"
        )
        self.username_entry.place(relx=0.15, rely=0.4)

        # Email label
        self.email_label = ctk.CTkLabel(
            self.main_frame,
            text="Email",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.email_label.place(relx=0.15, rely=0.47)

        # Email entry
        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="Enter your email",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999"
        )
        self.email_entry.place(relx=0.15, rely=0.52)

        # Password label
        self.password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.password_label.place(relx=0.15, rely=0.59)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="••••••••••",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999",
            show="•"
        )
        self.password_entry.place(relx=0.15, rely=0.64)

        # Confirm Password label
        self.confirm_password_label = ctk.CTkLabel(
            self.main_frame,
            text="Confirm Password",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.confirm_password_label.place(relx=0.15, rely=0.71)

        # Confirm Password entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="••••••••••",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999",
            show="•"
        )
        self.confirm_password_entry.place(relx=0.15, rely=0.76)

        # Register button
        self.register_button = ctk.CTkButton(
            self.main_frame,
            width=220,
            height=45,
            text="Register",
            font=("Arial", 14, "bold"),
            fg_color="#6c5ce7",
            hover_color="#5f50e3",
            corner_radius=8,
            command=self.register
        )
        self.register_button.place(relx=0.5, rely=0.89, anchor="center")

        # Login link
        self.login_label = ctk.CTkLabel(
            self.main_frame,
            text="Already have an account?",
            font=("Arial", 12),
            text_color="#666666"
        )
        self.login_label.place(relx=0.35, rely=0.95)

        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            text_color="#6c5ce7",
            fg_color="transparent",
            hover_color="#f0f0f0",
            width=30,
            command=self.show_login
        )
        self.login_button.place(relx=0.7, rely=0.95)

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate inputs
        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        # Connect to database
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()

        try:
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already exists")
                return

            # Insert new user
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login()

        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

    def show_login(self):
        self.destroy()
        from auth.login import LoginWindow
        login = LoginWindow()
        login.mainloop()

if __name__ == "__main__":
    app = RegisterWindow()
    app.mainloop()
