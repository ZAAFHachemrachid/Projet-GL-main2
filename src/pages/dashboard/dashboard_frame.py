import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.database.db_config import get_db_connection

class DashboardMetricCard(ctk.CTkFrame):
    def __init__(self, parent, title, value, icon="📊"):
        super().__init__(parent)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Icon and Title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky="ew")
        
        ctk.CTkLabel(header_frame, text=icon, font=("Arial", 20)).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text=title, font=("Arial", 14, "bold")).pack(side="left", padx=5)
        
        # Value
        ctk.CTkLabel(self, text=value, font=("Arial", 24, "bold")).grid(row=1, column=0, padx=10, pady=(0,10))

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create main container that fills the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Setup the dashboard layout"""
        # Configure grid
        self.scrollable_frame.grid_columnconfigure((0,1,2), weight=1)
        self.scrollable_frame.grid_rowconfigure((1,2), weight=1)
        
        # Title
        ctk.CTkLabel(
            self.scrollable_frame, 
            text="Dashboard", 
            font=("Arial", 24, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=20)
        
        # Create metrics section
        self.create_metrics_section()
        
        # Create charts section
        self.create_charts_section()
        
        # Create low stock section
        self.create_low_stock_section()
        
        # Add Purchase History Section
        purchase_history_frame = ctk.CTkFrame(self.scrollable_frame)
        purchase_history_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Purchase History Title
        ctk.CTkLabel(
            purchase_history_frame,
            text="Recent Purchases",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Create Treeview for purchase history
        columns = ('Date', 'Buyer', 'Product', 'Quantity', 'Price/Unit', 'Total', 'Points')
        self.purchase_tree = ttk.Treeview(purchase_history_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        column_widths = {
            'Date': 120,
            'Buyer': 120,
            'Product': 150,
            'Quantity': 80,
            'Price/Unit': 100,
            'Total': 100,
            'Points': 80
        }
        
        for col in columns:
            self.purchase_tree.heading(col, text=col)
            self.purchase_tree.column(col, width=column_widths[col])
        
        # Add scrollbars in a frame for better organization
        tree_frame = ctk.CTkFrame(purchase_history_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add vertical scrollbar
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.purchase_tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        
        # Add horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.purchase_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Configure the treeview to use both scrollbars
        self.purchase_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack the treeview after configuring scrollbars
        self.purchase_tree.pack(in_=tree_frame, side="left", fill="both", expand=True)
        
        # Load initial purchase history
        self.load_purchase_history()
    
    def create_metrics_section(self):
        """Create the metrics cards section"""
        metrics = self.get_metrics()
        
        # Total Products
        DashboardMetricCard(
            self.scrollable_frame,
            "Total Products",
            str(metrics['total_products']),
            "📦"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Total Value
        DashboardMetricCard(
            self.scrollable_frame,
            "Total Inventory Value",
            f"${metrics['total_value']:,.2f}",
            "💰"
        ).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Low Stock Items
        DashboardMetricCard(
            self.scrollable_frame,
            "Low Stock Items",
            str(metrics['low_stock_count']),
            "⚠️"
        ).grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
    
    def create_charts_section(self):
        """Create the charts section"""
        charts_frame = ctk.CTkFrame(self.scrollable_frame)
        charts_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        charts_frame.grid_columnconfigure((0,1), weight=1)
        
        # Create category distribution chart
        self.create_category_chart(charts_frame)
        
        # Create stock status chart
        self.create_stock_status_chart(charts_frame)
    
    def create_category_chart(self, parent):
        """Create pie chart showing product distribution by category"""
        # Get category data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.name, COUNT(p.id) as count
            FROM category c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY count DESC
        """)
        data = cursor.fetchall()
        conn.close()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Products by Category')
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
    
    def create_stock_status_chart(self, parent):
        """Create bar chart showing stock status"""
        # Get stock status data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN quantity <= min_quantity THEN 'Low Stock'
                    WHEN quantity <= (min_quantity * 2) THEN 'Medium Stock'
                    ELSE 'Good Stock'
                END as status,
                COUNT(*) as count
            FROM products
            GROUP BY status
        """)
        data = cursor.fetchall()
        conn.close()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        
        ax.bar(labels, values)
        ax.set_title('Stock Status Distribution')
        ax.set_ylabel('Number of Products')
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
    
    def create_low_stock_section(self):
        """Create the low stock items section"""
        # Create frame
        low_stock_frame = ctk.CTkFrame(self.scrollable_frame)
        low_stock_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Add title
        ctk.CTkLabel(
            low_stock_frame,
            text="Low Stock Items",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Create table
        columns = ('SKU', 'Name', 'Current Stock', 'Min Stock', 'Category')
        tree = ttk.Treeview(low_stock_frame, columns=columns, show='headings', height=5)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Get low stock items
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.reference, p.name, p.quantity, p.min_quantity, c.name
            FROM products p
            LEFT JOIN category c ON p.category_id = c.id
            WHERE p.quantity <= p.min_quantity
            ORDER BY p.quantity ASC
        """)
        items = cursor.fetchall()
        conn.close()
        
        # Add items to table
        for item in items:
            tree.insert('', 'end', values=item)
        
        tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    def get_metrics(self):
        """Get dashboard metrics"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        # Get total value
        cursor.execute("SELECT SUM(price * quantity) FROM products")
        total_value = cursor.fetchone()[0] or 0
        
        # Get low stock count
        cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= min_quantity")
        low_stock_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_products': total_products,
            'total_value': total_value,
            'low_stock_count': low_stock_count
        }
    
    def load_purchase_history(self):
        """Load and display all purchase history"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all purchases with product details and user information
            cursor.execute("""
                SELECT 
                    p.created_at,
                    u.name as buyer_name,
                    pr.name as product_name,
                    pi.quantity,
                    pi.price_per_unit,
                    (pi.quantity * pi.price_per_unit) as item_total,
                    p.points_earned
                FROM purchases p
                JOIN users u ON p.user_id = u.id
                JOIN purchase_items pi ON pi.purchase_id = p.id
                JOIN products pr ON pi.product_id = pr.id
                ORDER BY p.created_at DESC
            """)
            
            purchases = cursor.fetchall()
            
            # Clear existing items
            for item in self.purchase_tree.get_children():
                self.purchase_tree.delete(item)
            
            # Insert purchase history data
            for purchase in purchases:
                try:
                    # Try parsing the date, if it fails just use it as is
                    try:
                        date = datetime.strptime(purchase[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                    except (ValueError, TypeError):
                        date = str(purchase[0])
                    
                    self.purchase_tree.insert('', 'end', values=(
                        date,
                        purchase[1] or "Unknown",  # Buyer name
                        purchase[2] or "Unknown",  # Product name
                        purchase[3] or 0,  # Quantity
                        f"${purchase[4]:.2f}" if purchase[4] else "$0.00",  # Price per unit
                        f"${purchase[5]:.2f}" if purchase[5] else "$0.00",  # Total
                        purchase[6] or 0  # Points earned
                    ))
                except Exception as row_error:
                    print(f"Error processing purchase row: {row_error}")
                    continue
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading purchase history: {e}")
            # Print the full error traceback for debugging
            import traceback
            traceback.print_exc()
    
    def refresh(self):
        """Refresh dashboard data"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Rebuild dashboard
        self.setup_dashboard()
        
        # Load purchase history
        self.load_purchase_history()
