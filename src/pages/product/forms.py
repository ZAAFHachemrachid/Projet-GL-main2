import customtkinter as ctk
from tkinter import messagebox

class BaseForm(ctk.CTkFrame):
    def __init__(self, parent, product_manager=None, refresh_callback=None):
        super().__init__(parent)
        self.product_manager = product_manager
        self.refresh_callback = refresh_callback

class CreateForm(BaseForm):
    def __init__(self, parent, product_manager, refresh_callback):
        super().__init__(parent, product_manager, refresh_callback)
        
        # Create a scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Title
        ctk.CTkLabel(self.scroll_frame, text="Create Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        # SKU Field
        ctk.CTkLabel(self.scroll_frame, text="SKU:").pack(pady=5, padx=10, anchor="w")
        self.sku_entry = ctk.CTkEntry(self.scroll_frame)
        self.sku_entry.pack(pady=5, padx=10, fill="x")
        
        # Name Field
        ctk.CTkLabel(self.scroll_frame, text="Name:").pack(pady=5, padx=10, anchor="w")
        self.name_entry = ctk.CTkEntry(self.scroll_frame)
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        # Description Field
        ctk.CTkLabel(self.scroll_frame, text="Description:").pack(pady=5, padx=10, anchor="w")
        self.description_entry = ctk.CTkEntry(self.scroll_frame)
        self.description_entry.pack(pady=5, padx=10, fill="x")
        
        # Price Field
        ctk.CTkLabel(self.scroll_frame, text="Price:").pack(pady=5, padx=10, anchor="w")
        self.price_entry = ctk.CTkEntry(self.scroll_frame)
        self.price_entry.pack(pady=5, padx=10, fill="x")
        
        # Quantity Field
        ctk.CTkLabel(self.scroll_frame, text="Quantity:").pack(pady=5, padx=10, anchor="w")
        self.quantity_entry = ctk.CTkEntry(self.scroll_frame)
        self.quantity_entry.pack(pady=5, padx=10, fill="x")
        
        # Min Quantity Field
        ctk.CTkLabel(self.scroll_frame, text="Minimum Quantity:").pack(pady=5, padx=10, anchor="w")
        self.min_quantity_entry = ctk.CTkEntry(self.scroll_frame)
        self.min_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        # Category Field
        ctk.CTkLabel(self.scroll_frame, text="Category:").pack(pady=5, padx=10, anchor="w")
        self.category_combobox = ctk.CTkComboBox(self.scroll_frame, values=[cat[1] for cat in self.product_manager.categories], state="readonly")
        self.category_combobox.pack(pady=5, padx=10, fill="x")
        
        # Create Button
        ctk.CTkButton(
            self.scroll_frame,
            text="Create",
            command=self.create_product,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=10, padx=10, fill="x")
    
    def create_product(self):
        """Create a new product"""
        try:
            # Get values from entries
            sku = self.sku_entry.get().strip()
            name = self.name_entry.get().strip()
            description = self.description_entry.get().strip()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            min_quantity = int(self.min_quantity_entry.get())
            category = self.category_combobox.get()
            
            # Validate SKU format
            if not self.product_manager.validate_sku(sku):
                messagebox.showerror("Error", "Invalid SKU format. Must be 2-3 uppercase letters followed by 3 digits.")
                return
            
            # Check if SKU is unique
            if not self.product_manager.is_sku_unique(sku):
                messagebox.showerror("Error", "SKU already exists.")
                return
            
            # Create product
            if self.product_manager.create_product(sku, name, description, price, quantity, min_quantity, category):
                messagebox.showinfo("Success", "Product created successfully!")
                self.clear_entries()
                if self.refresh_callback:
                    self.refresh_callback()
        
        except ValueError as e:
            messagebox.showerror("Error", "Please check your input values.")
    
    def clear_entries(self):
        """Clear all entry fields"""
        self.sku_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.min_quantity_entry.delete(0, 'end')
        # Get the values using get() method and set the first value if available
        values = self.category_combobox.get()
        if values:
            self.category_combobox.set(self.product_manager.categories[0][1] if self.product_manager.categories else '')

class UpdateForm(BaseForm):
    def __init__(self, parent, product_manager, refresh_callback):
        super().__init__(parent, product_manager, refresh_callback)
        
        # Create a scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Title
        ctk.CTkLabel(self.scroll_frame, text="Update Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        # ID Entry and Load Button Frame
        id_frame = ctk.CTkFrame(self.scroll_frame)
        id_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(id_frame, text="ID:").pack(side="left", padx=(0,5))
        self.id_entry = ctk.CTkEntry(id_frame, width=120)
        self.id_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            id_frame,
            text="Load Product",
            command=self.load_product,
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=5)
        
        # Fields Frame
        self.fields_frame = ctk.CTkFrame(self.scroll_frame)
        self.fields_frame.pack(fill="x", padx=10, pady=5)
        
        # SKU Field
        ctk.CTkLabel(self.fields_frame, text="SKU:").pack(pady=5, anchor="w")
        self.sku_entry = ctk.CTkEntry(self.fields_frame)
        self.sku_entry.pack(fill="x", pady=5)
        
        # Name Field
        ctk.CTkLabel(self.fields_frame, text="Name:").pack(pady=5, anchor="w")
        self.name_entry = ctk.CTkEntry(self.fields_frame)
        self.name_entry.pack(fill="x", pady=5)
        
        # Description Field
        ctk.CTkLabel(self.fields_frame, text="Description:").pack(pady=5, anchor="w")
        self.description_entry = ctk.CTkEntry(self.fields_frame)
        self.description_entry.pack(fill="x", pady=5)
        
        # Price Field
        ctk.CTkLabel(self.fields_frame, text="Price:").pack(pady=5, anchor="w")
        self.price_entry = ctk.CTkEntry(self.fields_frame)
        self.price_entry.pack(fill="x", pady=5)
        
        # Quantity Field
        ctk.CTkLabel(self.fields_frame, text="Quantity:").pack(pady=5, anchor="w")
        self.quantity_entry = ctk.CTkEntry(self.fields_frame)
        self.quantity_entry.pack(fill="x", pady=5)
        
        # Min Quantity Field
        ctk.CTkLabel(self.fields_frame, text="Minimum Quantity:").pack(pady=5, anchor="w")
        self.min_quantity_entry = ctk.CTkEntry(self.fields_frame)
        self.min_quantity_entry.pack(fill="x", pady=5)
        
        # Category Field
        ctk.CTkLabel(self.fields_frame, text="Category:").pack(pady=5, anchor="w")
        self.category_combobox = ctk.CTkComboBox(self.fields_frame, values=[cat[1] for cat in self.product_manager.categories], state="readonly")
        self.category_combobox.pack(fill="x", pady=5)
        
        # Update Button
        ctk.CTkButton(
            self.fields_frame,
            text="Update",
            command=self.update_product,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=10, fill="x")
        
        # Initially disable fields
        self.set_fields_state("disabled")
    
    def set_fields_state(self, state):
        """Enable or disable form fields"""
        widgets = [
            self.sku_entry,
            self.name_entry,
            self.description_entry,
            self.price_entry,
            self.quantity_entry,
            self.min_quantity_entry,
            self.category_combobox
        ]
        for widget in widgets:
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(state=state)
            elif isinstance(widget, ctk.CTkComboBox):
                widget.configure(state=state)
    
    def load_product(self, product_id=None):
        """Load product data into form"""
        try:
            if not product_id:
                product_id = self.id_entry.get().strip()
            
            if not product_id:
                messagebox.showerror("Error", "Please enter a product ID")
                return
            
            product = self.product_manager.get_product(product_id)
            if product:
                self.set_fields_state("normal")
                self.id_entry.delete(0, 'end')
                self.id_entry.insert(0, str(product[0]))
                self.sku_entry.delete(0, 'end')
                self.sku_entry.insert(0, product[1])
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, product[2])
                self.description_entry.delete(0, 'end')
                self.description_entry.insert(0, product[3])
                self.price_entry.delete(0, 'end')
                self.price_entry.insert(0, str(product[4]))
                self.quantity_entry.delete(0, 'end')
                self.quantity_entry.insert(0, str(product[5]))
                self.min_quantity_entry.delete(0, 'end')
                self.min_quantity_entry.insert(0, str(product[6]))
                self.category_combobox.set(product[7])
            else:
                messagebox.showerror("Error", "Product not found")
                self.clear_entries()
                self.set_fields_state("disabled")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID")
            self.clear_entries()
            self.set_fields_state("disabled")
    
    def update_product(self):
        """Update the product"""
        try:
            # Get values from entries
            product_id = int(self.id_entry.get())
            sku = self.sku_entry.get().strip()
            name = self.name_entry.get().strip()
            description = self.description_entry.get().strip()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            min_quantity = int(self.min_quantity_entry.get())
            category = self.category_combobox.get()
            
            # Validate SKU format
            if not self.product_manager.validate_sku(sku):
                messagebox.showerror("Error", "Invalid SKU format. Must be 2-3 uppercase letters followed by 3 digits.")
                return
            
            # Check if SKU is unique (excluding current product)
            if not self.product_manager.is_sku_unique(sku, product_id):
                messagebox.showerror("Error", "SKU already exists.")
                return
            
            # Update product
            if self.product_manager.update_product(product_id, sku, name, description, price, quantity, min_quantity, category):
                messagebox.showinfo("Success", "Product updated successfully!")
                self.clear_entries()
                self.set_fields_state("disabled")
                if self.refresh_callback:
                    self.refresh_callback()
        
        except ValueError as e:
            messagebox.showerror("Error", "Please check your input values.")
    
    def clear_entries(self):
        """Clear all entry fields"""
        self.id_entry.delete(0, 'end')
        self.sku_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.min_quantity_entry.delete(0, 'end')
        # Get the values using get() method and set the first value if available
        values = self.category_combobox.get()
        if values:
            self.category_combobox.set(self.product_manager.categories[0][1] if self.product_manager.categories else '')

class DeleteForm(BaseForm):
    def __init__(self, parent, product_manager, refresh_callback):
        super().__init__(parent, product_manager, refresh_callback)
        
        # Title
        ctk.CTkLabel(self, text="Delete Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        # ID Field
        ctk.CTkLabel(self, text="ID:").pack(pady=5, padx=10, anchor="w")
        self.id_entry = ctk.CTkEntry(self)
        self.id_entry.pack(pady=5, padx=10, fill="x")
        
        # Delete Button
        ctk.CTkButton(
            self,
            text="Delete",
            command=self.delete_product,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(pady=10, padx=10, fill="x")
    
    def delete_product(self):
        """Delete a product"""
        try:
            product_id = int(self.id_entry.get().strip())
            
            # Get product details for confirmation
            product = self.product_manager.get_product(product_id)
            if not product:
                messagebox.showerror("Error", "Product not found")
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product {product[1]}?"):
                if self.product_manager.delete_product(product_id):
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.id_entry.delete(0, 'end')
                    if self.refresh_callback:
                        self.refresh_callback()
        
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID")

class SearchForm(BaseForm):
    def __init__(self, parent, product_manager, refresh_callback=None):
        super().__init__(parent, product_manager, refresh_callback)
        
        # Create search frame
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=5, pady=5)

        # Search row
        search_row = ctk.CTkFrame(search_frame)
        search_row.pack(fill="x", padx=5, pady=(5,0))
        
        ctk.CTkLabel(search_row, text="Search:").pack(side="left", padx=(5,2))
        self.search_entry = ctk.CTkEntry(search_row, width=400)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Search button
        search_btn = ctk.CTkButton(
            search_row, 
            text="Search", 
            command=self.search_products,
            width=100
        )
        search_btn.pack(side="right", padx=5)

        # Filters row
        filters_row = ctk.CTkFrame(search_frame)
        filters_row.pack(fill="x", padx=5, pady=5)

        # Category filter
        ctk.CTkLabel(filters_row, text="Category:").pack(side="left", padx=(5,2))
        categories = ['All'] + [cat[1] for cat in self.product_manager.categories]
        self.category_combo = ctk.CTkComboBox(
            filters_row, 
            values=categories,
            width=150,
            command=lambda _: self.search_products()
        )
        self.category_combo.set("All")
        self.category_combo.pack(side="left", padx=5)

        # Sort by filter
        ctk.CTkLabel(filters_row, text="Sort by:").pack(side="left", padx=(15,2))
        sort_options = [
            "Name (A-Z)", 
            "Name (Z-A)", 
            "Price (Low-High)", 
            "Price (High-Low)",
            "Stock (Low-High)",
            "Stock (High-Low)"
        ]
        self.sort_combo = ctk.CTkComboBox(
            filters_row, 
            values=sort_options,
            width=150,
            command=lambda _: self.search_products()
        )
        self.sort_combo.set("Name (A-Z)")
        self.sort_combo.pack(side="left", padx=5)

        # Stock status filter
        ctk.CTkLabel(filters_row, text="Stock Status:").pack(side="left", padx=(15,2))
        stock_options = ["All", "In Stock", "Low Stock"]
        self.stock_combo = ctk.CTkComboBox(
            filters_row, 
            values=stock_options,
            width=150,
            command=lambda _: self.search_products()
        )
        self.stock_combo.set("All")
        self.stock_combo.pack(side="left", padx=5)

        # Bind events
        self.search_entry.bind('<Return>', lambda e: self.search_products())

    def search_products(self):
        """Search for products"""
        search_params = {
            'search_term': self.search_entry.get().strip(),
            'category': self.category_combo.get(),
            'stock_status': self.stock_combo.get(),
            'sort_by': self.sort_combo.get()
        }
        
        # Store search parameters
        self.product_manager.current_search = search_params
        
        # Refresh the table
        if self.refresh_callback:
            self.refresh_callback()
