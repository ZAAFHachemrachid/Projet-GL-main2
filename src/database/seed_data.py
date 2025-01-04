import sqlite3
from src.database.db_config import get_db_connection

def seed_categories(admin_id):
    """Seed initial categories"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # List of categories
            categories = [
                ("Tools", "Hand and power tools"),
                ("Hardware", "Nuts, bolts, screws, and fasteners"),
                ("Plumbing", "Pipes, fittings, and plumbing supplies"),
                ("Electrical", "Wiring, outlets, and electrical components"),
                ("Paint", "Interior and exterior paints and supplies"),
                ("Lumber", "Wood and building materials"),
                ("Garden", "Garden tools and supplies")
            ]

            # Insert categories
            for name, description in categories:
                cursor.execute("""
                    INSERT OR IGNORE INTO category (name, created_by)
                    VALUES (?, ?)
                """, (name, admin_id))
            
            conn.commit()
            print("Categories seeded successfully")
            
        except sqlite3.Error as err:
            print(f"Error seeding categories: {err}")
        finally:
            conn.close()

def seed_products(admin_id):
    """Seed initial products"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Get category IDs
            cursor.execute("SELECT id, name FROM category")
            categories = {name: id for id, name in cursor.fetchall()}
            
            # List of products with category names
            products = [
                # Tools Category
                ("HT001", "Hammer - 22oz", "Ball-peen hammer", 22.99, 30, 15, "Tools"),
                ("SD002", "Screwdriver - Phillips #2", "Insulated screwdriver", 4.99, 50, 20, "Tools"),
                ("AW003", "Adjustable Wrench - 6\"", "Mini adjustable wrench", 6.99, 60, 30, "Tools"),
                ("CP004", "Cable Puller", "Cable pulling tool", 9.99, 25, 15, "Tools"),
                ("DL005", "Power Drill - 18V", "Cordless power drill", 89.99, 20, 10, "Tools"),
                ("SW006", "Circular Saw", "7-1/4\" circular saw", 129.99, 15, 8, "Tools"),
                ("MT007", "Measuring Tape - 25ft", "Professional measuring tape", 9.99, 60, 30, "Tools"),
                ("CS008", "Chisel Set - 4pc", "Wood chisel set", 34.99, 25, 15, "Tools"),
                ("SB009", "Toolbox - Large", "Heavy-duty toolbox", 45.99, 20, 10, "Tools"),
                
                # Hardware Category
                ("HW001", "Assorted Screws", "Box of 100 screws", 9.99, 200, 100, "Hardware"),
                ("HW002", "Wall Anchors", "Plastic anchors, pack of 50", 5.99, 150, 75, "Hardware"),
                ("HW003", "Door Hinges", "3-inch brass hinges", 7.99, 100, 50, "Hardware"),
                ("HW004", "Cabinet Handles", "Modern cabinet pulls", 4.99, 120, 60, "Hardware"),
                ("HW005", "Nails Assortment", "Various size nails", 12.99, 150, 75, "Hardware"),
                ("HW006", "Corner Brackets", "Metal L brackets", 3.99, 200, 100, "Hardware"),
                ("HW007", "Door Lock Set", "Complete door lock kit", 29.99, 30, 15, "Hardware"),
                ("HW008", "Chain - 3ft", "Heavy duty chain", 8.99, 80, 40, "Hardware"),
                
                # Plumbing Category
                ("PB001", "PVC Pipe 2\"", "2-inch PVC pipe, 10 feet", 12.99, 40, 25, "Plumbing"),
                ("PB002", "Pipe Wrench", "14-inch pipe wrench", 29.99, 20, 10, "Plumbing"),
                ("PB003", "Sink Faucet", "Kitchen sink faucet", 79.99, 15, 8, "Plumbing"),
                ("PB004", "Drain Snake", "25ft drain auger", 24.99, 20, 10, "Plumbing"),
                ("PB005", "Pipe Fittings Kit", "Assorted fittings", 19.99, 50, 25, "Plumbing"),
                ("PB006", "Toilet Repair Kit", "Complete repair kit", 22.99, 30, 15, "Plumbing"),
                ("PB007", "Water Filter", "Under-sink filter", 49.99, 20, 10, "Plumbing"),
                ("PB008", "Shower Head", "Adjustable shower head", 34.99, 25, 12, "Plumbing"),
                
                # Electrical Category
                ("EL001", "Wire Bundle", "14-gauge copper wire, 50 feet", 29.99, 25, 15, "Electrical"),
                ("EL002", "Outlet Box", "Single gang electrical box", 2.99, 100, 50, "Electrical"),
                ("EL003", "Light Switch", "Single pole switch", 4.99, 80, 40, "Electrical"),
                ("EL004", "LED Bulbs 4pk", "60W equivalent LED", 12.99, 60, 30, "Electrical"),
                ("EL005", "Circuit Breaker", "20 amp breaker", 8.99, 40, 20, "Electrical"),
                ("EL006", "Extension Cord", "25ft heavy duty", 19.99, 35, 18, "Electrical"),
                ("EL007", "Wire Stripper", "Automatic wire stripper", 14.99, 30, 15, "Electrical"),
                ("EL008", "Junction Box", "4-inch square box", 3.99, 90, 45, "Electrical"),
                
                # Paint Category
                ("PT001", "White Paint", "Interior latex paint, 1 gallon", 34.99, 20, 10, "Paint"),
                ("PT002", "Paint Roller Set", "9-inch roller with tray", 14.99, 30, 20, "Paint"),
                ("PT003", "Paint Brushes", "5pc brush set", 16.99, 40, 20, "Paint"),
                ("PT004", "Primer - White", "All-purpose primer", 29.99, 25, 12, "Paint"),
                ("PT005", "Paint Sprayer", "Electric paint sprayer", 89.99, 15, 8, "Paint"),
                ("PT006", "Drop Cloth", "9x12 canvas drop cloth", 9.99, 50, 25, "Paint"),
                ("PT007", "Painters Tape", "2-inch blue tape", 5.99, 100, 50, "Paint"),
                ("PT008", "Paint Thinner", "1 gallon thinner", 12.99, 30, 15, "Paint"),
                
                # Lumber Category
                ("LM001", "2x4 Stud", "8ft pressure treated", 5.99, 200, 100, "Lumber"),
                ("LM002", "Plywood Sheet", "4x8 3/4\" plywood", 39.99, 30, 15, "Lumber"),
                ("LM003", "Deck Boards", "5/4 deck board", 8.99, 150, 75, "Lumber"),
                ("LM004", "Fence Pickets", "6ft cedar picket", 6.99, 200, 100, "Lumber"),
                ("LM005", "MDF Board", "4x8 medium density", 29.99, 25, 12, "Lumber"),
                ("LM006", "Trim Molding", "8ft crown molding", 12.99, 80, 40, "Lumber"),
                ("LM007", "OSB Board", "4x8 OSB sheet", 22.99, 40, 20, "Lumber"),
                ("LM008", "Cedar Planks", "1x6 cedar board", 15.99, 100, 50, "Lumber"),
                
                # Garden Category
                ("GD001", "Garden Shovel", "Steel garden shovel", 27.99, 15, 10, "Garden"),
                ("GD002", "Pruning Shears", "Bypass pruning shears", 19.99, 25, 15, "Garden"),
                ("GD003", "Garden Hose", "50ft flexible hose", 34.99, 30, 15, "Garden"),
                ("GD004", "Leaf Rake", "24-inch leaf rake", 16.99, 35, 18, "Garden"),
                ("GD005", "Garden Gloves", "Leather work gloves", 9.99, 60, 30, "Garden"),
                ("GD006", "Wheelbarrow", "6 cubic ft capacity", 89.99, 10, 5, "Garden"),
                ("GD007", "Plant Food", "All-purpose fertilizer", 14.99, 40, 20, "Garden"),
                ("GD008", "Garden Trowel", "Hand trowel", 8.99, 45, 22, "Garden"),
                ("GD009", "Sprinkler", "Oscillating sprinkler", 24.99, 25, 12, "Garden"),
                ("GD010", "Weed Killer", "1 gallon concentrate", 19.99, 30, 15, "Garden")
            ]

            # Insert products with category IDs
            for ref, name, desc, price, qty, min_qty, cat_name in products:
                cursor.execute("""
                    INSERT OR IGNORE INTO products 
                    (reference, name, description, price, quantity, min_quantity, category_id, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (ref, name, desc, price, qty, min_qty, categories[cat_name], admin_id))
            
            conn.commit()
            print("Products seeded successfully")
            
        except sqlite3.Error as err:
            print(f"Error seeding products: {err}")
        finally:
            conn.close()

def seed_sample_users():
    """Seed sample users for testing"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Create regular users with loyalty points and purchases
            users = [
                ("John Smith", "123-456-7890", "john@email.com", 10, 150.50),  # 10 loyalty points
                ("Sarah Johnson", "234-567-8901", "sarah@email.com", 30, 450.75),  # 30 loyalty points
                ("Mike Wilson", "345-678-9012", "mike@email.com", 15, 200.25),  # 15 loyalty points
                ("Emma Davis", "456-789-0123", "emma@email.com", 25, 350.00)   # 25 loyalty points
            ]
            
            # Insert users
            for name, phone, email, loyalty_points, total_spent in users:
                cursor.execute("""
                    INSERT INTO users (name, phone, email, loyalty_points, total_spent)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, phone, email, loyalty_points, total_spent))
            
            # Get products for purchases
            cursor.execute("SELECT id, price FROM products")
            products = cursor.fetchall()
            
            if products:
                # Create purchases for users
                cursor.execute("SELECT id FROM users")
                user_ids = cursor.fetchall()
                
                import random
                from datetime import datetime, timedelta
                
                # Create purchases over the last 30 days
                for user_id in user_ids:
                    # Number of purchases (10-30 purchases per user)
                    num_purchases = random.randint(10, 30)
                    
                    for _ in range(num_purchases):
                        # Create the purchase first
                        total_amount = 0
                        points_earned = random.randint(1, 5)  # Random points earned
                        
                        cursor.execute("""
                            INSERT INTO purchases (user_id, total_amount, points_earned)
                            VALUES (?, ?, ?)
                        """, (user_id[0], total_amount, points_earned))
                        
                        purchase_id = cursor.lastrowid
                        
                        # Add 1-3 items to each purchase
                        num_items = random.randint(1, 3)
                        purchase_total = 0
                        
                        for _ in range(num_items):
                            # Random product and quantity
                            product = random.choice(products)
                            quantity = random.randint(1, 5)
                            price_per_unit = product[1]
                            item_total = price_per_unit * quantity
                            purchase_total += item_total
                            
                            cursor.execute("""
                                INSERT INTO purchase_items (purchase_id, product_id, quantity, price_per_unit)
                                VALUES (?, ?, ?, ?)
                            """, (purchase_id, product[0], quantity, price_per_unit))
                        
                        # Update the purchase total
                        cursor.execute("""
                            UPDATE purchases 
                            SET total_amount = ?
                            WHERE id = ?
                        """, (purchase_total, purchase_id))
                        
                        # Update user's total_spent
                        cursor.execute("""
                            UPDATE users 
                            SET total_spent = total_spent + ?
                            WHERE id = ?
                        """, (purchase_total, user_id[0]))
            
            conn.commit()
            print("Sample users and their purchases seeded successfully")
            
        except sqlite3.Error as err:
            print(f"Error seeding sample users: {err}")
        finally:
            conn.close()

def seed_all():
    """Seed all initial data"""
    conn = get_db_connection()
    if conn:
        try:
            # First seed the categories and products
            admin_id = create_admin('admin', 'admin123', 'admin')
            seed_categories(admin_id)
            seed_products(admin_id)
            
            # Then seed the users and their purchases
            seed_sample_users()
            
            print("All data seeded successfully")
            
        except Exception as e:
            print(f"Error seeding data: {e}")
        finally:
            conn.close()

def create_admin(username, password, role='admin'):
    """Create an admin user with the specified credentials"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Insert or update admin
            cursor.execute("""
                INSERT OR REPLACE INTO admin (username, password, role)
                VALUES (?, ?, ?)
            """, (username, password, role))
            
            conn.commit()
            admin_id = cursor.lastrowid
            print(f"Admin user '{username}' created/updated successfully")
            return admin_id
            
        except sqlite3.Error as err:
            print(f"Error creating admin user: {err}")
            return None
        finally:
            conn.close()

if __name__ == "__main__":
    seed_all()
