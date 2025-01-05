import re
from tkinter import messagebox
from src.database.db_config import get_db_connection

class ProductManager:
    def __init__(self):
        self.sku_pattern = re.compile(r'^[A-Z]{2,3}\d{3}$')
        self.categories = []  # Initialize as empty list
        self.current_search = None  # Initialize current search parameters
        self.load_categories()  # Load categories
    
    def load_categories(self):
        """Load all categories from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category ORDER BY name")
            self.categories = cursor.fetchall()
            conn.close()
            return self.categories
        except Exception as e:
            messagebox.showerror("Error", f"Error loading categories: {e}")
            return []
    
    def get_category_id(self, category_name):
        """Get category ID by name"""
        for cat_id, cat_name in self.categories:
            if cat_name == category_name:
                return cat_id
        return None
    
    def validate_sku(self, sku):
        """Validate SKU format"""
        if not self.sku_pattern.match(sku):
            return False
        return True
    
    def is_sku_unique(self, sku, exclude_id=None):
        """Check if SKU is unique"""
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
            messagebox.showerror("Error", f"Error checking SKU uniqueness: {e}")
            return False
    
    def create_product(self, sku, name, description, price, quantity, min_quantity, category):
        """Create a new product"""
        try:
            category_id = self.get_category_id(category)
            if not category_id:
                raise ValueError("Invalid category")
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (reference, name, description, price, quantity, min_quantity, category_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sku, name, description, price, quantity, min_quantity, category_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error creating product: {e}")
            return False
    
    def update_product(self, product_id, sku, name, description, price, quantity, min_quantity, category):
        """Update an existing product"""
        try:
            category_id = self.get_category_id(category)
            if not category_id:
                raise ValueError("Invalid category")
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products
                SET reference = ?, name = ?, description = ?, price = ?, quantity = ?, min_quantity = ?, category_id = ?
                WHERE id = ?
            """, (sku, name, description, price, quantity, min_quantity, category_id, product_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error updating product: {e}")
            return False
    
    def delete_product(self, product_id):
        """Delete a product"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting product: {e}")
            return False
    
    def get_product(self, product_id):
        """Get product by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.reference, p.name, p.description, p.price, p.quantity, p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE p.id = ?
            """, (product_id,))
            product = cursor.fetchone()
            conn.close()
            return product
        except Exception as e:
            messagebox.showerror("Error", f"Error loading product: {e}")
            return None
    
    def get_all_products(self):
        """Get all products"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.reference, p.name, p.description, p.price, p.quantity, p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                ORDER BY p.id
            """)
            products = cursor.fetchall()
            conn.close()
            return products
        except Exception as e:
            messagebox.showerror("Error", f"Error loading products: {e}")
            return []
    
  