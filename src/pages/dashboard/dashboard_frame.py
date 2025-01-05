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
        self.scrollable_frame.grid_rowconfigure(1, weight=1)
        
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
    
    def refresh(self):
        """Refresh dashboard data"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Rebuild dashboard
        self.setup_dashboard()
