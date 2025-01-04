import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db_config import get_db_connection
import hashlib
import sqlite3

class AdminManagementFrame(ctk.CTkFrame):
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
        
        ctk.CTkLabel(self.create_frame, text="Create Admin", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.username_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Username")
        self.username_entry.pack(pady=5, padx=10, fill="x")
        
        self.password_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5, padx=10, fill="x")
        
        self.confirm_password_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=5, padx=10, fill="x")
        
        self.email_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Email")
        self.email_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_admin).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self.left_container)
        self.update_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Admin", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Admin ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Admin", command=self.load_admin).pack(pady=5)
        
        self.update_username_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Username")
        self.update_username_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_email_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Email")
        self.update_email_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_password_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Password (optional)", show="*")
        self.update_password_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_confirm_password_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Confirm New Password", show="*")
        self.update_confirm_password_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_admin).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self.left_container)
        self.delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Admin", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Admin ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_admin,
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
        
        # Right side - Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ('ID', 'Username', 'Email', 'Created At')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        column_widths = {
            'ID': 50,
            'Username': 150,
            'Email': 200,
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
    
    def create_admin(self):
        """Create a new admin"""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            email = self.email_entry.get().strip()
            
            # Validate input
            if not username or not password or not confirm_password:
                messagebox.showerror("Error", "Username and password are required")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO admin (username, password, email)
                VALUES (?, ?, ?)
            """, (username, hashed_password, email))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Admin created successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating admin: {e}")
    
    def load_admin(self):
        """Load admin details for update"""
        try:
            admin_id = self.update_id_entry.get()
            if not admin_id:
                messagebox.showerror("Error", "Please enter an admin ID")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, email
                FROM admin
                WHERE id = ?
            """, (int(admin_id),))
            
            admin = cursor.fetchone()
            conn.close()
            
            if admin:
                self.update_username_entry.delete(0, 'end')
                self.update_username_entry.insert(0, admin[0])
                self.update_email_entry.delete(0, 'end')
                self.update_email_entry.insert(0, admin[1] or "")
            else:
                messagebox.showerror("Error", "Admin not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading admin: {e}")
    
    def update_admin(self):
        """Update admin details"""
        try:
            admin_id = self.update_id_entry.get()
            new_username = self.update_username_entry.get().strip()
            new_email = self.update_email_entry.get().strip()
            new_password = self.update_password_entry.get()
            confirm_password = self.update_confirm_password_entry.get()
            
            if not admin_id or not new_username:
                messagebox.showerror("Error", "Admin ID and username are required")
                return
            
            if new_password:
                if new_password != confirm_password:
                    messagebox.showerror("Error", "Passwords do not match")
                    return
                
                # Hash new password
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE admin
                    SET username = ?, email = ?, password = ?
                    WHERE id = ?
                """, (new_username, new_email, hashed_password, int(admin_id)))
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE admin
                    SET username = ?, email = ?
                    WHERE id = ?
                """, (new_username, new_email, int(admin_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Admin updated successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating admin: {e}")
    
    def delete_admin(self):
        """Delete an admin"""
        try:
            admin_id = self.delete_id_entry.get()
            if not admin_id:
                messagebox.showerror("Error", "Please enter an admin ID")
                return
            
            # Check if this is the last admin
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM admin")
            admin_count = cursor.fetchone()[0]
            
            if admin_count <= 1:
                messagebox.showerror("Error", "Cannot delete the last admin")
                conn.close()
                return
            
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this admin?"):
                conn.close()
                return
            
            cursor.execute("DELETE FROM admin WHERE id = ?", (int(admin_id),))
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "Admin deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting admin: {e}")
    
    def refresh_table(self):
        """Refresh the admin table"""
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, created_at
                FROM admin
                ORDER BY username
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        """Clear create form entries"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
    
    def clear_update_entries(self):
        """Clear update form entries"""
        self.update_id_entry.delete(0, 'end')
        self.update_username_entry.delete(0, 'end')
        self.update_email_entry.delete(0, 'end')
        self.update_password_entry.delete(0, 'end')
        self.update_confirm_password_entry.delete(0, 'end')
