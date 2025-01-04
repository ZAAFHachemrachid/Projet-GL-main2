import customtkinter as ctk
from tkinter import ttk, messagebox, Menu
import sqlite3
import re
from datetime import datetime
from database.db_config import get_db_connection

class ProductManagementFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Load categories
        self.categories = self.load_categories()
        
        # Add SKU validation pattern
        self.sku_pattern = re.compile(r'^[A-Z]{2,3}\d{3}$')
        
        # Create the left side (forms)
        self.setup_forms()
        
        # Create the right side (table)
        self.setup_table()
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
    
    def setup_forms(self):
        # Left side container
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_container.grid_rowconfigure(1, weight=1)
        self.left_container.grid_columnconfigure(0, weight=1)
        
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
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        ctk.CTkLabel(self.create_frame, text="SKU:").pack(pady=5, padx=10, anchor="w")
        self.sku_entry = ctk.CTkEntry(self.create_frame)
        self.sku_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Name:").pack(pady=5, padx=10, anchor="w")
        self.name_entry = ctk.CTkEntry(self.create_frame)
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Description:").pack(pady=5, padx=10, anchor="w")
        self.description_entry = ctk.CTkEntry(self.create_frame)
        self.description_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Price:").pack(pady=5, padx=10, anchor="w")
        self.price_entry = ctk.CTkEntry(self.create_frame)
        self.price_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Quantity:").pack(pady=5, padx=10, anchor="w")
        self.quantity_entry = ctk.CTkEntry(self.create_frame)
        self.quantity_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Minimum Quantity:").pack(pady=5, padx=10, anchor="w")
        self.min_quantity_entry = ctk.CTkEntry(self.create_frame)
        self.min_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.create_frame, text="Category:").pack(pady=5, padx=10, anchor="w")
        self.category_combobox = ctk.CTkComboBox(self.create_frame, values=[cat[1] for cat in self.categories])
        self.category_combobox.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_product).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        # Create a scrollable frame for the update form
        self.update_scroll_frame = ctk.CTkScrollableFrame(self.update_frame)
        self.update_scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Title
        ctk.CTkLabel(self.update_scroll_frame, text="Update Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        # ID Entry and Load Button Frame
        id_frame = ctk.CTkFrame(self.update_scroll_frame)
        id_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(id_frame, text="ID:").pack(side="left", padx=(0,5))
        self.update_id_entry = ctk.CTkEntry(id_frame, width=120)
        self.update_id_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            id_frame, 
            text="Load Product", 
            command=self.load_product_for_update,
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=5)
        
        # Rest of the form fields (initially disabled)
        self.update_fields_frame = ctk.CTkFrame(self.update_scroll_frame)
        self.update_fields_frame.pack(fill="x", padx=10, pady=5)
        
        # SKU Field
        ctk.CTkLabel(self.update_fields_frame, text="SKU:").pack(pady=5, anchor="w")
        self.update_sku_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_sku_entry.pack(fill="x", pady=5)
        
        # Name Field
        ctk.CTkLabel(self.update_fields_frame, text="Name:").pack(pady=5, anchor="w")
        self.update_name_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_name_entry.pack(fill="x", pady=5)
        
        # Description Field
        ctk.CTkLabel(self.update_fields_frame, text="Description:").pack(pady=5, anchor="w")
        self.update_description_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_description_entry.pack(fill="x", pady=5)
        
        # Price Field
        ctk.CTkLabel(self.update_fields_frame, text="Price:").pack(pady=5, anchor="w")
        self.update_price_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_price_entry.pack(fill="x", pady=5)
        
        # Quantity Field
        ctk.CTkLabel(self.update_fields_frame, text="Quantity:").pack(pady=5, anchor="w")
        self.update_quantity_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_quantity_entry.pack(fill="x", pady=5)
        
        # Min Quantity Field
        ctk.CTkLabel(self.update_fields_frame, text="Minimum Quantity:").pack(pady=5, anchor="w")
        self.update_min_quantity_entry = ctk.CTkEntry(self.update_fields_frame)
        self.update_min_quantity_entry.pack(fill="x", pady=5)
        
        # Category Field
        ctk.CTkLabel(self.update_fields_frame, text="Category:").pack(pady=5, anchor="w")
        self.update_category_combobox = ctk.CTkComboBox(self.update_fields_frame, values=[cat[1] for cat in self.categories])
        self.update_category_combobox.pack(fill="x", pady=5)
        
        # Update Button
        ctk.CTkButton(
            self.update_fields_frame,
            text="Update",
            command=self.update_product,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=10, fill="x")
        
        # Initially disable all fields except ID
        self.set_update_fields_state("disabled")
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        ctk.CTkLabel(self.delete_frame, text="ID:").pack(pady=5, padx=10, anchor="w")
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame)
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_product, hover_color="#8679EAFF").pack(pady=10)
        
        # Search Form
        self.search_frame = ctk.CTkFrame(self.left_container)
        self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.search_frame, text="Search Products", font=("Arial", 16, "bold")).pack(pady=5)
        
        # Search inputs frame
        search_inputs_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        search_inputs_frame.pack(fill="x", pady=(0, 10))
        
        # Search input
        self.search_entry = ctk.CTkEntry(
            search_inputs_frame,
            placeholder_text="Search by product name or reference...",
            width=400
        )
        self.search_entry.pack(pady=5, padx=10, fill="x")
        
        # Category dropdown for search
        self.search_category_var = ctk.StringVar(value="All Categories")
        self.search_category_dropdown = ctk.CTkOptionMenu(
            search_inputs_frame,
            values=["All Categories"] + [cat[1] for cat in self.categories],
            variable=self.search_category_var,
            width=150,
            command=lambda _: self.search_products()  # Trigger search when category changes
        )
        self.search_category_dropdown.pack(pady=5, padx=10, fill="x")
        
        # Stock status dropdown
        self.stock_status_var = ctk.StringVar(value="All")
        self.stock_status_dropdown = ctk.CTkOptionMenu(
            search_inputs_frame,
            values=["All", "In Stock", "Out of Stock"],
            variable=self.stock_status_var,
            width=150,
            command=lambda _: self.search_products()  # Trigger search when stock status changes
        )
        self.stock_status_dropdown.pack(pady=5, padx=10, fill="x")
        
        # Sort by dropdown
        self.sort_var = ctk.StringVar(value="Name (A-Z)")
        self.sort_dropdown = ctk.CTkOptionMenu(
            search_inputs_frame,
            values=["Name (A-Z)", "Name (Z-A)", "Price (Low-High)", "Price (High-Low)"],
            variable=self.sort_var,
            width=150,
            command=lambda _: self.search_products()  # Trigger search when sort option changes
        )
        self.sort_dropdown.pack(pady=5, padx=10, fill="x")
        
        # Price range frame
        price_frame = ctk.CTkFrame(search_inputs_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=5)
        
        price_label = ctk.CTkLabel(price_frame, text="Price Range:", anchor="w")
        price_label.pack(side="left", padx=(10, 5))
        
        self.search_min_price = ctk.CTkEntry(
            price_frame,
            placeholder_text="Min Price",
            width=150
        )
        self.search_min_price.pack(side="left", padx=5)
        
        self.search_max_price = ctk.CTkEntry(
            price_frame,
            placeholder_text="Max Price",
            width=150
        )
        self.search_max_price.pack(side="left", padx=5)
        
        # Search buttons
        search_btn = ctk.CTkButton(
            search_inputs_frame,
            text="Search",
            fg_color="#6c5ce7",
            hover_color="#5b4cc7",
            command=self.search_products
        )
        search_btn.pack(pady=5, padx=10, fill="x")
        
        reset_btn = ctk.CTkButton(
            search_inputs_frame,
            text="Reset Search",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.reset_search
        )
        reset_btn.pack(pady=5, padx=10, fill="x")
    
    def setup_table(self):
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Define columns with their properties
        self.columns = {
            'ID': {'width': 50, 'anchor': 'center'},
            'Reference': {'width': 100, 'anchor': 'w'},
            'Name': {'width': 200, 'anchor': 'w'},
            'Description': {'width': 300, 'anchor': 'w'},
            'Price': {'width': 80, 'anchor': 'e'},
            'Quantity': {'width': 80, 'anchor': 'center'},
            'Min Quantity': {'width': 80, 'anchor': 'center'},
            'Category': {'width': 100, 'anchor': 'w'},
            'Created At': {'width': 150, 'anchor': 'w'},
            'Created By': {'width': 100, 'anchor': 'w'}
        }
        
        # Create and configure the treeview
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=list(self.columns.keys()),
            show='headings',
            selectmode='browse'
        )
        
        # Configure the treeview style
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Configure columns and headings
        for col, props in self.columns.items():
            self.tree.heading(
                col,
                text=col,
                command=lambda c=col: self.sort_table_by_column(c)
            )
            self.tree.column(
                col,
                width=props['width'],
                anchor=props['anchor'],
                minwidth=50
            )
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Grid layout for table and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Create context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy SKU", command=self.copy_sku)
    
    def load_categories(self):
        """Load categories from database"""
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, name FROM category ORDER BY name")
                return cursor.fetchall()
            except sqlite3.Error as err:
                messagebox.showerror("Error", f"Error loading categories: {err}")
                return []
            finally:
                conn.close()
        return []
    
    def create_product(self):
        """Create a new product"""
        # Get form values
        sku = self.sku_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        min_quantity = self.min_quantity_entry.get().strip()
        category = self.category_combobox.get()
        
        # Validate inputs
        if not all([sku, name, price, quantity, min_quantity, category]):
            messagebox.showwarning("Warning", "All fields are required")
            return
        
        # Validate SKU format
        if not self.validate_sku(sku):
            return
        
        # Check if SKU is unique
        if not self.is_sku_unique(sku):
            return
        
        try:
            # Convert numeric values
            price = float(price)
            quantity = int(quantity)
            min_quantity = int(min_quantity)
            
            if price <= 0:
                messagebox.showwarning("Warning", "Price must be positive")
                return
            
            if quantity < 0:
                messagebox.showwarning("Warning", "Quantity cannot be negative")
                return
            
            if min_quantity < 0:
                messagebox.showwarning("Warning", "Minimum quantity cannot be negative")
                return
            
            # Get category ID
            category_id = self.get_category_id(category)
            if not category_id:
                return
            
            # Insert product
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO products (
                        reference, name, description, price, quantity, min_quantity,
                        category_id, created_by, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (sku, name, description, price, quantity, min_quantity, category_id, 1))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product created successfully")
                self.clear_create_entries()
                self.refresh_table()
                
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numeric values")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error creating product: {err}")
    
    def update_product(self):
        """Update an existing product"""
        # Get form values
        product_id = self.update_id_entry.get().strip()
        if not product_id:
            messagebox.showwarning("Warning", "Please enter a product ID")
            return
        
        try:
            product_id = int(product_id)
            sku = self.update_sku_entry.get().strip().upper()
            name = self.update_name_entry.get().strip()
            description = self.update_description_entry.get().strip()
            price = self.update_price_entry.get().strip()
            quantity = self.update_quantity_entry.get().strip()
            min_quantity = self.update_min_quantity_entry.get().strip()
            category = self.update_category_combobox.get()
            
            # Validate inputs
            if not all([sku, name, price, quantity, min_quantity, category]):
                messagebox.showwarning("Warning", "All fields are required")
                return
            
            # Validate SKU format
            if not self.validate_sku(sku):
                return
            
            # Check if SKU is unique (excluding current product)
            if not self.is_sku_unique(sku, product_id):
                return
            
            # Convert numeric values
            price = float(price)
            quantity = int(quantity)
            min_quantity = int(min_quantity)
            
            if price <= 0:
                messagebox.showwarning("Warning", "Price must be positive")
                return
            
            if quantity < 0:
                messagebox.showwarning("Warning", "Quantity cannot be negative")
                return
            
            if min_quantity < 0:
                messagebox.showwarning("Warning", "Minimum quantity cannot be negative")
                return
            
            # Get category ID
            category_id = self.get_category_id(category)
            if not category_id:
                return
            
            # Update product
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE products 
                    SET reference = ?, name = ?, description = ?, price = ?,
                        quantity = ?, min_quantity = ?, category_id = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (sku, name, description, price, quantity, min_quantity, category_id, product_id))
                
                if cursor.rowcount == 0:
                    messagebox.showwarning("Warning", "Product not found")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Product updated successfully")
                    self.clear_update_entries()
                    self.refresh_table()
                
                conn.close()
                
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numeric values")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error updating product: {err}")
    
    def delete_product(self):
        """Delete a product"""
        product_id = self.delete_id_entry.get().strip()
        if not product_id:
            messagebox.showwarning("Warning", "Please enter a product ID")
            return
        
        try:
            product_id = int(product_id)
            
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
                return
            
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                
                if cursor.rowcount == 0:
                    messagebox.showwarning("Warning", "Product not found")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Product deleted successfully")
                    self.delete_id_entry.delete(0, 'end')
                    self.refresh_table()
                
                conn.close()
                
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid product ID")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error deleting product: {err}")
    
    def refresh_table(self):
        """Refresh table data with improved formatting"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.reference, p.name, p.description, p.price,
                           p.quantity, p.min_quantity, c.name as category_name,
                           p.created_at, a.username as created_by
                    FROM products p
                    LEFT JOIN category c ON p.category_id = c.id
                    LEFT JOIN admin a ON p.created_by = a.id
                    ORDER BY p.name
                """)
                
                for row in cursor.fetchall():
                    try:
                        # Format price as currency
                        price = f"${row[4]:.2f}"
                        
                        # Format dates (handle potential NULL or invalid dates)
                        try:
                            created_at = datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M') if row[8] else ''
                        except (ValueError, TypeError):
                            created_at = ''
                        
                        # Add row to table with safe value handling
                        values = [
                            row[0] or '',          # ID
                            row[1] or '',          # Reference
                            row[2] or '',          # Name
                            row[3] or '',          # Description
                            price,                 # Price
                            row[5] or 0,           # Quantity
                            row[6] or 0,           # Min Quantity
                            row[7] or '',          # Category
                            created_at,            # Created At
                            row[9] or ''           # Created By
                        ]
                        self.tree.insert('', 'end', values=values)
                    except Exception as row_err:
                        print(f"Error processing row {row}: {row_err}")
                        continue
                
                conn.close()
                
        except Exception as err:
            print(f"Error refreshing table: {err}")
            messagebox.showerror("Error", f"Error refreshing table: {err}")
    
    def show_form(self, form_type):
        # Hide all forms first
        self.create_frame.grid_remove()
        self.update_frame.grid_remove()
        self.delete_frame.grid_remove()
        self.search_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "search":
            self.search_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def get_category_id(self, category_name):
        for cat_id, name in self.categories:
            if name == category_name:
                return cat_id
        return None
    
    def validate_sku(self, sku):
        """Validate SKU format (2-3 letters followed by 3 digits)"""
        if not sku:
            raise ValueError("SKU cannot be empty")
        if not self.sku_pattern.match(sku.upper()):
            raise ValueError("SKU must be 2-3 letters followed by 3 digits (e.g., HM001)")
        return sku.upper()
    
    def is_sku_unique(self, sku, exclude_id=None):
        """Check if SKU is unique in database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if exclude_id:
                cursor.execute("SELECT COUNT(*) FROM products WHERE reference = ? AND id != ?", (sku, exclude_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM products WHERE reference = ?", (sku,))
            count = cursor.fetchone()[0]
            conn.close()
            return count == 0
        except Exception as e:
            print(f"Error checking SKU uniqueness: {e}")
            return False
    
    def suggest_next_sku(self, prefix):
        """Suggest next available SKU for a given prefix"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reference FROM products WHERE reference LIKE ? ORDER BY reference DESC LIMIT 1",
                (f"{prefix}%",)
            )
            last_sku = cursor.fetchone()
            conn.close()
            
            if not last_sku:
                return f"{prefix}001"
            
            last_num = int(last_sku[0][-3:])
            next_num = last_num + 1
            if next_num > 999:
                raise ValueError("SKU sequence exhausted for this prefix")
            return f"{prefix}{next_num:03d}"
        except Exception as e:
            print(f"Error suggesting next SKU: {e}")
            return None
    
    def clear_create_entries(self):
        self.sku_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.min_quantity_entry.delete(0, 'end')
        self.category_combobox.set('')
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_sku_entry.delete(0, 'end')
        self.update_name_entry.delete(0, 'end')
        self.update_description_entry.delete(0, 'end')
        self.update_price_entry.delete(0, 'end')
        self.update_quantity_entry.delete(0, 'end')
        self.update_min_quantity_entry.delete(0, 'end')
        self.update_category_combobox.set('')
    
    def set_update_fields_state(self, state):
        """Enable or disable update form fields"""
        fields = [
            self.update_sku_entry,
            self.update_name_entry,
            self.update_description_entry,
            self.update_price_entry,
            self.update_quantity_entry,
            self.update_min_quantity_entry,
            self.update_category_combobox
        ]
        for field in fields:
            field.configure(state=state)

    def search_products(self):
        """Search products based on filters"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT p.id, p.reference, p.name, p.description, p.price,
                       p.quantity, p.min_quantity, c.name as category_name,
                       p.created_at, a.username as created_by
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                LEFT JOIN admin a ON p.created_by = a.id
                WHERE 1=1
            """
            params = []
            
            # Search term filter
            search_term = self.search_entry.get().strip()
            if search_term:
                query += """ AND (
                    LOWER(p.name) LIKE LOWER(?) OR 
                    LOWER(p.reference) LIKE LOWER(?) OR
                    LOWER(COALESCE(c.name, '')) LIKE LOWER(?)
                )"""
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern] * 3)
            
            # Category filter
            category = self.search_category_var.get()
            if category and category != "All Categories":
                query += " AND c.name = ?"
                params.append(category)
            
            # Stock status filter
            stock_status = self.stock_status_var.get()
            if stock_status == "In Stock":
                query += " AND p.quantity > 0"
            elif stock_status == "Out of Stock":
                query += " AND p.quantity = 0"
            
            # Price range filter
            min_price = self.search_min_price.get().strip()
            if min_price:
                try:
                    min_price = float(min_price)
                    query += " AND p.price >= ?"
                    params.append(min_price)
                except ValueError:
                    messagebox.showerror("Error", "Invalid minimum price")
                    return
            
            max_price = self.search_max_price.get().strip()
            if max_price:
                try:
                    max_price = float(max_price)
                    query += " AND p.price <= ?"
                    params.append(max_price)
                except ValueError:
                    messagebox.showerror("Error", "Invalid maximum price")
                    return
            
            # Apply sort
            sort_option = self.sort_var.get()
            if sort_option == "Name (A-Z)":
                query += " ORDER BY p.name ASC"
            elif sort_option == "Name (Z-A)":
                query += " ORDER BY p.name DESC"
            elif sort_option == "Price (Low-High)":
                query += " ORDER BY p.price ASC"
            elif sort_option == "Price (High-Low)":
                query += " ORDER BY p.price DESC"
            
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            # Clear the table
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert products with formatting
            for row in products:
                # Format price as currency
                price = f"${row[4]:.2f}"
                
                # Format dates
                created_at = datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                
                self.tree.insert('', 'end', values=(
                    row[0],          # ID
                    row[1],          # Reference
                    row[2],          # Name
                    row[3],          # Description
                    price,           # Price
                    row[5],          # Quantity
                    row[6],          # Min Quantity
                    row[7],          # Category
                    created_at,      # Created At
                    row[9]           # Created By
                ))
            
            conn.close()
            
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error searching products: {err}")
    
    def load_product_for_update(self):
        """Load product data into update form"""
        try:
            product_id = self.update_id_entry.get().strip()
            if not product_id:
                messagebox.showerror("Error", "Please enter a product ID")
                return
            
            try:
                product_id = int(product_id)
            except ValueError:
                messagebox.showerror("Error", "Product ID must be a number")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.reference, p.name, p.description, p.price, p.quantity,
                       p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE p.id = ?
            """, (product_id,))
            
            product = cursor.fetchone()
            conn.close()
            
            if product:
                # Enable fields for editing
                self.set_update_fields_state("normal")
                
                # Fill in the fields
                self.update_sku_entry.delete(0, 'end')
                self.update_sku_entry.insert(0, product[0])
                
                self.update_name_entry.delete(0, 'end')
                self.update_name_entry.insert(0, product[1])
                
                self.update_description_entry.delete(0, 'end')
                self.update_description_entry.insert(0, product[2] if product[2] else '')
                
                self.update_price_entry.delete(0, 'end')
                self.update_price_entry.insert(0, str(product[3]))
                
                self.update_quantity_entry.delete(0, 'end')
                self.update_quantity_entry.insert(0, str(product[4]))
                
                self.update_min_quantity_entry.delete(0, 'end')
                self.update_min_quantity_entry.insert(0, str(product[5]))
                
                self.update_category_combobox.set(product[6] if product[6] else '')
                
                messagebox.showinfo("Success", "Product loaded successfully")
            else:
                messagebox.showerror("Error", "Product not found")
                self.set_update_fields_state("disabled")
                self.clear_update_entries()
                
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error loading product: {err}")
            self.set_update_fields_state("disabled")
            self.clear_update_entries()
