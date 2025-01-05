import customtkinter as ctk
from tkinter import ttk
from src.database.db_config import get_db_connection

class PurchaseTable(ctk.CTkFrame):
    def __init__(self, parent, product_manager):
        super().__init__(parent)
        self.product_manager = product_manager
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create a frame to contain the treeview and scrollbars
        self.table_frame = ctk.CTkFrame(self, width=500)
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Admin", "User", "Date", "Total Amount", "Products"), show="headings")
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Admin", text="Admin")
        self.tree.heading("User", text="User")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Total Amount", text="Total Amount")
        self.tree.heading("Products", text="Purchased Items")
        
        # Configure column widths
        self.tree.column("ID", width=50)
        self.tree.column("Admin", width=100)
        self.tree.column("User", width=100)
        self.tree.column("Date", width=150)
        self.tree.column("Total Amount", width=100)
        self.tree.column("Products", width=300)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Initial load
        self.refresh()
    
    def refresh(self):
        """Refresh the purchase table data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all purchases with admin and user info
            cursor.execute("""
                SELECT 
                    p.id,
                    a.username as admin_name,
                    u.name as user_name,
                    p.created_at,
                    p.total_amount
                FROM purchases p
                LEFT JOIN admin a ON p.created_by = a.id
                LEFT JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
            """)
            purchases = cursor.fetchall()
            
            # For each purchase, get its products
            for purchase in purchases:
                purchase_id = purchase[0]
                cursor.execute("""
                    SELECT pr.name, pd.quantity
                    FROM purchase_details pd
                    JOIN products pr ON pd.product_id = pr.id
                    WHERE pd.purchase_id = ?
                    ORDER BY pr.name
                """, (purchase_id,))
                products = cursor.fetchall()
                
                # Format products as "item1, qty1 | item2, qty2"
                products_str = " | ".join([f"{name}, {qty}" for name, qty in products])
                
                # Format total amount with currency symbol
                formatted_total = f"${purchase[4]:.2f}"
                
                # Insert into treeview with all information
                self.tree.insert("", "end", values=(
                    purchase_id,
                    purchase[1] or "N/A",  # Admin name
                    purchase[2] or "N/A",  # User name
                    purchase[3],           # Date
                    formatted_total,       # Total amount
                    products_str          # Products with quantities
                ))
            
            conn.close()
                
        except Exception as e:
            print(f"Error loading purchases: {e}")
