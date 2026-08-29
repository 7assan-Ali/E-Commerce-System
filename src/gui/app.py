import os
import sys
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Keep the existing model imports unchanged. The model folder is added to the path
# so imports such as "from user import User" continue to work.
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from customer import Customer
from admin import Admin
from product import Product
from category import Category
from cart import Cart
from cart_item import CartItem
from order import Order
from order_item import OrderItem
from address import Address
from payment import Payment
from review import Review
from shipment import Shipment


class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce System")
        self.geometry("1100x700")
        self.minsize(950, 600)

        self.products = [
            Product(1, "Laptop", "Dell Laptop", 25000.50, 10, "DELL001"),
            Product(2, "Wireless Mouse", "Wireless Mouse", 500.0, 25, "MOU001"),
            Product(3, "Keyboard", "Mechanical Keyboard", 1500.0, 15, "KEY001"),
        ]
        self.categories = [Category(1, "Electronics", "Electronic devices")]
        for product in self.products:
            self.categories[0].addProduct(product)

        self.customer = Customer(1, "Hassan", "hassan@gmail.com", "1234", "01012345678", 101)
        self.customer.cart = Cart(1, str(date.today()))
        self.admin = Admin(2, "System Admin", "admin@ecommerce.com", "admin", "01000000000", 1, "Administrator")
        self.addresses = []
        self.orders = []
        self.payments = []
        self.shipments = []
        self.reviews = []

        self.current_user = None
        self.selected_product = None
        self.cart_records = []

        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("TButton", padding=8)
        style.configure("Treeview", rowheight=30)

    def show_login(self):
        self.clear_window()
        self.style()

        frame = ttk.Frame(self, padding=50)
        frame.pack(expand=True)

        ttk.Label(frame, text="E-Commerce System", style="Title.TLabel").pack(pady=(0, 10))
        ttk.Label(frame, text="Choose your account").pack(pady=(0, 30))

        ttk.Button(frame, text="Customer Login", width=25,
                   command=lambda: self.login(self.customer)).pack(pady=8)
        ttk.Button(frame, text="Admin Login", width=25,
                   command=lambda: self.login(self.admin)).pack(pady=8)
        ttk.Button(frame, text="Exit", width=25, command=self.destroy).pack(pady=8)

        ttk.Label(
            frame,
            text="Demo customer: Hassan | Demo admin: System Admin",
            foreground="gray"
        ).pack(pady=25)

    def login(self, user):
        user.login()
        self.current_user = user
        if isinstance(user, Admin):
            self.show_admin_dashboard()
        else:
            self.show_customer_dashboard()

    def logout(self):
        if self.current_user:
            self.current_user.logout()
        self.current_user = None
        self.show_login()

    def header(self, title):
        top = ttk.Frame(self, padding=(20, 15))
        top.pack(fill="x")
        ttk.Label(top, text=title, style="Heading.TLabel").pack(side="left")
        ttk.Button(top, text="Logout", command=self.logout).pack(side="right")

    def show_customer_dashboard(self):
        self.clear_window()
        self.header(f"Customer Dashboard - {self.customer.name}")

        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)

        buttons = [
            ("Browse Products", self.show_products),
            ("My Cart", self.show_cart),
            ("My Orders", self.show_orders),
            ("Profile", self.show_profile),
            ("Address", self.show_address),
            ("Reviews", self.show_reviews),
        ]
        for index, (text, command) in enumerate(buttons):
            row, col = divmod(index, 2)
            ttk.Button(body, text=text, command=command, width=30).grid(
                row=row, column=col, padx=15, pady=15, sticky="nsew"
            )
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        for row in range(3):
            body.rowconfigure(row, weight=1)

    def show_products(self):
        self.clear_window()
        self.header("Products")

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("id", "name", "price", "stock", "sku"), show="headings")
        for col, text in zip(("id", "name", "price", "stock", "sku"),
                             ("ID", "Product", "Price", "Stock", "SKU")):
            tree.heading(col, text=text)
        tree.column("id", width=70)
        tree.column("name", width=250)
        tree.column("price", width=140)
        tree.column("stock", width=100)
        tree.column("sku", width=150)

        for product in self.products:
            tree.insert("", "end", iid=str(product.productId),
                        values=(product.productId, product.name, f"{product.price:.2f}", product.stock, product.sku))
        tree.pack(fill="both", expand=True)

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)

        def add_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Select Product", "Please select a product first.")
                return
            product = next(p for p in self.products if str(p.productId) == selection[0])
            if not product.isAvailable():
                messagebox.showwarning("Unavailable", "This product is out of stock.")
                return
            quantity = simpledialog.askinteger("Quantity", "Enter quantity:", initialvalue=1, minvalue=1)
            if quantity is None:
                return
            if quantity > product.stock:
                messagebox.showwarning("Stock", "Not enough stock available.")
                return
            item = CartItem(quantity, product.price)
            item.product = product
            self.customer.cart.addItem(item)
            self.cart_records.append(item)
            self.refresh_cart_total()
            messagebox.showinfo("Cart", f"{product.name} added to cart.")

        ttk.Button(controls, text="Add to Cart", command=add_selected).pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def refresh_cart_total(self):
        total = 0.0
        for item in self.customer.cart.items:
            total += item.calculateSubtotal()
        self.customer.cart.totalAmount = total

    def show_cart(self):
        self.clear_window()
        self.header("My Cart")
        self.refresh_cart_total()

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("product", "quantity", "unit", "subtotal"), show="headings")
        for col, text in zip(("product", "quantity", "unit", "subtotal"),
                             ("Product", "Quantity", "Unit Price", "Subtotal")):
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)

        for index, item in enumerate(self.customer.cart.items):
            product = getattr(item, "product", None)
            name = product.name if product else "Product"
            tree.insert("", "end", iid=str(index), values=(
                name, item.quantity, f"{item.unitPrice:.2f}", f"{item.calculateSubtotal():.2f}"
            ))

        total_label = ttk.Label(frame, text=f"Total: {self.customer.cart.getTotal():.2f}", style="Heading.TLabel")
        total_label.pack(anchor="e", pady=10)

        controls = ttk.Frame(frame)
        controls.pack(fill="x")

        def remove_selected():
            selection = tree.selection()
            if not selection:
                return
            item = self.customer.cart.items[int(selection[0])]
            self.customer.cart.removeItem(item)
            self.refresh_cart_total()
            self.show_cart()

        def update_selected():
            selection = tree.selection()
            if not selection:
                return
            item = self.customer.cart.items[int(selection[0])]
            quantity = simpledialog.askinteger("Quantity", "New quantity:", initialvalue=item.quantity, minvalue=1)
            if quantity is None:
                return
            item.updateQuantity(quantity)
            self.refresh_cart_total()
            self.show_cart()

        def checkout():
            if not self.customer.cart.items:
                messagebox.showwarning("Cart", "Your cart is empty.")
                return
            self.refresh_cart_total()
            order = Order(len(self.orders) + 1, str(date.today()))
            for item in self.customer.cart.items:
                product = getattr(item, "product", None)
                order_item = OrderItem(item.quantity, item.unitPrice)
                order_item.calculateSubtotal()
                order_item.product = product
                order.items.append(order_item)
            order.total = self.customer.cart.getTotal()
            self.orders.append(order)
            self.customer.orders.append(order)
            payment = Payment(len(self.payments) + 1, order.total, str(date.today()), method="Cash")
            self.payments.append(payment)
            self.customer.cart.clearCart()
            self.cart_records.clear()
            messagebox.showinfo("Order", f"Order #{order.orderId} created successfully.")
            self.show_orders()

        ttk.Button(controls, text="Update Quantity", command=update_selected).pack(side="left", padx=5)
        ttk.Button(controls, text="Remove", command=remove_selected).pack(side="left", padx=5)
        ttk.Button(controls, text="Checkout", command=checkout).pack(side="left", padx=5)
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def show_orders(self):
        self.clear_window()
        self.header("My Orders")
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("id", "date", "status", "total"), show="headings")
        for col, text in zip(("id", "date", "status", "total"), ("Order ID", "Date", "Status", "Total")):
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for order in self.customer.orders:
            tree.insert("", "end", values=(order.orderId, order.orderDate, order.status, f"{order.total:.2f}"))

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)

        def cancel_selected():
            selection = tree.selection()
            if not selection:
                return
            order_id = int(tree.item(selection[0], "values")[0])
            order = next(o for o in self.customer.orders if o.orderId == order_id)
            order.cancelOrder()
            self.show_orders()

        ttk.Button(controls, text="Cancel Selected", command=cancel_selected).pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def show_profile(self):
        self.clear_window()
        self.header("My Profile")
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=f"Customer ID: {self.customer.customerId}", style="Heading.TLabel").pack(anchor="w", pady=8)
        fields = [("Name", self.customer.name), ("Email", self.customer.email),
                  ("Phone", self.customer.phone), ("Loyalty Points", self.customer.loyaltyPoints)]
        for label, value in fields:
            ttk.Label(frame, text=f"{label}: {value}").pack(anchor="w", pady=8)

        def update():
            name = simpledialog.askstring("Name", "New name:", initialvalue=self.customer.name)
            if name is None:
                return
            email = simpledialog.askstring("Email", "New email:", initialvalue=self.customer.email)
            if email is None:
                return
            phone = simpledialog.askstring("Phone", "New phone:", initialvalue=self.customer.phone)
            if phone is None:
                return
            self.customer.name = name
            self.customer.email = email
            self.customer.phone = phone
            self.show_profile()

        ttk.Button(frame, text="Update Profile", command=update).pack(anchor="w", pady=20)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(anchor="e")

    def show_address(self):
        self.clear_window()
        self.header("My Address")
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        if self.addresses:
            address = self.addresses[0]
            ttk.Label(frame, text=f"{address.street}, {address.city}, {address.governorate} - {address.postalCode}",
                      style="Heading.TLabel").pack(anchor="w", pady=15)
        else:
            ttk.Label(frame, text="No address saved.").pack(anchor="w", pady=15)

        def save_address():
            values = []
            for title in ("Street", "City", "Governorate", "Postal Code"):
                value = simpledialog.askstring(title, f"Enter {title.lower()}:")
                if value is None:
                    return
                values.append(value)
            if self.addresses:
                self.addresses[0].updateAddress(*values)
            else:
                self.addresses.append(Address(1, *values))
            self.show_address()

        ttk.Button(frame, text="Add / Update Address", command=save_address).pack(anchor="w")
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(anchor="e", pady=20)

    def show_reviews(self):
        self.clear_window()
        self.header("Reviews")
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "rating", "comment", "date"), show="headings")
        for col, text in zip(("id", "rating", "comment", "date"), ("ID", "Rating", "Comment", "Date")):
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for review in self.reviews:
            tree.insert("", "end", values=(review.reviewId, review.rating, review.comment, review.reviewDate))

        def add_review():
            rating = simpledialog.askinteger("Rating", "Rating (1-5):", minvalue=1, maxvalue=5)
            if rating is None:
                return
            comment = simpledialog.askstring("Comment", "Your comment:")
            if comment is None:
                return
            review = Review(len(self.reviews) + 1, rating, comment, str(date.today()))
            self.reviews.append(review)
            review.addReview()
            self.show_reviews()

        ttk.Button(frame, text="Add Review", command=add_review).pack(side="left", pady=15)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(side="right", pady=15)

    def show_admin_dashboard(self):
        self.clear_window()
        self.header(f"Admin Dashboard - {self.admin.name}")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        buttons = [
            ("Manage Products", self.admin_products),
            ("Manage Orders", self.admin_orders),
            ("Admin Profile", self.admin_profile),
        ]
        for index, (text, command) in enumerate(buttons):
            ttk.Button(body, text=text, command=command, width=30).grid(
                row=0, column=index, padx=15, pady=30, sticky="nsew"
            )
            body.columnconfigure(index, weight=1)

    def admin_products(self):
        self.clear_window()
        self.header("Admin - Manage Products")
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "name", "price", "stock", "sku"), show="headings")
        for col, text in zip(("id", "name", "price", "stock", "sku"), ("ID", "Product", "Price", "Stock", "SKU")):
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)

        def refresh():
            tree.delete(*tree.get_children())
            for product in self.products:
                tree.insert("", "end", iid=str(product.productId), values=(product.productId, product.name,
                             f"{product.price:.2f}", product.stock, product.sku))

        refresh()

        def add_product():
            name = simpledialog.askstring("Product", "Name:")
            if not name: return
            description = simpledialog.askstring("Product", "Description:") or ""
            price = simpledialog.askfloat("Product", "Price:", minvalue=0)
            if price is None: return
            stock = simpledialog.askinteger("Product", "Stock:", minvalue=0)
            if stock is None: return
            sku = simpledialog.askstring("Product", "SKU:") or f"SKU{len(self.products)+1:03d}"
            product = Product(len(self.products) + 1, name, description, price, stock, sku)
            self.products.append(product)
            self.admin.addProduct(product)
            refresh()

        def update_product():
            selection = tree.selection()
            if not selection: return
            product = next(p for p in self.products if str(p.productId) == selection[0])
            price = simpledialog.askfloat("Price", "New price:", initialvalue=product.price, minvalue=0)
            if price is not None: product.updatePrice(price)
            stock = simpledialog.askinteger("Stock", "New stock:", initialvalue=product.stock, minvalue=0)
            if stock is not None: product.updateStock(stock)
            self.admin.updateProduct(product)
            refresh()

        def delete_product():
            selection = tree.selection()
            if not selection: return
            product = next(p for p in self.products if str(p.productId) == selection[0])
            if messagebox.askyesno("Delete", f"Delete {product.name}?"):
                self.products.remove(product)
                for category in self.categories:
                    category.removeProduct(product)
                self.admin.deleteProduct(product)
                refresh()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add Product", command=add_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Update Product", command=update_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Delete Product", command=delete_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Back", command=self.show_admin_dashboard).pack(side="right")

    def admin_orders(self):
        self.clear_window()
        self.header("Admin - Manage Orders")
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "customer", "date", "status", "total"), show="headings")
        for col, text in zip(("id", "customer", "date", "status", "total"),
                             ("Order ID", "Customer", "Date", "Status", "Total")):
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for order in self.orders:
            tree.insert("", "end", iid=str(order.orderId), values=(order.orderId, self.customer.name,
                        order.orderDate, order.status, f"{order.total:.2f}"))

        def update_status():
            selection = tree.selection()
            if not selection: return
            order = next(o for o in self.orders if str(o.orderId) == selection[0])
            status = simpledialog.askstring("Status", "Pending / Processing / Shipped / Delivered / Cancelled:",
                                            initialvalue=order.status)
            if status:
                order.updateStatus(status)
                self.admin.manageOrders()
                self.admin_orders()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Update Status", command=update_status).pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_admin_dashboard).pack(side="right")

    def admin_profile(self):
        self.clear_window()
        self.header("Admin Profile")
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        self.admin.displayAdminInfo()
        for text in (
            f"Admin ID: {self.admin.adminId}",
            f"Name: {self.admin.name}",
            f"Email: {self.admin.email}",
            f"Phone: {self.admin.phone}",
            f"Role: {self.admin.role}",
        ):
            ttk.Label(frame, text=text).pack(anchor="w", pady=8)
        ttk.Button(frame, text="Back", command=self.show_admin_dashboard).pack(anchor="e", pady=20)


if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
