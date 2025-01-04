import customtkinter as ctk
from tkinter import ttk
from database.db_config import get_stock_alerts

class StockAlertFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        title = ctk.CTkLabel(
            self,
            text="Stock Alerts",
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        title.pack(pady=20)
        
        # Create table frame
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Create Treeview
        self.tree = ttk.Treeview(table_frame, columns=("Reference", "Name", "Quantity", "Min Quantity", "Category"), show="headings")
        
        # Define column headings
        self.tree.heading("Reference", text="Reference")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Min Quantity", text="Min Quantity")
        self.tree.heading("Category", text="Category")
        
        # Configure column widths
        self.tree.column("Reference", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("Quantity", width=80)
        self.tree.column("Min Quantity", width=80)
        self.tree.column("Category", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            self,
            text="Refresh",
            command=self.refresh_alerts
        )
        refresh_btn.pack(pady=10)
        
        # Load initial data
        self.refresh_alerts()
    
    def refresh_alerts(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and display alerts
        alerts = get_stock_alerts()
        for alert in alerts:
            self.tree.insert("", "end", values=alert)
