from database.db_config import get_db_connection

class StockManager:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
    
    def add_stock(self, product_id, quantity_added, date, note=""):
        """Add stock for a product"""
        try:
            # First update the product's quantity
            self.cursor.execute("""
                UPDATE products 
                SET quantity = quantity + ? 
                WHERE id = ?
            """, (quantity_added, product_id))
            
            # Then record the stock movement
            self.cursor.execute("""
                INSERT INTO stock_movements (product_id, quantity_change, movement_type, date, note)
                VALUES (?, ?, 'IN', ?, ?)
            """, (product_id, quantity_added, date, note))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding stock: {e}")
            self.conn.rollback()
            return False
    
    def remove_stock(self, product_id, quantity_removed, date, note=""):
        """Remove stock for a product"""
        try:
            # Check if we have enough stock
            self.cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
            current_quantity = self.cursor.fetchone()[0]
            
            if current_quantity < quantity_removed:
                return False, "Insufficient stock"
            
            # Update product quantity
            self.cursor.execute("""
                UPDATE products 
                SET quantity = quantity - ? 
                WHERE id = ?
            """, (quantity_removed, product_id))
            
            # Record the stock movement
            self.cursor.execute("""
                INSERT INTO stock_movements (product_id, quantity_change, movement_type, date, note)
                VALUES (?, ?, 'OUT', ?, ?)
            """, (product_id, quantity_removed, date, note))
            
            self.conn.commit()
            return True, "Stock removed successfully"
        except Exception as e:
            print(f"Error removing stock: {e}")
            self.conn.rollback()
            return False, str(e)
    
    def get_stock_movements(self, filters=None):
        """Get stock movements with optional filters"""
        try:
            query = """
                SELECT 
                    sm.id,
                    p.reference,
                    p.name,
                    sm.quantity_change,
                    sm.movement_type,
                    sm.date,
                    sm.note,
                    p.quantity as current_stock
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
            """
            
            if filters:
                conditions = []
                params = []
                
                if filters.get('product_id'):
                    conditions.append("p.id = ?")
                    params.append(filters['product_id'])
                
                if filters.get('movement_type'):
                    conditions.append("sm.movement_type = ?")
                    params.append(filters['movement_type'])
                
                if filters.get('date_from'):
                    conditions.append("sm.date >= ?")
                    params.append(filters['date_from'])
                
                if filters.get('date_to'):
                    conditions.append("sm.date <= ?")
                    params.append(filters['date_to'])
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY sm.date DESC"
            
            self.cursor.execute(query, params if filters else ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting stock movements: {e}")
            return []
    
    def get_low_stock_products(self, threshold=None):
        """Get products with stock below their minimum quantity"""
        try:
            query = """
                SELECT 
                    id, reference, name, quantity, min_quantity,
                    CASE 
                        WHEN quantity <= 0 THEN 'Out of Stock'
                        WHEN quantity <= min_quantity THEN 'Low Stock'
                        ELSE 'OK'
                    END as status
                FROM products
                WHERE quantity <= COALESCE(?, min_quantity)
                ORDER BY 
                    CASE 
                        WHEN quantity <= 0 THEN 1
                        WHEN quantity <= min_quantity THEN 2
                        ELSE 3
                    END
            """
            
            self.cursor.execute(query, (threshold,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
