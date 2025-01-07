import sqlite3
import os
from pathlib import Path
import random

# Get the absolute path to the database file
DB_FILE = os.path.join(Path(__file__).parent.parent.parent, "database.db")


def get_db_connection():
    """Get a connection to the SQLite database"""
    try:
        return sqlite3.connect(DB_FILE)
    except sqlite3.Error as err:
        print(f"Could not connect to database: {err}")
        return None


def seed_admin(cursor):
    """Seed admin table with additional staff members"""
    admins = [
        ("manager", "manager123", "manager@hardware.com", "admin"),
        ("sales1", "sales123", "sales1@hardware.com", "user"),
        ("sales2", "sales123", "sales2@hardware.com", "user"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO admin (username, password, email, role)
        VALUES (?, ?, ?, ?)
    """,
        admins,
    )
    print("Admin table seeded successfully!")


def seed_categories(cursor):
    """Seed categories table with hardware store categories"""
    categories = [
        ("Hand Tools", "Manual tools for various tasks", 1),
        ("Power Tools", "Electric and battery-powered tools", 1),
        ("Fasteners", "Screws, nails, and other fastening materials", 1),
        ("Plumbing", "Pipes, fittings, and plumbing supplies", 1),
        ("Electrical", "Wiring, fixtures, and electrical supplies", 1),
        ("Hardware", "General hardware items and fittings", 1),
        ("Safety Equipment", "Personal protective equipment and safety gear", 1),
        ("Paint & Supplies", "Paints, brushes, and painting accessories", 1),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO category (name, description, created_by)
        VALUES (?, ?, ?)
    """,
        categories,
    )
    print("Categories table seeded successfully!")
    return {
        name: cursor.execute(
            "SELECT id FROM category WHERE name = ?", (name,)
        ).fetchone()[0]
        for name, _, _ in categories
    }


def seed_products(cursor, category_map):
    """Seed products table with hardware store inventory"""
    products = [
        # Hand Tools
        (
            "HT001",
            "Hammer - 16oz",
            "Standard claw hammer",
            24.99,
            50,
            10,
            category_map["Hand Tools"],
            1,
        ),
        (
            "HT002",
            "Screwdriver Set",
            "6-piece precision set",
            19.99,
            40,
            15,
            category_map["Hand Tools"],
            1,
        ),
        (
            "HT003",
            "Adjustable Wrench",
            "10-inch adjustable wrench",
            16.99,
            45,
            12,
            category_map["Hand Tools"],
            1,
        ),
        # Power Tools
        (
            "PT001",
            "Cordless Drill - 18V",
            "With battery and charger",
            149.99,
            25,
            8,
            category_map["Power Tools"],
            1,
        ),
        (
            "PT002",
            "Circular Saw",
            "7-1/4 inch blade",
            129.99,
            20,
            5,
            category_map["Power Tools"],
            1,
        ),
        (
            "PT003",
            "Impact Driver Kit",
            "20V with accessories",
            179.99,
            15,
            5,
            category_map["Power Tools"],
            1,
        ),
        # Fasteners
        (
            "FT001",
            'Wood Screws 1.5"',
            "Box of 100",
            8.99,
            150,
            50,
            category_map["Fasteners"],
            1,
        ),
        (
            "FT002",
            "Drywall Anchors",
            "Pack of 50",
            6.99,
            100,
            30,
            category_map["Fasteners"],
            1,
        ),
        (
            "FT003",
            'Deck Screws 2.5"',
            "Box of 50",
            12.99,
            4,
            20,
            category_map["Fasteners"],
            1,
        ),  # Low stock
        # Plumbing
        (
            "PL001",
            'PVC Pipe 2"',
            "10 ft length",
            15.99,
            60,
            20,
            category_map["Plumbing"],
            1,
        ),
        (
            "PL002",
            "Pipe Wrench",
            "14-inch heavy duty",
            34.99,
            25,
            8,
            category_map["Plumbing"],
            1,
        ),
        # Electrical
        (
            "EL001",
            "Wire Stripper",
            "Professional grade",
            22.99,
            30,
            10,
            category_map["Electrical"],
            1,
        ),
        (
            "EL002",
            "Electrical Tape",
            "Pack of 3",
            7.99,
            80,
            25,
            category_map["Electrical"],
            1,
        ),
        # Hardware
        (
            "HW001",
            "Door Hinges",
            "Brass finish, pair",
            9.99,
            60,
            20,
            category_map["Hardware"],
            1,
        ),
        (
            "HW002",
            "Cabinet Pulls",
            "Modern style, 5-pack",
            16.99,
            40,
            15,
            category_map["Hardware"],
            1,
        ),
        # Safety Equipment
        (
            "SF001",
            "Safety Glasses",
            "ANSI certified",
            12.99,
            75,
            25,
            category_map["Safety Equipment"],
            1,
        ),
        (
            "SF002",
            "Work Gloves",
            "Leather, large",
            19.99,
            50,
            20,
            category_map["Safety Equipment"],
            1,
        ),
        # Paint & Supplies
        (
            "PS001",
            "Paint Brush Set",
            "3-piece premium",
            24.99,
            35,
            12,
            category_map["Paint & Supplies"],
            1,
        ),
        (
            "PS002",
            "Paint Roller Kit",
            "With tray and covers",
            18.99,
            45,
            15,
            category_map["Paint & Supplies"],
            1,
        ),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO products 
        (reference, name, description, price, quantity, min_quantity, category_id, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        products,
    )
    print("Products table seeded successfully!")
    return {
        ref: (
            cursor.execute(
                "SELECT id, price FROM products WHERE reference = ?", (ref,)
            ).fetchone()
        )
        for ref, _, _, _, _, _, _, _ in products
    }


def seed_users(cursor):
    """Seed users table with customer data"""
    users = [
        ("Mike Johnson", "555-0101", "mike@email.com", 200, 1500.0, 1),
        ("Sarah Wilson", "555-0102", "sarah@email.com", 150, 1200.0, 1),
        ("Tom Anderson", "555-0103", "tom@email.com", 300, 2000.0, 1),
        ("Lisa Cooper", "555-0104", "lisa@email.com", 100, 800.0, 1),
        ("Bill Martinez", "555-0105", "bill@email.com", 250, 1800.0, 1),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO users 
        (name, phone, email, loyalty_points, total_spent, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        users,
    )
    print("Users table seeded successfully!")
    return {
        name: cursor.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()[
            0
        ]
        for name, _, _, _, _, _ in users
    }


def seed_purchases(cursor, user_map, product_map):
    """Seed purchases and purchase_details tables"""
    # Generate purchases for each user
    for user_name, user_id in user_map.items():
        # Create 3-5 purchases for each user
        for _ in range(random.randint(3, 5)):
            # Select random products for this purchase
            purchase_products = random.sample(
                list(product_map.items()), random.randint(2, 5)
            )
            purchase_total = 0
            purchase_details = []

            # Calculate purchase details
            for product_ref, (product_id, price) in purchase_products:
                quantity = random.randint(1, 3)
                total_price = price * quantity
                purchase_total += total_price
                purchase_details.append((product_id, quantity, price, total_price))

            # Create purchase record
            points_earned = int(purchase_total // 10)  # 1 point per $10 spent
            cursor.execute(
                """
                INSERT INTO purchases (user_id, total_amount, points_earned, created_by)
                VALUES (?, ?, ?, ?)
            """,
                (user_id, purchase_total, points_earned, 1),
            )

            purchase_id = cursor.lastrowid

            # Create purchase details
            cursor.executemany(
                """
                INSERT INTO purchase_details 
                (purchase_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            """,
                [
                    (purchase_id, prod_id, qty, price, total)
                    for prod_id, qty, price, total in purchase_details
                ],
            )

    print("Purchases and purchase details tables seeded successfully!")


def seed_database():
    """Main function to seed all tables"""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        # Seed each table
        seed_admin(cursor)
        category_map = seed_categories(cursor)
        product_map = seed_products(cursor, category_map)
        user_map = seed_users(cursor)
        seed_purchases(cursor, user_map, product_map)

        conn.commit()
        print("Database seeding completed successfully!")

    except sqlite3.Error as err:
        print(f"Error seeding database: {err}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    seed_database()
