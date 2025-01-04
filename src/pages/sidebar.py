import customtkinter as ctk

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, show_content_callback):
        super().__init__(parent)
        self.show_content_callback = show_content_callback
        
        # Menu label
        ctk.CTkLabel(
            self,
            text="Hardware Store",
            font=("Arial", 20, "bold"),
            text_color="#333333"
        ).pack(pady=10)
        
        # Create horizontal frame for buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=5)
        
        # Create navigation buttons
        self.buttons = {
            "dashboard": {
                "text": "Dashboard",
                "icon": "📊"
            },
            "products": {
                "text": "Products",
                "icon": "📦"
            },
            "categories": {
                "text": "Categories",
                "icon": "🏷️"
            },
            "checkout": {
                "text": "Checkout",
                "icon": "🛒"
            },
            "users": {
                "text": "Users",
                "icon": "👥"
            },
            "admin": {
                "text": "Admin",
                "icon": "👨‍💼"
            }
        }
        
        for button_type, button_config in self.buttons.items():
            self.create_menu_button(button_config["icon"] + " " + button_config["text"], button_type, button_frame)
    
    def create_menu_button(self, text, content_type, parent):
        """Create a menu button with consistent styling"""
        button = ctk.CTkButton(
            parent,
            text=text,
            fg_color="transparent",
            text_color=("#333333", "#FFFFFF"),
            hover_color=("gray75", "gray25"),
            width=120,  # Fixed width for uniform buttons
            height=35,  # Fixed height for uniform buttons
            command=lambda content_type=content_type: self.show_content_callback(content_type)
        )
        button.pack(side="left", padx=5, pady=5)
