import customtkinter as ctk
from tkinter import ttk, messagebox
from src.database.db_config import get_db_connection

class CheckoutFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.parent = parent  # Store parent reference
        self.cart_items = []  # List to store cart items
        
        # Configure grid
        self.grid_columnconfigure(0, weight=3)  # Products list (wider)
        self.grid_columnconfigure(1, weight=2)  # Cart (narrower)
        
        # Left side - Products List
        self.products_frame = ctk.CTkFrame(self)
        self.products_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Products title
        title_frame = ctk.CTkFrame(self.products_frame, fg_color="transparent")
        title_frame.pack(pady=(10,5), fill="x")
        
        ctk.CTkLabel(
            title_frame,
            text="Available Products",
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(self.products_frame)
        search_frame.pack(pady=5, padx=10, fill="x")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search products...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(5,10))
        
        ctk.CTkButton(
            search_frame,
            text="Search",
            width=80,
            command=self.search_products
        ).pack(side="left")
        
        ctk.CTkButton(
            search_frame,
            text="Clear",
            width=80,
            command=self.refresh_products
        ).pack(side="left", padx=5)

        # Products table
        columns = ('ID', 'Name', 'Price', 'Stock')
        self.products_tree = ttk.Treeview(self.products_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        self.products_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Add to cart frame
        add_frame = ctk.CTkFrame(self.products_frame)
        add_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(add_frame, text="Quantity:").pack(side="left", padx=5)
        self.quantity_entry = ctk.CTkEntry(add_frame, width=100)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.insert(0, "1")
        
        ctk.CTkButton(
            add_frame,
            text="Add to Cart",
            command=self.add_to_cart
        ).pack(side="left", padx=5)
        
        # Right side - Cart
        self.cart_frame = ctk.CTkFrame(self)
        self.cart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Cart title
        ctk.CTkLabel(
            self.cart_frame,
            text="Shopping Cart",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Cart table
        cart_columns = ('Name', 'Quantity', 'Price', 'Total')
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=cart_columns, show='headings')
        
        # Define cart headings
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
        
        self.cart_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Remove from cart button
        ctk.CTkButton(
            self.cart_frame,
            text="Remove Selected Item",
            command=self.remove_from_cart,
            fg_color="#ff9800",
            hover_color="#f57c00"
        ).pack(pady=5)
        
        # Total amount label
        self.total_label = ctk.CTkLabel(
            self.cart_frame,
            text="Total: $0.00",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack(pady=5)
        
        # Buyer name entry
        self.buyer_name = ctk.CTkEntry(
            self.cart_frame,
            placeholder_text="Buyer Name"
        )
        self.buyer_name.pack(pady=5, padx=10, fill="x")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        buttons_frame.pack(pady=10, fill="x")
        
        # Purchase button
        ctk.CTkButton(
            buttons_frame,
            text="Complete Purchase",
            command=self.complete_purchase,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5, expand=True)
        
        # Cancel button
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.cancel_purchase,
            fg_color="#ff5252",
            hover_color="#ff0000"
        ).pack(side="left", padx=5, expand=True)
        
        # Load initial data
        self.refresh_products()
    
    def refresh_products(self):
        """Refresh the products list"""
        # Clear search entry
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, 'end')
            
        # Clear the current table
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, quantity FROM products")
            products = cursor.fetchall()
            
            for product in products:
                self.products_tree.insert('', 'end', values=product)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def search_products(self):
        """Search products based on search entry"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear the current table
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Search in name and description
            cursor.execute("""
                SELECT id, name, price, quantity 
                FROM products 
                WHERE LOWER(name) LIKE ? OR LOWER(reference) LIKE ?
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            products = cursor.fetchall()
            
            for product in products:
                self.products_tree.insert('', 'end', values=product)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search products: {str(e)}")
        finally:
            if conn:
                conn.close()
                
    def add_to_cart(self):
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be positive")
                return
            
            # Get product details
            product_values = self.products_tree.item(selected_item[0])['values']
            product_id = product_values[0]
            product_name = product_values[1]
            product_price = float(product_values[2])
            available_stock = int(product_values[3])
            
            if quantity > available_stock:
                messagebox.showwarning("Warning", "Not enough stock available")
                return
            
            # Check if item already in cart
            for item in self.cart_items:
                if item['id'] == product_id:
                    new_quantity = item['quantity'] + quantity
                    if new_quantity > available_stock:
                        messagebox.showwarning("Warning", "Not enough stock available")
                        return
                    item['quantity'] = new_quantity
                    self.update_cart_display()
                    return
            
            # Add new item to cart
            self.cart_items.append({
                'id': product_id,
                'name': product_name,
                'price': product_price,
                'quantity': quantity
            })
            
            self.update_cart_display()
            
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity")
    
    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        item_index = self.cart_tree.index(selected_item[0])
        if 0 <= item_index < len(self.cart_items):
            self.cart_items.pop(item_index)
            self.update_cart_display()
    
    def update_cart_display(self):
        # Clear current items
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Calculate total
        total = 0
        
        # Add items to display
        for item in self.cart_items:
            item_total = item['price'] * item['quantity']
            total += item_total
            
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item_total:.2f}"
            ))
        
        # Update total label
        self.total_label.configure(text=f"Total: ${total:.2f}")
    
    def complete_purchase(self):
        """Complete the purchase and record it in the database"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        buyer = self.buyer_name.get().strip()
        if not buyer:
            messagebox.showwarning("Warning", "Please enter buyer name")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Calculate total amount
            total_amount = sum(item['quantity'] * item['price'] for item in self.cart_items)
            print(f"Total amount: {total_amount}")
            
            # Find or create user
            cursor.execute("SELECT id, loyalty_points, total_spent FROM users WHERE name = ?", (buyer,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                current_points = user[1]
                current_spent = user[2]
                print(f"Existing user found - ID: {user_id}, Points: {current_points}, Spent: {current_spent}")
            else:
                cursor.execute("INSERT INTO users (name) VALUES (?)", (buyer,))
                user_id = cursor.lastrowid
                current_points = 0
                current_spent = 0.0
                print(f"New user created - ID: {user_id}")
            
            # Calculate new loyalty points (10 points per $100 spent)
            new_points = int((total_amount / 100) * 10)
            total_points = current_points + new_points
            total_spent = current_spent + total_amount
            print(f"Points calculation - New: {new_points}, Total: {total_points}, Total Spent: {total_spent}")
            
            # Update user's loyalty points and total spent
            cursor.execute("""
                UPDATE users 
                SET loyalty_points = ?, total_spent = ?
                WHERE id = ?
            """, (total_points, total_spent, user_id))
            print("Updated user loyalty points and total spent")
            
            # Create purchase record
            cursor.execute("""
                INSERT INTO purchases (user_id, total_amount, points_earned, created_by)
                VALUES (?, ?, ?, 1)
            """, (user_id, total_amount, new_points))
            
            purchase_id = cursor.lastrowid
            print(f"Created purchase record - ID: {purchase_id}")
            
            # Record individual purchase items
            for item in self.cart_items:
                cursor.execute("""
                    INSERT INTO purchase_items (purchase_id, product_id, quantity, price_per_unit)
                    VALUES (?, ?, ?, ?)
                """, (purchase_id, item['id'], item['quantity'], item['price']))
                print(f"Added purchase item - Product: {item['id']}, Quantity: {item['quantity']}, Price: {item['price']}")
                
                # Update product quantities
                cursor.execute("""
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (item['quantity'], item['id']))
                print(f"Updated product quantity - Product: {item['id']}, Reduced by: {item['quantity']}")
            
            conn.commit()
            print("Transaction committed successfully")
            conn.close()
            
            # Show success message with points earned
            messagebox.showinfo(
                "Success",
                f"Purchase completed successfully!\n\n"
                f"Points earned: {new_points}\n"
                f"Total points: {total_points}"
            )
            
            # Clear cart
            self.cart_items = []
            self.update_cart_display()
            self.refresh_products()
            
            # Refresh dashboard if it exists
            if hasattr(self.parent, 'show_content'):
                print("Refreshing dashboard")
                self.parent.show_content('dashboard')
            
        except Exception as e:
            print(f"Error completing purchase: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error completing purchase: {e}")
    
    def cancel_purchase(self):
        if messagebox.askyesno("Cancel Purchase", "Are you sure you want to cancel this purchase?"):
            self.cart_items = []
            self.update_cart_display()
            self.buyer_name.delete(0, 'end')
