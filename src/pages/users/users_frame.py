import customtkinter as ctk
from tkinter import ttk, messagebox
from src.database.db_config import get_db_connection
import sqlite3

class UsersFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)  # Left side (forms)
        self.grid_columnconfigure(1, weight=3)  # Right side (table)
        self.grid_rowconfigure(0, weight=1)  # Make row expandable
        
        # Left side container
        self.left_container = ctk.CTkFrame(self)
        self.left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_container.grid_rowconfigure(1, weight=1)  # Make forms row expandable
        self.left_container.grid_columnconfigure(0, weight=1)
        
        # Buttons Frame for switching forms
        self.switch_buttons_frame = ctk.CTkFrame(self.left_container)
        self.switch_buttons_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.switch_buttons_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Create buttons to switch between forms
        ctk.CTkButton(self.switch_buttons_frame, text="Create Form", command=lambda: self.show_form("create")).grid(row=0, column=0, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Update Form", command=lambda: self.show_form("update")).grid(row=0, column=1, padx=2, sticky="ew")
        ctk.CTkButton(self.switch_buttons_frame, text="Delete Form", command=lambda: self.show_form("delete")).grid(row=0, column=2, padx=2, sticky="ew")
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self.left_container)
        self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Name")
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        self.phone_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Phone")
        self.phone_entry.pack(pady=5, padx=10, fill="x")
        
        self.email_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Email")
        self.email_entry.pack(pady=5, padx=10, fill="x")
        
        self.loyalty_points_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Loyalty Points")
        self.loyalty_points_entry.pack(pady=5, padx=10, fill="x")
        self.loyalty_points_entry.insert(0, "0")  # Default value
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_user).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="User ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load User", command=self.load_user).pack(pady=5)
        
        self.update_name_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Name")
        self.update_name_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_phone_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Phone")
        self.update_phone_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_email_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Email")
        self.update_email_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_loyalty_points_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Loyalty Points")
        self.update_loyalty_points_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_user).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete User", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="User ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_user,
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Name', 'Phone', 'Email', 'Loyalty Points', 'Total Spent', 'Created At')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        column_widths = {
            'ID': 50,
            'Name': 150,
            'Phone': 100,
            'Email': 200,
            'Loyalty Points': 100,
            'Total Spent': 100,
            'Created At': 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the table and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Show create form by default
        self.show_form("create")
        
        # Load initial data
        self.refresh_table()
    
    def show_form(self, form_type):
        """Show the selected form"""
        # Hide all forms first
        self.create_frame.grid_remove()
        self.update_frame.grid_remove()
        self.delete_frame.grid_remove()
        
        # Show the selected form
        if form_type == "create":
            self.create_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "update":
            self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        elif form_type == "delete":
            self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    
    def create_user(self):
        """Create a new user"""
        try:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            loyalty_points = self.loyalty_points_entry.get().strip() or "0"
            
            # Validate input
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            try:
                loyalty_points = int(loyalty_points)
                if loyalty_points < 0:
                    messagebox.showerror("Error", "Loyalty points cannot be negative")
                    return
            except ValueError:
                messagebox.showerror("Error", "Loyalty points must be a valid number")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (name, phone, email, loyalty_points, total_spent)
                VALUES (?, ?, ?, ?, 0.0)
            """, (name, phone, email, loyalty_points))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "User created successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Name already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating user: {e}")
    
    def load_user(self):
        """Load user details for update"""
        try:
            user_id = self.update_id_entry.get()
            if not user_id:
                messagebox.showerror("Error", "Please enter a user ID")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, phone, email, loyalty_points
                FROM users
                WHERE id = ?
            """, (int(user_id),))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.update_name_entry.delete(0, 'end')
                self.update_name_entry.insert(0, user[0])
                self.update_phone_entry.delete(0, 'end')
                self.update_phone_entry.insert(0, user[1] or "")
                self.update_email_entry.delete(0, 'end')
                self.update_email_entry.insert(0, user[2] or "")
                self.update_loyalty_points_entry.delete(0, 'end')
                self.update_loyalty_points_entry.insert(0, str(user[3]))
            else:
                messagebox.showerror("Error", "User not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading user: {e}")
    
    def update_user(self):
        """Update user details"""
        try:
            user_id = self.update_id_entry.get()
            new_name = self.update_name_entry.get().strip()
            new_phone = self.update_phone_entry.get().strip()
            new_email = self.update_email_entry.get().strip()
            new_loyalty_points = self.update_loyalty_points_entry.get().strip()
            
            if not user_id or not new_name:
                messagebox.showerror("Error", "User ID and Name are required")
                return
            
            try:
                loyalty_points = int(new_loyalty_points)
                if loyalty_points < 0:
                    messagebox.showerror("Error", "Loyalty points cannot be negative")
                    return
            except ValueError:
                messagebox.showerror("Error", "Loyalty points must be a valid number")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users
                SET name = ?, phone = ?, email = ?, loyalty_points = ?
                WHERE id = ?
            """, (new_name, new_phone, new_email, loyalty_points, int(user_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "User updated successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Name already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating user: {e}")
    
    def delete_user(self):
        """Delete a user"""
        try:
            user_id = self.delete_id_entry.get()
            if not user_id:
                messagebox.showerror("Error", "Please enter a user ID")
                return
            
            # Check if user has any purchases
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM purchase WHERE buyer_id = ?
            """, (int(user_id),))
            
            purchase_count = cursor.fetchone()[0]
            
            if purchase_count > 0:
                if not messagebox.askyesno("Warning", 
                    f"This user has {purchase_count} purchases. Deleting the user will keep the purchase records. Continue?"):
                    conn.close()
                    return
            
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
                conn.close()
                return
            
            cursor.execute("DELETE FROM users WHERE id = ?", (int(user_id),))
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "User deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting user: {e}")
    
    def refresh_table(self):
        """Refresh the user table"""
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, phone, email, loyalty_points, total_spent, created_at
                FROM users
                ORDER BY name
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        """Clear create form entries"""
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.loyalty_points_entry.delete(0, 'end')
        self.loyalty_points_entry.insert(0, "0")  # Reset to default value
    
    def clear_update_entries(self):
        """Clear update form entries"""
        self.update_id_entry.delete(0, 'end')
        self.update_name_entry.delete(0, 'end')
        self.update_phone_entry.delete(0, 'end')
        self.update_email_entry.delete(0, 'end')
        self.update_loyalty_points_entry.delete(0, 'end')
