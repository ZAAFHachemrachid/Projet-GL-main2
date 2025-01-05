import sqlite3
import os
from tkinter import messagebox
from pathlib import Path

# Get the absolute path to the database file
DB_FILE = os.path.join(Path(__file__).parent.parent.parent, "database.db")

def get_db_connection():
    """Get a connection to the SQLite database"""
    try:
        return sqlite3.connect(DB_FILE)
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Could not connect to database: {err}")
        return None

def create_tables():
    """Create all required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create admin table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create category table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES admin (id)
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL,
            category_id INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category (id),
            FOREIGN KEY (created_by) REFERENCES admin (id)
        )
    """)
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            loyalty_points INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES admin (id)
        )
    """)

    # Create purchases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_amount REAL NOT NULL,
            points_earned INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (created_by) REFERENCES admin (id)
        )
    """)

    # Create purchase_details table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)

    # Create default admin account if it doesn't exist
    cursor.execute("""
        INSERT OR IGNORE INTO admin (username, password, email, role)
        VALUES (?, ?, ?, ?)
    """, ('admin', 'admin123', 'admin@example.com', 'admin'))

    conn.commit()
    conn.close()

def update_category_table():
    """Add description column to category table if it doesn't exist"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if description column exists
            cursor.execute("PRAGMA table_info(category)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'description' not in columns:
                cursor.execute("ALTER TABLE category ADD COLUMN description TEXT")
                conn.commit()
                print("Added description column to category table")
            
        except sqlite3.Error as err:
            print(f"Error updating category table: {err}")
        finally:
            conn.close()

def setup_database():
    """Initialize the database"""
    try:
        # Create database file if it doesn't exist
        conn = sqlite3.connect(DB_FILE)
        conn.close()
        
        # Create all tables
        create_tables()
        update_category_table()
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Error setting up database: {e}")

def get_stock_alerts():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.reference, p.name, p.quantity, p.min_quantity, c.name as category
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE p.quantity < p.min_quantity
                ORDER BY p.quantity ASC
            """)
            alerts = cursor.fetchall()
            conn.close()
            return alerts
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error fetching stock alerts: {err}")
            return []
    return []

if __name__ == "__main__":
    setup_database()
