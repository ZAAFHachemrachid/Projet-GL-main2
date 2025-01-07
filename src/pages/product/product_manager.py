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
    
    def search_products(self, search_term=None, category=None, stock_status=None, sort_by=None):
        """
        Search products based on various criteria
        
        Args:
            search_term (str): Search term to match against product name or SKU
            category (str): Category name to filter products
            stock_status (str): Filter by stock status ('In Stock', 'Low Stock', 'All')
            sort_by (str): Sort option (e.g., "Price (Low-High)")
            
        Returns:
            list: List of matching products
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT p.id, p.reference, p.name, p.description, p.price, p.quantity, p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE 1=1
            """
            params = []
            
            if search_term:
                query += """ AND (
                    LOWER(p.name) LIKE LOWER(?)
                    OR LOWER(p.reference) LIKE LOWER(?)
                )"""
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
            
            if category and category != "All":
                query += " AND c.name = ?"
                params.append(category)
            
            if stock_status:
                if stock_status == "Low Stock":
                    query += " AND p.quantity > 0 AND p.quantity <= p.min_quantity"
                elif stock_status == "In Stock":
                    query += " AND p.quantity > p.min_quantity"
            
            # Handle sorting
            if sort_by:
                if sort_by == "Name (A-Z)":
                    query += " ORDER BY p.name ASC"
                elif sort_by == "Name (Z-A)":
                    query += " ORDER BY p.name DESC"
                elif sort_by == "Price (Low-High)":
                    query += " ORDER BY p.price ASC"
                elif sort_by == "Price (High-Low)":
                    query += " ORDER BY p.price DESC"
                elif sort_by == "Stock (Low-High)":
                    query += " ORDER BY p.quantity ASC"
                elif sort_by == "Stock (High-Low)":
                    query += " ORDER BY p.quantity DESC"
            else:
                query += " ORDER BY p.name ASC"
            
            cursor.execute(query, params)
            products = cursor.fetchall()
            conn.close()
            return products
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching products: {e}")
            return []