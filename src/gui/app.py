import os
import sys
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from user import User
from customer import Customer
from admin import Admin
from product import Product
from cart import Cart
from cart_item import CartItem
from order import Order
from order_item import OrderItem
from payment import Payment
from address import Address
from review import Review
from shipment import Shipment


class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce System")
        self.geometry("1200x760")
        self.minsize(1000, 650)
        self.configure(bg="#f5f7fb")

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

        self.customers = []
        self.admins = []
        self.orders = []
        self.payments = []
        self.shipments = []
        self.reviews = []
        self.current_user = None

        # Runtime demo accounts are kept internal and are never displayed in the GUI.
        customer = Customer(1, "Hassan", "hassan@gmail.com", "1234", "01012345678", 101)
        customer.cart = Cart(1, str(date.today()))
        customer.orders = []
        customer.reviews = []
        customer.address = Address(1, "Main Street", "Beni Suef", "Beni Suef", "62511")
        self.customers.append(customer)

        admin = Admin(2, "System Admin", "admin@ecommerce.com", "admin", "01000000000", 1, "Administrator")
        self.admins.append(admin)

        self.setup_style()
        self.show_login()

    # -------------------- UI helpers --------------------
    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="white")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 28, "bold"))
        style.configure("Heading.TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#f5f7fb", foreground="#667085", font=("Segoe UI", 11))
        style.configure("CardTitle.TLabel", background="white", foreground="#172033", font=("Segoe UI", 14, "bold"))
        style.configure("CardText.TLabel", background="white", foreground="#667085", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def header(self, title, subtitle="", back=None):
        top = ttk.Frame(self, padding=(28, 20))
        top.pack(fill="x")
        if back:
            ttk.Button(top, text="← Back", command=back).pack(side="right", padx=(8, 0))
        ttk.Button(top, text="Logout", command=self.logout).pack(side="right")
        ttk.Label(top, text=title, style="Heading.TLabel").pack(anchor="w")
        ttk.Label(top, text=subtitle, style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

    def account_exists(self, email):
        return any(u.email.lower() == email.lower() for u in self.customers + self.admins)

    def calculate_cart_total(self, customer=None):
        customer = customer or self.current_user
        total = 0.0
        if customer and customer.cart:
            for item in customer.cart.items:
                total += item.calculateSubtotal()
            customer.cart.totalAmount = total
        return total

    def selected_product(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Product", "Please select a product first.")
            return None
        pid = int(tree.item(selection[0], "values")[0])
        return next((p for p in self.products if p.productId == pid), None)

    # -------------------- Authentication --------------------
    def show_login(self):
        self.clear()
        outer = ttk.Frame(self, padding=45)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="E-Commerce System", style="Title.TLabel").pack(pady=(35, 3))
        ttk.Label(outer, text="Login to continue", style="Subtitle.TLabel").pack(pady=(0, 25))

        card = ttk.Frame(outer, style="Card.TFrame", padding=35)
        card.pack(ipadx=35)
        ttk.Label(card, text="Welcome Back", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="Use your account credentials", style="CardText.TLabel").pack(anchor="w", pady=(4, 20))

        ttk.Label(card, text="Email", style="CardText.TLabel").pack(anchor="w")
        email = ttk.Entry(card, width=42)
        email.pack(fill="x", pady=(5, 12), ipady=5)

        ttk.Label(card, text="Password", style="CardText.TLabel").pack(anchor="w")
        password = ttk.Entry(card, width=42, show="*")
        password.pack(fill="x", pady=(5, 16), ipady=5)

        def login():
            e = email.get().strip().lower()
            p = password.get()
            for user in self.customers + self.admins:
                if user.email.lower() == e and user.password == p:
                    user.login()
                    self.current_user = user
                    if isinstance(user, Admin):
                        self.show_admin_dashboard()
                    else:
                        self.show_customer_dashboard()
                    return
            messagebox.showerror("Login Failed", "Invalid email or password.")

        ttk.Button(card, text="Login", command=login, style="Accent.TButton").pack(fill="x", pady=(0, 12))
        ttk.Button(card, text="Sign Up", command=self.show_signup).pack(fill="x")
        ttk.Button(outer, text="Exit", command=self.destroy).pack(pady=20)

    def show_signup(self):
        self.clear()
        outer = ttk.Frame(self, padding=30)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Create Customer Account", style="Title.TLabel").pack(pady=(10, 3))
        ttk.Label(outer, text="All fields are required", style="Subtitle.TLabel").pack(pady=(0, 15))
        card = ttk.Frame(outer, style="Card.TFrame", padding=28)
        card.pack(ipadx=30)

        entries = {}
        for label, key, show in [
            ("Full Name", "name", None), ("Email", "email", None), ("Phone", "phone", None),
            ("Password", "password", "*"), ("Confirm Password", "confirm", "*")
        ]:
            ttk.Label(card, text=label, style="CardText.TLabel").pack(anchor="w", pady=(5, 3))
            entries[key] = ttk.Entry(card, width=42, show=show)
            entries[key].pack(fill="x", ipady=4)

        def signup():
            name = entries["name"].get().strip()
            email = entries["email"].get().strip().lower()
            phone = entries["phone"].get().strip()
            password = entries["password"].get()
            if not all([name, email, phone, password]):
                messagebox.showwarning("Sign Up", "Please fill in all fields.")
                return
            if password != entries["confirm"].get():
                messagebox.showerror("Sign Up", "Passwords do not match.")
                return
            if self.account_exists(email):
                messagebox.showerror("Sign Up", "This email is already registered.")
                return
            user_id = len(self.customers) + len(self.admins) + 1
            customer_id = 100 + len(self.customers) + 1
            c = Customer(user_id, name, email, password, phone, customer_id)
            c.cart = Cart(customer_id, str(date.today()))
            c.orders = []
            c.reviews = []
            self.customers.append(c)
            messagebox.showinfo("Success", "Account created successfully.")
            self.show_login()

        ttk.Button(card, text="Create Account", command=signup, style="Accent.TButton").pack(fill="x", pady=(15, 10))
        ttk.Button(card, text="Back to Login", command=self.show_login).pack(fill="x")

    def logout(self):
        if self.current_user:
            self.current_user.logout()
        self.current_user = None
        self.show_login()

    # -------------------- Dashboards --------------------
    def dashboard_card(self, parent, title, description, command, row, col):
        card = ttk.Frame(parent, style="Card.TFrame", padding=22)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=description, style="CardText.TLabel", wraplength=280).pack(anchor="w", pady=(8, 15))
        ttk.Button(card, text="Open", command=command).pack(anchor="w")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)

    def show_customer_dashboard(self):
        self.clear()
        self.header(f"Welcome, {self.current_user.name}", "Customer Dashboard")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        cards = [
            ("Products", "Browse the catalog and add products to your cart.", self.show_products),
            ("My Cart", "Manage quantities, remove items and checkout.", self.show_cart),
            ("My Orders", "View orders and track their status.", self.show_orders),
            ("Profile", "Manage profile, address and reviews.", self.show_profile),
        ]
        for i, item in enumerate(cards):
            self.dashboard_card(body, *item, i // 2, i % 2)

    def show_admin_dashboard(self):
        self.clear()
        self.header(f"Welcome, {self.current_user.name}", "Admin Dashboard")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        cards = [
            ("Products", "Add, update prices/stock and delete products.", self.show_admin_products),
            ("Orders", "Review orders and update order status.", self.show_admin_orders),
            ("Shipments", "Track and update shipment status.", self.show_shipments),
            ("Profile", "View administrator account information.", self.show_admin_profile),
        ]
        for i, item in enumerate(cards):
            self.dashboard_card(body, *item, i // 2, i % 2)

    # -------------------- Products --------------------
    def product_tree(self, parent):
        tree = ttk.Treeview(parent, columns=("id", "name", "description", "price", "stock", "sku"), show="headings")
        for col, text, width in [
            ("id", "ID", 60), ("name", "Product", 190), ("description", "Description", 300),
            ("price", "Price (EGP)", 130), ("stock", "Stock", 90), ("sku", "SKU", 110)
        ]:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center")
        tree.pack(fill="both", expand=True)
        return tree

    def refresh_product_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for p in self.products:
            tree.insert("", "end", values=(p.productId, p.name, p.description, f"{p.price:,.2f}", p.stock, p.sku))

    def show_products(self):
        self.clear()
        self.header("Products", "Available products", self.show_customer_dashboard)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = self.product_tree(frame)
        self.refresh_product_tree(tree)

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)

        def add():
            product = self.selected_product(tree)
            if not product:
                return
            if not product.isAvailable():
                messagebox.showwarning("Stock", "Product is out of stock.")
                return
            quantity = simpledialog.askinteger("Quantity", "Enter quantity:", initialvalue=1, minvalue=1)
            if quantity is None:
                return
            if quantity > product.stock:
                messagebox.showwarning("Stock", "Not enough stock available.")
                return
            item = CartItem(quantity, product.price)
            item.product = product
            self.current_user.cart.addItem(item)
            self.calculate_cart_total()
            self.current_user.addToCart(product)
            messagebox.showinfo("Cart", f"{product.name} added to cart.")

        ttk.Button(controls, text="Add to Cart", command=add, style="Accent.TButton").pack(side="left")

    # -------------------- Cart / Checkout --------------------
    def show_cart(self):
        self.clear()
        self.header("My Cart", "Shopping cart", self.show_customer_dashboard)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("index", "product", "quantity", "unit", "subtotal"), show="headings")
        for col, text, width in [("index", "#", 50), ("product", "Product", 260), ("quantity", "Quantity", 100), ("unit", "Unit Price", 130), ("subtotal", "Subtotal", 140)]:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center")
        tree.pack(fill="both", expand=True)

        for i, item in enumerate(self.current_user.cart.items):
            product = getattr(item, "product", None)
            name = product.name if product else "Product"
            tree.insert("", "end", iid=str(i), values=(i + 1, name, item.quantity, f"{item.unitPrice:,.2f}", f"{item.calculateSubtotal():,.2f}"))

        total = self.calculate_cart_total()
        ttk.Label(frame, text=f"Total: {total:,.2f} EGP", style="Heading.TLabel").pack(anchor="e", pady=12)
        controls = ttk.Frame(frame)
        controls.pack(fill="x")

        def get_item():
            s = tree.selection()
            if not s:
                messagebox.showwarning("Cart", "Please select an item first.")
                return None
            return self.current_user.cart.items[int(s[0])]

        def update():
            item = get_item()
            if item:
                quantity = simpledialog.askinteger("Quantity", "New quantity:", initialvalue=item.quantity, minvalue=1)
                if quantity is not None:
                    product = getattr(item, "product", None)
                    if product and quantity > product.stock:
                        messagebox.showwarning("Stock", "Not enough stock available.")
                        return
                    item.updateQuantity(quantity)
                    self.show_cart()

        def remove():
            item = get_item()
            if item:
                self.current_user.cart.removeItem(item)
                self.show_cart()

        def clear_cart():
            self.current_user.cart.clearCart()
            self.show_cart()

        def checkout():
            if not self.current_user.cart.items:
                messagebox.showwarning("Checkout", "Your cart is empty.")
                return
            total = self.calculate_cart_total()
            if not messagebox.askyesno("Checkout", f"Confirm order for {total:,.2f} EGP?"):
                return

            order = Order(len(self.orders) + 1, str(date.today()), "Pending")
            for item in self.current_user.cart.items:
                oi = OrderItem(item.quantity, item.unitPrice)
                oi.calculateSubtotal()
                oi.product = getattr(item, "product", None)
                order.items.append(oi)
                if oi.product:
                    oi.product.stock -= oi.quantity
            order.total = total
            self.orders.append(order)
            self.current_user.orders.append(order)

            payment = Payment(len(self.payments) + 1, total, str(date.today()), "Pending", "Cash")
            payment.processPayment()
            self.payments.append(payment)

            address = getattr(self.current_user, "address", None)
            address_text = "No address"
            if address:
                address_text = f"{address.street}, {address.city}, {address.governorate}, {address.postalCode}"
            shipment = Shipment(len(self.shipments) + 1, address_text, str(date.today()), "Pending")
            self.shipments.append(shipment)
            order.shipment = shipment
            order.payment = payment

            self.current_user.cart.clearCart()
            self.current_user.placeOrder()
            messagebox.showinfo("Success", f"Order #{order.orderId} placed successfully.")
            self.show_orders()

        ttk.Button(controls, text="Update Quantity", command=update).pack(side="left", padx=4)
        ttk.Button(controls, text="Remove", command=remove).pack(side="left", padx=4)
        ttk.Button(controls, text="Clear Cart", command=clear_cart).pack(side="left", padx=4)
        ttk.Button(controls, text="Checkout", command=checkout, style="Accent.TButton").pack(side="left", padx=4)

    # -------------------- Orders / Payment / Shipment --------------------
    def show_orders(self):
        self.clear()
        self.header("My Orders", "Orders and payment status", self.show_customer_dashboard)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "date", "status", "total", "payment", "shipment"), show="headings")
        for col, text in [("id", "Order ID"), ("date", "Date"), ("status", "Order Status"), ("total", "Total"), ("payment", "Payment"), ("shipment", "Shipment")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for order in self.current_user.orders:
            payment = getattr(order, "payment", None)
            shipment = getattr(order, "shipment", None)
            tree.insert("", "end", iid=str(order.orderId), values=(order.orderId, order.orderDate, order.status, f"{order.total:,.2f}", payment.checkStatus() if payment else "-", shipment.trackShipment() if shipment else "-"))

        def cancel():
            s = tree.selection()
            if not s:
                messagebox.showwarning("Order", "Please select an order first.")
                return
            order = next(o for o in self.current_user.orders if str(o.orderId) == s[0])
            if order.status in ("Pending", "Processing"):
                order.cancelOrder()
                self.show_orders()
            else:
                messagebox.showwarning("Order", "This order cannot be cancelled now.")

        ttk.Button(frame, text="Cancel Selected Order", command=cancel).pack(side="left", pady=15)

    def show_shipments(self):
        self.clear()
        back = self.show_admin_dashboard if isinstance(self.current_user, Admin) else self.show_orders
        self.header("Shipments", "Shipment tracking", back)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "address", "date", "status"), show="headings")
        for col, text in [("id", "Shipment ID"), ("address", "Address"), ("date", "Date"), ("status", "Status")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for s in self.shipments:
            tree.insert("", "end", iid=str(s.shipmentId), values=(s.shipmentId, s.shippingAddress, s.shippingDate, s.status))

        if isinstance(self.current_user, Admin):
            def update():
                selection = tree.selection()
                if not selection:
                    messagebox.showwarning("Shipment", "Select a shipment first.")
                    return
                shipment = next(x for x in self.shipments if str(x.shipmentId) == selection[0])
                status = simpledialog.askstring("Shipment Status", "Enter: Pending, Shipped, In Transit, Delivered", initialvalue=shipment.status)
                if status:
                    shipment.updateStatus(status)
                    self.show_shipments()
            ttk.Button(frame, text="Update Status", command=update, style="Accent.TButton").pack(side="left", pady=15)

    # -------------------- Profile / Address / Reviews --------------------
    def show_profile(self):
        self.clear()
        self.header("My Profile", "Customer information", self.show_customer_dashboard)
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        c = self.current_user
        info = ttk.Frame(frame, style="Card.TFrame", padding=25)
        info.pack(fill="x")
        for label, value in [("Customer ID", c.customerId), ("Name", c.name), ("Email", c.email), ("Phone", c.phone), ("Loyalty Points", c.loyaltyPoints)]:
            ttk.Label(info, text=f"{label}: {value}", style="CardText.TLabel").pack(anchor="w", pady=5)

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=20)
        ttk.Button(buttons, text="Update Profile", command=self.update_customer_profile).pack(side="left", padx=4)
        ttk.Button(buttons, text="Address", command=self.show_address).pack(side="left", padx=4)
        ttk.Button(buttons, text="Reviews", command=self.show_reviews).pack(side="left", padx=4)

    def update_customer_profile(self):
        c = self.current_user
        dialog = tk.Toplevel(self)
        dialog.title("Update Profile")
        dialog.geometry("420x330")
        dialog.transient(self)
        dialog.grab_set()
        entries = {}
        for label, key, value in [("Name", "name", c.name), ("Email", "email", c.email), ("Phone", "phone", c.phone)]:
            ttk.Label(dialog, text=label).pack(anchor="w", padx=25, pady=(15, 3))
            e = ttk.Entry(dialog, width=42)
            e.insert(0, value)
            e.pack(padx=25, fill="x")
            entries[key] = e

        def save():
            email = entries["email"].get().strip().lower()
            if not email:
                messagebox.showwarning("Profile", "Email cannot be empty.", parent=dialog)
                return
            for u in self.customers + self.admins:
                if u is not c and u.email.lower() == email:
                    messagebox.showerror("Profile", "Email already exists.", parent=dialog)
                    return
            c.name = entries["name"].get().strip()
            c.email = email
            c.phone = entries["phone"].get().strip()
            messagebox.showinfo("Profile", "Profile updated successfully.", parent=dialog)
            dialog.destroy()
            self.show_profile()

        ttk.Button(dialog, text="Save", command=save, style="Accent.TButton").pack(pady=20)

    def show_address(self):
        self.clear()
        self.header("My Address", "Shipping address", self.show_profile)
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        address = getattr(self.current_user, "address", None)
        if not address:
            address = Address(1, "", "", "", "")
            self.current_user.address = address
        card = ttk.Frame(frame, style="Card.TFrame", padding=25)
        card.pack(fill="x")
        for label, value in [("Street", address.street), ("City", address.city), ("Governorate", address.governorate), ("Postal Code", address.postalCode)]:
            ttk.Label(card, text=f"{label}: {value}", style="CardText.TLabel").pack(anchor="w", pady=6)

        def edit():
            values = []
            for label, value in [("Street", address.street), ("City", address.city), ("Governorate", address.governorate), ("Postal Code", address.postalCode)]:
                values.append(simpledialog.askstring("Address", f"{label}:", initialvalue=value))
            if all(v is not None for v in values):
                address.updateAddress(*values)
                self.show_address()
        ttk.Button(frame, text="Update Address", command=edit, style="Accent.TButton").pack(anchor="w", pady=20)

    def show_reviews(self):
        self.clear()
        self.header("My Reviews", "Product reviews", self.show_profile)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "product", "rating", "comment", "date"), show="headings")
        for col, text in [("id", "ID"), ("product", "Product"), ("rating", "Rating"), ("comment", "Comment"), ("date", "Date")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for review in self.current_user.reviews:
            tree.insert("", "end", values=(review.reviewId, getattr(review, "product", "-"), review.rating, review.comment, review.reviewDate))

        def add_review():
            available = [o for o in self.current_user.orders if o.status != "Cancelled"]
            products = []
            for order in available:
                for item in getattr(order, "items", []):
                    if getattr(item, "product", None) and item.product not in products:
                        products.append(item.product)
            if not products:
                messagebox.showinfo("Reviews", "Buy a product first to review it.")
                return
            names = ", ".join(f"{p.productId}: {p.name}" for p in products)
            pid = simpledialog.askinteger("Review", f"Enter Product ID:\n{names}")
            product = next((p for p in products if p.productId == pid), None)
            if not product:
                messagebox.showwarning("Review", "Product not found in your orders.")
                return
            rating = simpledialog.askinteger("Review", "Rating (1-5):", minvalue=1, maxvalue=5)
            if rating is None:
                return
            comment = simpledialog.askstring("Review", "Comment:")
            if comment is None:
                return
            review = Review(len(self.reviews) + 1, rating, comment, str(date.today()))
            review.product = product.name
            self.reviews.append(review)
            self.current_user.reviews.append(review)
            review.addReview()
            self.show_reviews()

        ttk.Button(frame, text="Add Review", command=add_review, style="Accent.TButton").pack(side="left", pady=15)

    # -------------------- Admin --------------------
    def show_admin_products(self):
        self.clear()
        self.header("Manage Products", "Admin product management", self.show_admin_dashboard)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = self.product_tree(frame)
        self.refresh_product_tree(tree)

        def selected():
            return self.selected_product(tree)

        def add_product():
            dialog = tk.Toplevel(self)
            dialog.title("Add Product")
            dialog.geometry("430x440")
            dialog.transient(self)
            dialog.grab_set()
            fields = {}
            for label, key in [("Name", "name"), ("Description", "description"), ("Price", "price"), ("Stock", "stock"), ("SKU", "sku")]:
                ttk.Label(dialog, text=label).pack(anchor="w", padx=25, pady=(12, 3))
                fields[key] = ttk.Entry(dialog, width=42)
                fields[key].pack(padx=25, fill="x")

            def save():
                try:
                    name = fields["name"].get().strip()
                    description = fields["description"].get().strip()
                    price = float(fields["price"].get())
                    stock = int(fields["stock"].get())
                    sku = fields["sku"].get().strip()
                    if not name or price < 0 or stock < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Product", "Enter valid product data.", parent=dialog)
                    return
                pid = max((p.productId for p in self.products), default=0) + 1
                product = Product(pid, name, description, price, stock, sku)
                self.products.append(product)
                self.current_user.addProduct(product)
                dialog.destroy()
                self.show_admin_products()

            ttk.Button(dialog, text="Add Product", command=save, style="Accent.TButton").pack(pady=20)

        def update_product():
            p = selected()
            if not p:
                return
            price = simpledialog.askfloat("Price", "New price:", initialvalue=p.price, minvalue=0)
            if price is not None:
                p.updatePrice(price)
            stock = simpledialog.askinteger("Stock", "New stock:", initialvalue=p.stock, minvalue=0)
            if stock is not None:
                p.updateStock(stock)
            self.current_user.updateProduct(p)
            self.show_admin_products()

        def delete_product():
            p = selected()
            if not p:
                return
            if messagebox.askyesno("Delete", f"Delete {p.name}?"):
                self.products.remove(p)
                self.current_user.deleteProduct(p)
                self.show_admin_products()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add Product", command=add_product, style="Accent.TButton").pack(side="left", padx=4)
        ttk.Button(controls, text="Update Price / Stock", command=update_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Delete", command=delete_product).pack(side="left", padx=4)

    def show_admin_orders(self):
        self.clear()
        self.header("Manage Orders", "All customer orders", self.show_admin_dashboard)
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "customer", "date", "status", "total"), show="headings")
        for col, text in [("id", "Order ID"), ("customer", "Customer"), ("date", "Date"), ("status", "Status"), ("total", "Total")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for c in self.customers:
            for o in c.orders:
                tree.insert("", "end", iid=str(o.orderId), values=(o.orderId, c.name, o.orderDate, o.status, f"{o.total:,.2f}"))

        def update_status():
            s = tree.selection()
            if not s:
                messagebox.showwarning("Order", "Select an order first.")
                return
            order = next((o for c in self.customers for o in c.orders if str(o.orderId) == s[0]), None)
            if not order:
                return
            status = simpledialog.askstring("Order Status", "Enter: Pending, Processing, Shipped, Delivered, Cancelled", initialvalue=order.status)
            if status:
                order.updateStatus(status)
                self.show_admin_orders()

        ttk.Button(frame, text="Update Status", command=update_status, style="Accent.TButton").pack(side="left", pady=15)

    def show_admin_profile(self):
        self.clear()
        self.header("Admin Profile", "Administrator information", self.show_admin_dashboard)
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        a = self.current_user
        card = ttk.Frame(frame, style="Card.TFrame", padding=25)
        card.pack(fill="x")
        for label, value in [("Admin ID", a.adminId), ("Name", a.name), ("Email", a.email), ("Phone", a.phone), ("Role", a.role)]:
            ttk.Label(card, text=f"{label}: {value}", style="CardText.TLabel").pack(anchor="w", pady=6)


if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
