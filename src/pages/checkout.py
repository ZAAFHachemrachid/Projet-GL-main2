import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from src.database.db_config import get_db_connection
import json
from datetime import datetime
import os

class CheckoutFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.parent = parent  # Store parent reference
        self.cart_items = []  # List to store cart items
        
        # Configure grid with better spacing
        self.grid_columnconfigure(0, weight=4)  # Products list (wider)
        self.grid_columnconfigure(1, weight=3)  # Cart (narrower)
        self.grid_rowconfigure(0, weight=1)     # Make the main content expandable
        
        # Left side - Products List
        self.products_frame = ctk.CTkFrame(self)
        self.products_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.products_frame.grid_rowconfigure(2, weight=1)  # Make the treeview expandable
        
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

        # Products table with scrollbar
        table_frame = ctk.CTkFrame(self.products_frame)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        columns = ('ID', 'Name', 'Price', 'Stock')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.products_tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.products_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        self.products_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Define headings with better widths
        self.products_tree.heading('ID', text='ID', anchor='w')
        self.products_tree.heading('Name', text='Name', anchor='w')
        self.products_tree.heading('Price', text='Price', anchor='e')
        self.products_tree.heading('Stock', text='Stock', anchor='e')
        
        self.products_tree.column('ID', width=50, minwidth=50)
        self.products_tree.column('Name', width=200, minwidth=150)
        self.products_tree.column('Price', width=100, minwidth=80)
        self.products_tree.column('Stock', width=80, minwidth=60)
        
        self.products_tree.pack(fill="both", expand=True)
        
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
        self.cart_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Cart title
        ctk.CTkLabel(
            self.cart_frame,
            text="Shopping Cart",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Cart table with scrollbar
        cart_table_frame = ctk.CTkFrame(self.cart_frame)
        cart_table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        cart_columns = ('Name', 'Quantity', 'Price', 'Total')
        self.cart_tree = ttk.Treeview(cart_table_frame, columns=cart_columns, show='headings', selectmode='browse')
        
        # Add scrollbars for cart
        cart_y_scrollbar = ttk.Scrollbar(cart_table_frame, orient="vertical", command=self.cart_tree.yview)
        cart_y_scrollbar.pack(side="right", fill="y")
        cart_x_scrollbar = ttk.Scrollbar(cart_table_frame, orient="horizontal", command=self.cart_tree.xview)
        cart_x_scrollbar.pack(side="bottom", fill="x")
        
        self.cart_tree.configure(yscrollcommand=cart_y_scrollbar.set, xscrollcommand=cart_x_scrollbar.set)
        
        # Define cart headings with better alignment
        self.cart_tree.heading('Name', text='Name', anchor='w')
        self.cart_tree.heading('Quantity', text='Qty', anchor='e')
        self.cart_tree.heading('Price', text='Price', anchor='e')
        self.cart_tree.heading('Total', text='Total', anchor='e')
        
        self.cart_tree.column('Name', width=150, minwidth=100)
        self.cart_tree.column('Quantity', width=70, minwidth=50)
        self.cart_tree.column('Price', width=80, minwidth=70)
        self.cart_tree.column('Total', width=100, minwidth=80)
        
        self.cart_tree.pack(fill="both", expand=True)
        
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
        
        # Action buttons frame with better layout
        action_buttons_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        action_buttons_frame.pack(pady=(10,5), fill="x")
        
        # Purchase button
        ctk.CTkButton(
            action_buttons_frame,
            text="Complete Purchase",
            command=self.complete_purchase,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5, expand=True)
        
        # Cancel button
        ctk.CTkButton(
            action_buttons_frame,
            text="Cancel",
            command=self.cancel_purchase,
            fg_color="#ff5252",
            hover_color="#ff0000"
        ).pack(side="left", padx=5, expand=True)
        
        # Save for later button
        ctk.CTkButton(
            action_buttons_frame,
            text="Save Cart",
            command=self.save_cart,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=5, expand=True)
        
        # Load saved cart button
        ctk.CTkButton(
            action_buttons_frame,
            text="Load Saved",
            command=self.load_saved_cart,
            fg_color="#2196F3",
            hover_color="#1976D2"
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
            
            # Find or create user
            cursor.execute("SELECT id, loyalty_points, total_spent FROM users WHERE name = ?", (buyer,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                current_points = user[1]
                current_spent = user[2]
            else:
                # Create new user with default admin as creator
                cursor.execute("INSERT INTO users (name, created_by) VALUES (?, 1)", (buyer,))
                user_id = cursor.lastrowid
                current_points = 0
                current_spent = 0.0
            
            # Calculate new loyalty points (10 points per $100 spent)
            new_points = int((total_amount / 100) * 10)
            total_points = current_points + new_points
            total_spent = current_spent + total_amount
            
            # Update user's loyalty points and total spent
            cursor.execute("""
                UPDATE users 
                SET loyalty_points = ?, total_spent = ?
                WHERE id = ?
            """, (total_points, total_spent, user_id))
            
            # Create purchase record
            cursor.execute("""
                INSERT INTO purchases (user_id, total_amount, points_earned, created_by)
                VALUES (?, ?, ?, 1)
            """, (user_id, total_amount, new_points))
            
            purchase_id = cursor.lastrowid
            
            # Record individual purchase items
            for item in self.cart_items:
                item_total = item['quantity'] * item['price']
                cursor.execute("""
                    INSERT INTO purchase_details (
                        purchase_id, 
                        product_id, 
                        quantity, 
                        unit_price, 
                        total_price
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    purchase_id, 
                    item['id'], 
                    item['quantity'], 
                    item['price'],
                    item_total
                ))
                
                # Update product quantities
                cursor.execute("""
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (item['quantity'], item['id']))
            
            conn.commit()
            
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
                self.parent.show_content('dashboard')
            
        except Exception as e:
            print(f"Error completing purchase: {e}")
            messagebox.showerror("Error", f"Error completing purchase: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    
    def cancel_purchase(self):
        if messagebox.askyesno("Cancel Purchase", "Are you sure you want to cancel this purchase?"):
            self.cart_items = []
            self.update_cart_display()
            self.buyer_name.delete(0, 'end')

    def save_cart(self):
        """Save the current cart as a markdown file"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty")
            return
            
        try:
            # Create saves directory if it doesn't exist
            saves_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
            os.makedirs(saves_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cart_{timestamp}.md"
            filepath = os.path.join(saves_dir, filename)
            
            # Calculate total
            total = sum(item['quantity'] * item['price'] for item in self.cart_items)
            
            # Create markdown content
            content = f"# Saved Cart - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += "## Items\n\n"
            content += "| Product | Quantity | Price | Total |\n"
            content += "|---------|-----------|-------|-------|\n"
            
            for item in self.cart_items:
                item_total = item['quantity'] * item['price']
                content += f"| {item['name']} | {item['quantity']} | ${item['price']:.2f} | ${item_total:.2f} |\n"
            
            content += f"\n## Total Amount: ${total:.2f}\n"
            
            # Add JSON data for loading
            content += "\n<cart_data>\n"
            content += json.dumps(self.cart_items, indent=2)
            content += "\n</cart_data>"
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Success", f"Cart saved successfully to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cart: {str(e)}")
    
    def load_saved_cart(self):
        """Show a window to select and load a saved cart"""
        # Create saves directory if it doesn't exist
        saves_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
        os.makedirs(saves_dir, exist_ok=True)
        
        # Create selection window
        select_window = ctk.CTkToplevel(self)
        select_window.title("Select Saved Cart")
        select_window.geometry("600x400")
        select_window.grab_set()  # Make window modal
        
        # Create frame for content
        content_frame = ctk.CTkFrame(select_window)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Label
        ctk.CTkLabel(
            content_frame,
            text="Select a Saved Cart",
            font=("Arial", 16, "bold")
        ).pack(pady=(0,10))
        
        # Create frame for cart list
        list_frame = ctk.CTkFrame(content_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for saved carts
        columns = ('Filename', 'Date', 'Items', 'Total')
        cart_list = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=cart_list.yview)
        scrollbar.pack(side="right", fill="y")
        cart_list.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        cart_list.heading('Filename', text='Filename')
        cart_list.heading('Date', text='Date')
        cart_list.heading('Items', text='Items')
        cart_list.heading('Total', text='Total')
        
        cart_list.column('Filename', width=150)
        cart_list.column('Date', width=150)
        cart_list.column('Items', width=100)
        cart_list.column('Total', width=100)
        
        cart_list.pack(fill="both", expand=True)
        
        # Load cart files
        cart_files = []
        for filename in os.listdir(saves_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(saves_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract cart data
                        start = content.find("<cart_data>") + len("<cart_data>")
                        end = content.find("</cart_data>")
                        cart_data = json.loads(content[start:end])
                        
                        # Calculate totals
                        total = sum(item['quantity'] * item['price'] for item in cart_data)
                        num_items = sum(item['quantity'] for item in cart_data)
                        
                        # Get file date from filename
                        date_str = filename[5:-3]  # Remove 'cart_' and '.md'
                        date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                        
                        cart_files.append({
                            'filename': filename,
                            'filepath': filepath,
                            'date': date.strftime("%Y-%m-%d %H:%M:%S"),
                            'items': num_items,
                            'total': total,
                            'cart_data': cart_data
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        # Sort by date (newest first)
        cart_files.sort(key=lambda x: x['filename'], reverse=True)
        
        # Add to treeview
        for cart in cart_files:
            cart_list.insert('', 'end', values=(
                cart['filename'],
                cart['date'],
                f"{cart['items']} items",
                f"${cart['total']:.2f}"
            ))
        
        def load_selected_cart():
            selection = cart_list.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a cart to load")
                return
                
            selected_idx = cart_list.index(selection[0])
            selected_cart = cart_files[selected_idx]
            
            try:
                # Verify stock availability
                conn = get_db_connection()
                cursor = conn.cursor()
                
                for item in selected_cart['cart_data']:
                    cursor.execute("SELECT quantity FROM products WHERE id = ?", (item['id'],))
                    result = cursor.fetchone()
                    if not result:
                        messagebox.showwarning(
                            "Warning", 
                            f"Product {item['name']} no longer exists in the database"
                        )
                        return
                    
                    current_stock = result[0]
                    if current_stock < item['quantity']:
                        messagebox.showwarning(
                            "Warning", 
                            f"Not enough stock for {item['name']}. Available: {current_stock}"
                        )
                        return
                
                # Load the cart
                self.cart_items = selected_cart['cart_data']
                self.update_cart_display()
                select_window.destroy()
                messagebox.showinfo("Success", "Cart loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load cart: {str(e)}")
            finally:
                if conn:
                    conn.close()
        
        def delete_selected_cart():
            selection = cart_list.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a cart to delete")
                return
                
            selected_idx = cart_list.index(selection[0])
            selected_cart = cart_files[selected_idx]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_cart['filename']}?"):
                try:
                    # Delete the file
                    os.remove(selected_cart['filepath'])
                    
                    # Remove from treeview and cart_files
                    cart_list.delete(selection[0])
                    cart_files.pop(selected_idx)
                    
                    messagebox.showinfo("Success", "Cart deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete cart: {str(e)}")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(pady=10, fill="x")
        
        # Load button
        ctk.CTkButton(
            buttons_frame,
            text="Load Selected Cart",
            command=load_selected_cart,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5, expand=True)
        
        # Delete button
        ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            command=delete_selected_cart,
            fg_color="#ff9800",
            hover_color="#f57c00"
        ).pack(side="left", padx=5, expand=True)
        
        # Cancel button
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=select_window.destroy,
            fg_color="#ff5252",
            hover_color="#ff0000"
        ).pack(side="left", padx=5, expand=True)
