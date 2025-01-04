import customtkinter as ctk
from .stock_manager import StockManager
from .stock_table import StockTable
from .forms import AddStockForm, RemoveStockForm, SearchStockForm

class StockManagementFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Configure grid for the main frame
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Initialize stock manager
        self.stock_manager = StockManager()
        
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
        
        # Show add form by default
        self.show_form("add")
        
        # Load initial data
        self.refresh_table()
    
    def setup_forms(self):
        """Setup all forms and form switching buttons"""
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Create buttons to switch between forms
        button_styles = {
            "add": {"text": "Add Stock", "fg_color": "#2ecc71", "hover_color": "#27ae60"},
            "remove": {"text": "Remove Stock", "fg_color": "#e74c3c", "hover_color": "#c0392b"},
            "search": {"text": "Search", "fg_color": "#3498db", "hover_color": "#2980b9"}
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
        self.add_form = AddStockForm(self.left_container, self.stock_manager, self.refresh_table)
        self.remove_form = RemoveStockForm(self.left_container, self.stock_manager, self.refresh_table)
        self.search_form = SearchStockForm(self.left_container, self.stock_manager, self.refresh_table)
        
        # Store forms in a dictionary for easy access
        self.forms = {
            "add": self.add_form,
            "remove": self.remove_form,
            "search": self.search_form
        }
    
    def setup_table(self):
        """Setup the stock table"""
        self.stock_table = StockTable(self.table_frame, self.stock_manager)
        self.stock_table.pack(fill="both", expand=True)
    
    def show_form(self, form_type):
        """Show the selected form and hide others"""
        for form in self.forms.values():
            form.pack_forget()
        self.forms[form_type].pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh_table(self, filters=None):
        """Refresh the stock table"""
        self.stock_table.refresh(filters)
