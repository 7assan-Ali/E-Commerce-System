import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from product import Product


class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce System")
        self.geometry("1180x720")
        self.configure(bg="#f5f7fb")

        # Products shown in the GUI.
        self.products = [
            Product(1, "Dell Laptop", "Dell Inspiron Laptop", 45000.00, 10, "DELL001"),
            Product(2, "iPhone 15", "Apple iPhone 15", 38000.00, 8, "IPH015"),
            Product(3, "Samsung Galaxy S24", "Samsung Galaxy S24", 32000.00, 12, "SAM024"),
            Product(4, "AirPods Pro", "Apple AirPods Pro", 9500.00, 20, "AIRP001"),
            Product(5, "Logitech Mouse", "Wireless Logitech Mouse", 1500.00, 25, "LOG001"),
            Product(6, "Mechanical Keyboard", "RGB Mechanical Keyboard", 3000.00, 15, "KEY001"),
            Product(7, "HP Monitor 24 inch", "Full HD HP Monitor", 7500.00, 10, "HP024"),
            Product(8, "USB-C Hub", "Multi-port USB-C Hub", 1200.00, 30, "USB001"),
        ]

        self.setup_style()
        self.show_products()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 26, "bold"))
        style.configure("Subtitle.TLabel", background="#f5f7fb", foreground="#667085", font=("Segoe UI", 11))
        style.configure("Treeview", rowheight=38, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))

    def show_products(self):
        for widget in self.winfo_children():
            widget.destroy()

        header = ttk.Frame(self, padding=(30, 25))
        header.pack(fill="x")
        ttk.Label(header, text="Products", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Available products and prices", style="Subtitle.TLabel").pack(anchor="w")

        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            frame,
            columns=("id", "name", "description", "price", "stock", "sku"),
            show="headings"
        )

        columns = [
            ("id", "ID", 70),
            ("name", "Product", 210),
            ("description", "Description", 300),
            ("price", "Price (EGP)", 130),
            ("stock", "Stock", 90),
            ("sku", "SKU", 110),
        ]

        for column, heading, width in columns:
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="center")

        tree.pack(fill="both", expand=True)

        for product in self.products:
            tree.insert(
                "",
                "end",
                values=(
                    product.productId,
                    product.name,
                    product.description,
                    f"{product.price:,.2f}",
                    product.stock,
                    product.sku
                )
            )

        bottom = ttk.Frame(frame, padding=(0, 15))
        bottom.pack(fill="x")
        ttk.Label(
            bottom,
            text=f"Total Products: {len(self.products)}",
            style="Subtitle.TLabel"
        ).pack(side="left")
        ttk.Button(
            bottom,
            text="Refresh",
            command=self.show_products,
            style="Accent.TButton"
        ).pack(side="right")


if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
