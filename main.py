import customtkinter as ctk
from src.database.db_config import setup_database
from src.interfaces.hub import MainWindow

if __name__ == "__main__":
    # Setup the database
    setup_database()

    # Create and run the application
    app = MainWindow()
import tkinter as tk
from src.database.db_config import setup_database
from src.auth.login import LoginFrame
import customtkinter as ctk
from src.interfaces.hub import MainWindow


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure the window
        self.title("Hardware Store Login")
        self.geometry("400x500")

        # Create and pack the login frame
        self.login_frame = LoginFrame(self, self)
        self.login_frame.pack(fill="both", expand=True)

        # Center the window
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    # Setup the database
    setup_database()

    # Create and run the application
    app = App()
    app.mainloop()
