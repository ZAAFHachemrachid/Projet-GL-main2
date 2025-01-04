import customtkinter as ctk
from tkinter import ttk, Menu
from datetime import datetime

class StockTable(ctk.CTkFrame):
    def __init__(self, parent, stock_manager):
        super().__init__(parent)
        self.stock_manager = stock_manager
        
        # Define columns with their properties
        self.columns = {
            'ID': {'width': 50, 'anchor': 'center'},
            'Reference': {'width': 100, 'anchor': 'w'},
            'Product': {'width': 200, 'anchor': 'w'},
            'Quantity Change': {'width': 100, 'anchor': 'center'},
            'Type': {'width': 80, 'anchor': 'center'},
            'Date': {'width': 150, 'anchor': 'w'},
            'Note': {'width': 200, 'anchor': 'w'},
            'Current Stock': {'width': 100, 'anchor': 'center'}
        }
        
        self.setup_table()
        self.setup_context_menu()
    
    def setup_table(self):
        """Setup the table and scrollbars"""
        columns = list(self.columns.keys())
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # Configure the treeview style
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Define headings and columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_table_by_column(c))
            self.tree.column(col, width=self.columns[col]['width'], anchor=self.columns[col]['anchor'])
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack the table and scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Bind events
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def setup_context_menu(self):
        """Setup the right-click context menu"""
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.view_details)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Export Movement", command=self.export_movement)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def view_details(self):
        """View details of selected movement"""
        selection = self.tree.selection()
        if not selection:
            return
        # TODO: Implement view details dialog
        pass
    
    def export_movement(self):
        """Export selected movement"""
        selection = self.tree.selection()
        if not selection:
            return
        # TODO: Implement export functionality
        pass
    
    def sort_table_by_column(self, column):
        """Sort table by clicking on column header"""
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children()]
        
        # Sort items
        items.sort(reverse=getattr(self, '_sort_reverse', False))
        
        # Update sort direction for next click
        self._sort_reverse = not getattr(self, '_sort_reverse', False)
        
        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def refresh(self, filters=None):
        """Refresh table data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get and display stock movements
        movements = self.stock_manager.get_stock_movements(filters)
        for movement in movements:
            values = (
                movement[0],  # ID
                movement[1],  # Reference
                movement[2],  # Product Name
                movement[3],  # Quantity Change
                movement[4],  # Movement Type
                movement[5],  # Date
                movement[6],  # Note
                movement[7]   # Current Stock
            )
            
            # Set row color based on movement type
            tag = 'in' if movement[4] == 'IN' else 'out'
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure row colors
        self.tree.tag_configure('in', foreground='green')
        self.tree.tag_configure('out', foreground='red')
