import customtkinter as ctk
from .forms import CreateForm, UpdateForm, DeleteForm, SearchForm
from .product_table import ProductTable
from .product_manager import ProductManager

class ProductManagementFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Configure grid for the main frame
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Initialize product manager
        self.product_manager = ProductManager()
        
        # Create left side container for forms
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_container.grid_rowconfigure(1, weight=1)  # Make forms row expandable
        self.left_container.grid_columnconfigure(0, weight=1)
        
        # Create forms
        self.setup_forms()
        
        # Create table frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Create table
        self.setup_table()
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
    
    def setup_forms(self):
        """Setup all forms and form switching buttons"""
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Create buttons to switch between forms
        button_styles = {
            "create": {"text": "Create Product", "fg_color": "#2ecc71", "hover_color": "#27ae60"},
            "update": {"text": "Update Product", "fg_color": "#3498db", "hover_color": "#2980b9"},
            "delete": {"text": "Delete Product", "fg_color": "#e74c3c", "hover_color": "#c0392b"},
            "search": {"text": "Search Product", "fg_color": "#9b59b6", "hover_color": "#8e44ad"}
        }
        
        for i, (form_type, style) in enumerate(button_styles.items()):
            ctk.CTkButton(
                self.switch_buttons_frame,
                text=style["text"],
                command=lambda t=form_type: self.show_form(t),
                fg_color=style["fg_color"],
                hover_color=style["hover_color"]
            ).grid(row=0, column=i, padx=2, sticky="ew")
        
        # Initialize forms
        self.create_form = CreateForm(self.left_container, self.product_manager, self.refresh_table)
        self.update_form = UpdateForm(self.left_container, self.product_manager, self.refresh_table)
        self.delete_form = DeleteForm(self.left_container, self.product_manager, self.refresh_table)
        self.search_form = SearchForm(self.left_container, self.product_manager, self.refresh_table)
        
        # Store forms in a dictionary for easy access
        self.forms = {
            "create": self.create_form,
            "update": self.update_form,
            "delete": self.delete_form,
            "search": self.search_form
        }
    
    def setup_table(self):
        """Setup the product table"""
        self.product_table = ProductTable(self.table_frame, self.product_manager)
        self.product_table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    def show_form(self, form_type):
        """Show the selected form and hide others"""
        for form in self.forms.values():
            form.grid_remove()
        self.forms[form_type].grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def refresh_table(self):
        """Refresh the product table"""
        self.product_table.refresh()
