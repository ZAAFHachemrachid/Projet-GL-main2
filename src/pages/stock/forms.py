import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

class AddStockForm(ctk.CTkFrame):
    def __init__(self, parent, stock_manager, refresh_callback):
        super().__init__(parent)
        self.stock_manager = stock_manager
        self.refresh_callback = refresh_callback
        
        # Title
        ctk.CTkLabel(self, text="Add Stock", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Product ID
        self.product_id = ctk.CTkEntry(self, placeholder_text="Product ID")
        self.product_id.pack(pady=5, padx=10, fill="x")
        
        # Quantity
        self.quantity = ctk.CTkEntry(self, placeholder_text="Quantity to Add")
        self.quantity.pack(pady=5, padx=10, fill="x")
        
        # Date frame
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(date_frame, text="Date:").pack(side="left", padx=5)
        self.date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.date_entry.pack(side="left", padx=5)
        
        # Note
        self.note = ctk.CTkEntry(self, placeholder_text="Note (Optional)")
        self.note.pack(pady=5, padx=10, fill="x")
        
        # Add button
        ctk.CTkButton(self, text="Add Stock", 
                     command=self.add_stock,
                     fg_color="#2ecc71",
                     hover_color="#27ae60").pack(pady=10)
    
    def add_stock(self):
        try:
            product_id = int(self.product_id.get())
            quantity = int(self.quantity.get())
            date = self.date_entry.get_date().strftime("%Y-%m-%d")
            note = self.note.get()
            
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            success = self.stock_manager.add_stock(product_id, quantity, date, note)
            
            if success:
                messagebox.showinfo("Success", "Stock added successfully")
                self.refresh_callback()
                # Clear fields
                self.product_id.delete(0, 'end')
                self.quantity.delete(0, 'end')
                self.note.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Failed to add stock")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

class RemoveStockForm(ctk.CTkFrame):
    def __init__(self, parent, stock_manager, refresh_callback):
        super().__init__(parent)
        self.stock_manager = stock_manager
        self.refresh_callback = refresh_callback
        
        # Title
        ctk.CTkLabel(self, text="Remove Stock", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Product ID
        self.product_id = ctk.CTkEntry(self, placeholder_text="Product ID")
        self.product_id.pack(pady=5, padx=10, fill="x")
        
        # Quantity
        self.quantity = ctk.CTkEntry(self, placeholder_text="Quantity to Remove")
        self.quantity.pack(pady=5, padx=10, fill="x")
        
        # Date frame
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(date_frame, text="Date:").pack(side="left", padx=5)
        self.date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.date_entry.pack(side="left", padx=5)
        
        # Note
        self.note = ctk.CTkEntry(self, placeholder_text="Note (Optional)")
        self.note.pack(pady=5, padx=10, fill="x")
        
        # Remove button
        ctk.CTkButton(self, text="Remove Stock",
                     command=self.remove_stock,
                     fg_color="#e74c3c",
                     hover_color="#c0392b").pack(pady=10)
    
    def remove_stock(self):
        try:
            product_id = int(self.product_id.get())
            quantity = int(self.quantity.get())
            date = self.date_entry.get_date().strftime("%Y-%m-%d")
            note = self.note.get()
            
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            success, message = self.stock_manager.remove_stock(product_id, quantity, date, note)
            
            if success:
                messagebox.showinfo("Success", "Stock removed successfully")
                self.refresh_callback()
                # Clear fields
                self.product_id.delete(0, 'end')
                self.quantity.delete(0, 'end')
                self.note.delete(0, 'end')
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

class SearchStockForm(ctk.CTkFrame):
    def __init__(self, parent, stock_manager, refresh_callback):
        super().__init__(parent)
        self.stock_manager = stock_manager
        self.refresh_callback = refresh_callback
        
        # Title
        ctk.CTkLabel(self, text="Search Stock Movements", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Product ID
        self.product_id = ctk.CTkEntry(self, placeholder_text="Product ID (Optional)")
        self.product_id.pack(pady=5, padx=10, fill="x")
        
        # Movement Type
        self.movement_type = ctk.CTkComboBox(self, values=["All", "IN", "OUT"])
        self.movement_type.set("All")
        self.movement_type.pack(pady=5, padx=10, fill="x")
        
        # Date range frame
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=5, padx=10, fill="x")
        
        # From date
        ctk.CTkLabel(date_frame, text="From:").pack(side="left", padx=5)
        self.date_from = DateEntry(date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        self.date_from.pack(side="left", padx=5)
        
        # To date
        ctk.CTkLabel(date_frame, text="To:").pack(side="left", padx=5)
        self.date_to = DateEntry(date_frame, width=12, background='darkblue',
                               foreground='white', borderwidth=2)
        self.date_to.pack(side="left", padx=5)
        
        # Search button
        ctk.CTkButton(self, text="Search",
                     command=self.search).pack(pady=10)
        
        # Clear button
        ctk.CTkButton(self, text="Clear",
                     command=self.clear,
                     fg_color="#95a5a6",
                     hover_color="#7f8c8d").pack(pady=5)
    
    def search(self):
        filters = {}
        
        # Add product ID filter if provided
        if self.product_id.get():
            try:
                filters['product_id'] = int(self.product_id.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Product ID")
                return
        
        # Add movement type filter if not "All"
        if self.movement_type.get() != "All":
            filters['movement_type'] = self.movement_type.get()
        
        # Add date range filters
        filters['date_from'] = self.date_from.get_date().strftime("%Y-%m-%d")
        filters['date_to'] = self.date_to.get_date().strftime("%Y-%m-%d")
        
        # Refresh table with filters
        self.refresh_callback(filters)
    
    def clear(self):
        self.product_id.delete(0, 'end')
        self.movement_type.set("All")
        self.date_from.set_date(datetime.now())
        self.date_to.set_date(datetime.now())
        self.refresh_callback(None)  # Refresh without filters
