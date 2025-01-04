import customtkinter as ctk
from tkinter import ttk, Menu, messagebox

class ProductTable(ctk.CTkFrame):
    def __init__(self, parent, product_manager):
        super().__init__(parent)
        self.product_manager = product_manager
        
        # Define columns with their properties
        self.columns = {
            'ID': {'width': 50, 'anchor': 'center'},
            'Reference': {'width': 100, 'anchor': 'w'},
            'Name': {'width': 200, 'anchor': 'w'},
            'Description': {'width': 300, 'anchor': 'w'},
            'Price': {'width': 80, 'anchor': 'e'},
            'Quantity': {'width': 80, 'anchor': 'center'},
            'Min Quantity': {'width': 80, 'anchor': 'center'},
            'Category': {'width': 100, 'anchor': 'w'}
        }
        
        self.setup_table()
        self.setup_context_menu()
    
    def setup_table(self):
        """Setup the table and scrollbars"""
        columns = ('ID', 'Reference', 'Name', 'Description', 'Price', 'Quantity', 'Min Quantity', 'Category')
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
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def setup_context_menu(self):
        """Setup the right-click context menu"""
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy SKU", command=self.copy_sku)
    
    def on_double_click(self, event):
        """Handle double-click on table row"""
        item = self.tree.selection()[0]
        self.edit_selected(item)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_selected(self, item=None):
        """Load selected item into update form"""
        if not item:
            selection = self.tree.selection()
            if not selection:
                return
            item = selection[0]
        
        values = self.tree.item(item)['values']
        if values:
            # Switch to update form and load values
            self.master.show_form("update")
            self.master.update_form.load_product(values[0])
    
    def delete_selected(self):
        """Delete selected item"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        if values and messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product {values[1]}?"):
            if self.product_manager.delete_product(values[0]):
                self.refresh()
    
    def copy_sku(self):
        """Copy selected item's SKU to clipboard"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        if values:
            self.clipboard_clear()
            self.clipboard_append(values[1])
            messagebox.showinfo("Success", "SKU copied to clipboard")
    
    def sort_table_by_column(self, column):
        """Sort table by clicking on column header"""
        # Get current sort order
        if hasattr(self, '_sort_column') and self._sort_column == column:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = column
            self._sort_reverse = False
        
        # Get all items
        items = [(self.tree.item(item)["values"], item) for item in self.tree.get_children()]
        
        # Get column index
        col_index = list(self.columns.keys()).index(column)
        
        # Sort items
        items.sort(
            key=lambda x: (
                float(x[0][col_index]) if column in ['Price', 'Quantity', 'Min Quantity'] 
                else str(x[0][col_index]).lower()
            ),
            reverse=self._sort_reverse
        )
        
        # Rearrange items in sorted order
        for index, (values, item) in enumerate(items):
            self.tree.move(item, "", index)
        
        # Update headings to show sort order
        for col in self.columns:
            if col == column:
                self.tree.heading(col, text=f"{col} {'↓' if self._sort_reverse else '↑'}")
            else:
                self.tree.heading(col, text=col)
    
    def refresh(self):
        """Refresh table data"""
        # Clear the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get search parameters if they exist
        search_params = getattr(self.product_manager, 'current_search', None)
        
        # Fetch products based on search parameters
        if search_params:
            products = self.product_manager.search_products(
                search_term=search_params['search_term'],
                category=search_params['category'],
                stock_status=search_params['stock_status'],
                sort_by=search_params['sort_by']
            )
        else:
            products = self.product_manager.get_all_products()
        
        # Insert products with proper formatting
        for product in products:
            formatted_values = list(product)
            # Format price to 2 decimal places
            formatted_values[4] = f"${formatted_values[4]:.2f}"
            # Add warning icon for low stock
            if formatted_values[5] <= formatted_values[6]:
                formatted_values[5] = f"⚠️ {formatted_values[5]}"
            
            self.tree.insert(
                '',
                'end',
                values=formatted_values,
                tags=('low_stock',) if product[5] <= product[6] else ()
            )
        
        # Configure tag for low stock items
        self.tree.tag_configure('low_stock', foreground='red')
