import sqlite3
from db_config import get_db_connection

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

def seed_sample_users(admin_id):
    """Seed sample users"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # List of sample users
            users = [
                ("John Doe", "555-0101", "john@example.com"),
                ("Jane Smith", "555-0102", "jane@example.com"),
                ("Bob Wilson", "555-0103", "bob@example.com"),
                ("Alice Johnson", "555-0104", "alice@example.com"),
                ("Charlie Brown", "555-0105", "charlie@example.com"),
                ("Diana Prince", "555-0106", "diana@example.com"),
                ("Edward Stone", "555-0107", "edward@example.com"),
                ("Fiona Green", "555-0108", "fiona@example.com"),
                ("George Miller", "555-0109", "george@example.com"),
                ("Helen Davis", "555-0110", "helen@example.com")
            ]

            # Insert users
            for name, phone, email in users:
                cursor.execute("""
                    INSERT OR IGNORE INTO users (name, phone, email, created_by)
                    VALUES (?, ?, ?, ?)
                """, (name, phone, email, admin_id))
            
            conn.commit()
            print("Sample users seeded successfully")
            
        except sqlite3.Error as err:
            print(f"Error seeding users: {err}")
        finally:
            conn.close()

def seed_all(admin_id):
    """Seed all initial data"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Seed all data
            seed_categories(admin_id)
            seed_products(admin_id)
            seed_sample_users(admin_id)
            
            print("All data seeded successfully")
            
        except sqlite3.Error as err:
            print(f"Error in seed_all: {err}")
        finally:
            conn.close()

def create_admin(username, password):
    """Create an admin user with the specified credentials or update if exists"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT id FROM admin WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                # Update existing user's password
                cursor.execute("""
                    UPDATE admin SET password = ? WHERE username = ?
                """, (password, username))
                admin_id = result[0]
                print("Admin user password updated successfully")
            else:
                # Create new user
                cursor.execute("""
                    INSERT INTO admin (username, password)
                    VALUES (?, ?)
                """, (username, password))
                admin_id = cursor.lastrowid
                print("Admin user created successfully")
            
            conn.commit()
            return admin_id
            
        except sqlite3.Error as err:
            print(f"Error managing admin user: {err}")
            return None
        finally:
            conn.close()

if __name__ == "__main__":
    # Create admin users
    admin1_id = create_admin('admin1', 'admin123')
    admin2_id = create_admin('admin2', 'admin456')
    admin3_id = create_admin('admin3', 'admin789')
    
    if admin1_id:
        seed_all(admin1_id)
