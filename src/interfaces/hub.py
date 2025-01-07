import customtkinter as ctk
from tkinter import messagebox
from src.database.db_config import get_db_connection

# Import components
from ..pages.sidebar import SidebarFrame
from ..pages.product import ProductManagementFrame
from ..pages.categories import CategoriesFrame
from ..pages.dashboard import DashboardFrame
from ..pages.checkout import CheckoutFrame
from ..pages.admin import AdminFrame
from ..pages.users import UsersFrame


class ProfileDialog(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.title("User Profile")
        self.geometry("400x300")

        # Make the dialog modal
        self.transient(parent)
        self.grab_set()

        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Profile content
        ctk.CTkLabel(self, text="Profile Information", font=("Arial", 24, "bold")).pack(
            pady=20
        )

        # Username display
        username_frame = ctk.CTkFrame(self)
        username_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(username_frame, text="Username:", font=("Arial", 14, "bold")).pack(
            side="left", padx=10
        )

        ctk.CTkLabel(username_frame, text=username, font=("Arial", 14)).pack(
            side="left", padx=10
        )

        # Change password section
        password_frame = ctk.CTkFrame(self)
        password_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            password_frame, text="Change Password", font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.current_password = ctk.CTkEntry(
            password_frame, placeholder_text="Current Password", show="*"
        )
        self.current_password.pack(pady=5, padx=10, fill="x")

        self.new_password = ctk.CTkEntry(
            password_frame, placeholder_text="New Password", show="*"
        )
        self.new_password.pack(pady=5, padx=10, fill="x")

        self.confirm_password = ctk.CTkEntry(
            password_frame, placeholder_text="Confirm New Password", show="*"
        )
        self.confirm_password.pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(
            password_frame, text="Change Password", command=self.change_password
        ).pack(pady=10)

    def change_password(self):
        current = self.current_password.get()
        new = self.new_password.get()
        confirm = self.confirm_password.get()

        if not all([current, new, confirm]):
            messagebox.showwarning("Warning", "All fields are required")
            return

        if new != confirm:
            messagebox.showwarning("Warning", "New passwords do not match")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verify current password
            cursor.execute(
                "SELECT password FROM users WHERE username = ?", (self.master.username,)
            )
            stored_password = cursor.fetchone()[0]

            if current != stored_password:  # In a real app, use proper password hashing
                messagebox.showerror("Error", "Current password is incorrect")
                return

            # Update password
            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new, self.master.username),
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Password changed successfully")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error changing password: {e}")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize database connection
        self.db_connection = get_db_connection()

        # Configure the window
        self.title("Hardware Store Management")
        self.geometry("1200x800")

        # Create the main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        # Create sidebar
        self.sidebar = SidebarFrame(
            self.main_container, show_content_callback=self.show_content
        )
        self.sidebar.pack(side="top", fill="x", padx=10, pady=10)

        # Create content frame
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Show initial content
        self.show_content("dashboard")

    def show_content(self, content_type):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show the selected content
        if content_type == "dashboard":
            DashboardFrame(self.content_frame).pack(fill="both", expand=True)
        elif content_type == "products":
            ProductManagementFrame(self.content_frame).pack(fill="both", expand=True)
        elif content_type == "categories":
            CategoriesFrame(self.content_frame).pack(fill="both", expand=True)
        elif content_type == "checkout":
            CheckoutFrame(self.content_frame).pack(fill="both", expand=True)
        elif content_type == "admin":
            AdminFrame(self.content_frame).pack(fill="both", expand=True)
        elif content_type == "users":
            UsersFrame(self.content_frame).pack(fill="both", expand=True)

    def on_closing(self):
        # Close database connection
        if hasattr(self, "db_connection") and self.db_connection:
            self.db_connection.close()
        self.quit()

    def run(self):
        """Run the application"""
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
