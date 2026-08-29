import os
import sys
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from customer import Customer
from admin import Admin
from product import Product
from cart import Cart
from cart_item import CartItem
from order import Order
from order_item import OrderItem
from payment import Payment


class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce System")
        self.geometry("1180x720")
        self.minsize(950, 600)
        self.configure(bg="#f5f7fb")

        self.products = [
            Product(1, "Laptop", "Dell Laptop", 25000.50, 10, "DELL001"),
            Product(2, "Wireless Mouse", "Wireless Mouse", 500.0, 25, "MOU001"),
            Product(3, "Keyboard", "Mechanical Keyboard", 1500.0, 15, "KEY001"),
            Product(4, "Headphones", "Wireless Headphones", 2200.0, 12, "HDP001"),
        ]

        self.customer_accounts = [
            Customer(1, "Hassan", "hassan@gmail.com", "1234", "01012345678", 101)
        ]
        self.admin_accounts = [
            Admin(2, "System Admin", "admin@ecommerce.com", "admin", "01000000000", 1, "Administrator")
        ]

        for customer in self.customer_accounts:
            customer.cart = Cart(customer.customerId, str(date.today()))
            customer.orders = []

        self.orders = []
        self.payments = []
        self.current_user = None

        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="white")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 28, "bold"))
        style.configure("Subtitle.TLabel", background="#f5f7fb", foreground="#667085", font=("Segoe UI", 11))
        style.configure("Heading.TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 18, "bold"))
        style.configure("CardTitle.TLabel", background="white", foreground="#172033", font=("Segoe UI", 14, "bold"))
        style.configure("CardText.TLabel", background="white", foreground="#667085", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ==================== AUTH ====================
    def show_login(self):
        self.clear_window()

        outer = ttk.Frame(self, padding=40)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="E-Commerce System", style="Title.TLabel").pack(pady=(30, 2))
        ttk.Label(outer, text="Sign in to your account", style="Subtitle.TLabel").pack(pady=(0, 25))

        card = ttk.Frame(outer, style="Card.TFrame", padding=35)
        card.pack(pady=5, ipadx=35)

        ttk.Label(card, text="Welcome Back", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="Login as Customer or Admin", style="CardText.TLabel").pack(anchor="w", pady=(4, 20))

        ttk.Label(card, text="Email", style="CardText.TLabel").pack(anchor="w")
        email = ttk.Entry(card, width=42)
        email.pack(fill="x", pady=(5, 12), ipady=5)

        ttk.Label(card, text="Password", style="CardText.TLabel").pack(anchor="w")
        password = ttk.Entry(card, width=42, show="*")
        password.pack(fill="x", pady=(5, 16), ipady=5)

        def do_login():
            entered_email = email.get().strip().lower()
            entered_password = password.get()

            for user in self.customer_accounts + self.admin_accounts:
                if user.email.lower() == entered_email and user.password == entered_password:
                    user.login()
                    self.current_user = user
                    if isinstance(user, Admin):
                        self.show_admin_dashboard()
                    else:
                        self.show_customer_dashboard()
                    return

            messagebox.showerror("Login Failed", "Invalid email or password.")

        ttk.Button(card, text="Login", command=do_login, style="Accent.TButton").pack(fill="x", pady=(0, 12))

        signup_frame = ttk.Frame(card, style="Card.TFrame")
        signup_frame.pack()
        ttk.Label(signup_frame, text="Don't have an account?", style="CardText.TLabel").pack(side="left")
        ttk.Button(signup_frame, text="Sign Up", command=self.show_signup).pack(side="left", padx=5)

        # Passwords and account credentials are intentionally not displayed here.
        ttk.Button(outer, text="Exit", command=self.destroy).pack(pady=20)

    def show_signup(self):
        self.clear_window()

        outer = ttk.Frame(self, padding=30)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Create Account", style="Title.TLabel").pack(pady=(10, 2))
        ttk.Label(outer, text="Create a new Customer account", style="Subtitle.TLabel").pack(pady=(0, 15))

        card = ttk.Frame(outer, style="Card.TFrame", padding=28)
        card.pack(pady=5, ipadx=30)

        def make_field(label, show=None):
            ttk.Label(card, text=label, style="CardText.TLabel").pack(anchor="w", pady=(5, 3))
            entry = ttk.Entry(card, width=42, show=show)
            entry.pack(fill="x", ipady=4)
            return entry

        name = make_field("Full Name")
        email = make_field("Email")
        phone = make_field("Phone")
        password = make_field("Password", "*")
        confirm = make_field("Confirm Password", "*")

        def create_account():
            name_v = name.get().strip()
            email_v = email.get().strip().lower()
            phone_v = phone.get().strip()
            password_v = password.get()

            if not all([name_v, email_v, phone_v, password_v]):
                messagebox.showwarning("Missing Data", "Please fill in all fields.")
                return

            if password_v != confirm.get():
                messagebox.showerror("Password", "Passwords do not match.")
                return

            all_accounts = self.customer_accounts + self.admin_accounts
            if any(account.email.lower() == email_v for account in all_accounts):
                messagebox.showerror("Account Exists", "This email is already registered.")
                return

            new_user_id = len(all_accounts) + 1
            new_customer_id = 100 + len(self.customer_accounts) + 1
            customer = Customer(new_user_id, name_v, email_v, password_v, phone_v, new_customer_id)
            customer.cart = Cart(new_customer_id, str(date.today()))
            customer.orders = []
            self.customer_accounts.append(customer)

            messagebox.showinfo("Success", "Customer account created successfully.")
            self.show_login()

        ttk.Button(card, text="Create Account", command=create_account, style="Accent.TButton").pack(fill="x", pady=(15, 10))
        ttk.Button(card, text="Back to Login", command=self.show_login).pack(fill="x")

    def logout(self):
        if self.current_user:
            self.current_user.logout()
        self.current_user = None
        self.show_login()

    # ==================== DASHBOARDS ====================
    def header(self, title, subtitle=""):
        top = ttk.Frame(self, padding=(30, 22))
        top.pack(fill="x")
        left = ttk.Frame(top)
        left.pack(side="left")
        ttk.Label(left, text=title, style="Heading.TLabel").pack(anchor="w")
        ttk.Label(left, text=subtitle, style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Button(top, text="Logout", command=self.logout).pack(side="right")

    def make_card(self, parent, title, description, command):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=description, style="CardText.TLabel", wraplength=260).pack(anchor="w", pady=(8, 15))
        ttk.Button(card, text="Open", command=command).pack(anchor="w")
        return card

    def show_customer_dashboard(self):
        self.clear_window()
        self.header(f"Welcome, {self.current_user.name}", "Customer Dashboard")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        cards = [
            ("Products", "Browse products and add items to your cart.", self.show_products),
            ("My Cart", "Review items, update quantities and checkout.", self.show_cart),
            ("My Orders", "View your previous orders.", self.show_orders),
            ("My Profile", "View and update your profile.", self.show_profile),
        ]
        for i, (title, desc, command) in enumerate(cards):
            row, col = divmod(i, 2)
            card = self.make_card(body, title, desc, command)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            body.columnconfigure(col, weight=1)
            body.rowconfigure(row, weight=1)

    def show_admin_dashboard(self):
        self.clear_window()
        self.header(f"Welcome, {self.current_user.name}", "Admin Dashboard")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        cards = [
            ("Manage Products", "Add, update and delete products.", self.show_admin_products),
            ("Manage Orders", "View and manage customer orders.", self.show_admin_orders),
            ("Admin Profile", "View administrator information.", self.show_admin_profile),
        ]
        for i, (title, desc, command) in enumerate(cards):
            card = self.make_card(body, title, desc, command)
            card.grid(row=0, column=i, padx=10, pady=20, sticky="nsew")
            body.columnconfigure(i, weight=1)

    # ==================== CUSTOMER PAGES ====================
    def show_products(self):
        self.clear_window()
        self.header("Products", "Browse available products")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "name", "description", "price", "stock", "sku"), show="headings")
        for col, text in [("id", "ID"), ("name", "Product"), ("description", "Description"), ("price", "Price"), ("stock", "Stock"), ("sku", "SKU")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for p in self.products:
            tree.insert("", "end", iid=str(p.productId), values=(p.productId, p.name, p.description, f"{p.price:.2f}", p.stock, p.sku))

        def add_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Product", "Please select a product first.")
                return
            product = next(p for p in self.products if str(p.productId) == selection[0])
            if not product.isAvailable():
                messagebox.showwarning("Stock", "This product is out of stock.")
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
            messagebox.showinfo("Cart", f"{product.name} added to cart.")

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add to Cart", command=add_selected, style="Accent.TButton").pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def calculate_cart_total(self):
        self.current_user.cart.totalAmount = sum(item.calculateSubtotal() for item in self.current_user.cart.items)
        return self.current_user.cart.totalAmount

    def show_cart(self):
        self.clear_window()
        self.header("My Cart", "Review and manage your items")
        self.calculate_cart_total()
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("product", "quantity", "unit", "subtotal"), show="headings")
        for col, text in [("product", "Product"), ("quantity", "Quantity"), ("unit", "Unit Price"), ("subtotal", "Subtotal")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for index, item in enumerate(self.current_user.cart.items):
            product = getattr(item, "product", None)
            tree.insert("", "end", iid=str(index), values=(product.name if product else "Product", item.quantity, f"{item.unitPrice:.2f}", f"{item.calculateSubtotal():.2f}"))
        ttk.Label(frame, text=f"Total: {self.current_user.cart.getTotal():.2f}", style="Heading.TLabel").pack(anchor="e", pady=12)

        def selected_item():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Cart", "Please select an item first.")
                return None
            return self.current_user.cart.items[int(selection[0])]

        def remove_selected():
            item = selected_item()
            if item:
                self.current_user.cart.removeItem(item)
                self.show_cart()

        def update_selected():
            item = selected_item()
            if not item:
                return
            quantity = simpledialog.askinteger("Quantity", "New quantity:", initialvalue=item.quantity, minvalue=1)
            if quantity is not None:
                item.updateQuantity(quantity)
                self.calculate_cart_total()
                self.show_cart()

        def checkout():
            if not self.current_user.cart.items:
                messagebox.showwarning("Checkout", "Your cart is empty.")
                return
            self.calculate_cart_total()
            order = Order(len(self.orders) + 1, str(date.today()), "Pending")
            order.items = []
            order.total = self.current_user.cart.totalAmount
            for item in self.current_user.cart.items:
                order_item = OrderItem(item.quantity, item.unitPrice)
                order_item.calculateSubtotal()
                order_item.product = getattr(item, "product", None)
                order.items.append(order_item)
                product = getattr(item, "product", None)
                if product:
                    product.stock -= item.quantity
            self.orders.append(order)
            self.current_user.orders.append(order)
            self.payments.append(Payment(len(self.payments) + 1, order.total, str(date.today()), "Pending", "Cash"))
            self.current_user.cart.clearCart()
            messagebox.showinfo("Checkout", f"Order #{order.orderId} created successfully.")
            self.show_orders()

        controls = ttk.Frame(frame)
        controls.pack(fill="x")
        ttk.Button(controls, text="Update Quantity", command=update_selected).pack(side="left", padx=4)
        ttk.Button(controls, text="Remove", command=remove_selected).pack(side="left", padx=4)
        ttk.Button(controls, text="Checkout", command=checkout, style="Accent.TButton").pack(side="left", padx=4)
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def show_orders(self):
        self.clear_window()
        self.header("My Orders", "Track your orders")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "date", "status", "total"), show="headings")
        for col, text in [("id", "Order ID"), ("date", "Date"), ("status", "Status"), ("total", "Total")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for order in self.current_user.orders:
            tree.insert("", "end", values=(order.orderId, order.orderDate, order.status, f"{order.total:.2f}"))

        def cancel_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Order", "Please select an order first.")
                return
            order_id = int(tree.item(selection[0], "values")[0])
            order = next(o for o in self.current_user.orders if o.orderId == order_id)
            if order.status.lower() == "pending":
                order.canceledOrder()
                self.show_orders()
            else:
                messagebox.showwarning("Order", "Only pending orders can be cancelled.")

        ttk.Button(frame, text="Cancel Selected", command=cancel_selected).pack(side="left", pady=15)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(side="right", pady=15)

    def show_profile(self):
        self.clear_window()
        self.header("My Profile", "Customer account information")
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        c = self.current_user
        for label, value in [("Customer ID", c.customerId), ("Name", c.name), ("Email", c.email), ("Phone", c.phone), ("Loyalty Points", c.loyaltyPoints)]:
            ttk.Label(frame, text=f"{label}: {value}", style="Heading.TLabel").pack(anchor="w", pady=8)
        ttk.Button(frame, text="Update Profile", command=c.updateProfile).pack(side="left", pady=20)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(side="right", pady=20)

    # ==================== ADMIN PAGES ====================
    def show_admin_products(self):
        self.clear_window()
        self.header("Manage Products", "Administrator product management")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "name", "price", "stock", "sku"), show="headings")
        for col, text in [("id", "ID"), ("name", "Product"), ("price", "Price"), ("stock", "Stock"), ("sku", "SKU")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)

        def refresh():
            for row in tree.get_children():
                tree.delete(row)
            for p in self.products:
                tree.insert("", "end", iid=str(p.productId), values=(p.productId, p.name, f"{p.price:.2f}", p.stock, p.sku))
        refresh()

        def selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Product", "Please select a product first.")
                return None
            return next(p for p in self.products if str(p.productId) == selection[0])

        def add_product():
            pid = max((p.productId for p in self.products), default=0) + 1
            product = Product(pid, "New Product", "Product description", 0.0, 0, f"SKU{pid:03d}")
            self.products.append(product)
            self.current_user.addProduct(product)
            refresh()

        def update_product():
            product = selected()
            if not product:
                return
            price = simpledialog.askfloat("Price", "New price:", initialvalue=product.price, minvalue=0)
            if price is not None:
                product.updatePrice(price)
            stock = simpledialog.askinteger("Stock", "New stock:", initialvalue=product.stock, minvalue=0)
            if stock is not None:
                product.updateStock(stock)
            self.current_user.updateProduct(product)
            refresh()

        def delete_product():
            product = selected()
            if not product:
                return
            if messagebox.askyesno("Delete Product", f"Delete {product.name}?"):
                self.products.remove(product)
                self.current_user.deleteProduct(product)
                refresh()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add Product", command=add_product, style="Accent.TButton").pack(side="left", padx=4)
        ttk.Button(controls, text="Update", command=update_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Delete", command=delete_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Back", command=self.show_admin_dashboard).pack(side="right")

    def show_admin_orders(self):
        self.clear_window()
        self.header("Manage Orders", "Administrator order management")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "customer", "status", "total"), show="headings")
        for col, text in [("id", "Order ID"), ("customer", "Customer"), ("status", "Status"), ("total", "Total")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for customer in self.customer_accounts:
            for order in customer.orders:
                tree.insert("", "end", values=(order.orderId, customer.name, order.status, f"{order.total:.2f}"))

        ttk.Button(frame, text="Back", command=self.show_admin_dashboard).pack(side="right", pady=15)

    def show_admin_profile(self):
        self.clear_window()
        self.header("Admin Profile", "Administrator account information")
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        a = self.current_user
        for label, value in [("Admin ID", a.adminId), ("Name", a.name), ("Email", a.email), ("Phone", a.phone), ("Role", a.role)]:
            ttk.Label(frame, text=f"{label}: {value}", style="Heading.TLabel").pack(anchor="w", pady=8)
        ttk.Button(frame, text="Back", command=self.show_admin_dashboard).pack(side="right", pady=20)


if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
