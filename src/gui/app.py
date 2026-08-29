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
        self.geometry("1180x720")
        self.minsize(1000, 650)
        self.configure(bg="#f5f7fb")

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

        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="white")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#172033",
                        font=("Segoe UI", 28, "bold"))
        style.configure("Subtitle.TLabel", background="#f5f7fb", foreground="#667085",
                        font=("Segoe UI", 11))
        style.configure("Heading.TLabel", background="#f5f7fb", foreground="#172033",
                        font=("Segoe UI", 18, "bold"))
        style.configure("CardTitle.TLabel", background="white", foreground="#172033",
                        font=("Segoe UI", 13, "bold"))
        style.configure("CardText.TLabel", background="white", foreground="#667085",
                        font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()

        outer = ttk.Frame(self, padding=40)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="E-Commerce", style="Title.TLabel").pack(pady=(35, 0))
        ttk.Label(outer, text="Sign in to your account", style="Subtitle.TLabel").pack(pady=(5, 28))

        card = ttk.Frame(outer, style="Card.TFrame", padding=35)
        card.pack(pady=5, ipadx=35, ipady=20)

        ttk.Label(card, text="Welcome back", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="Enter your account credentials to continue.",
                  style="CardText.TLabel").pack(anchor="w", pady=(3, 20))

        ttk.Label(card, text="Email", style="CardText.TLabel").pack(anchor="w")
        email = ttk.Entry(card, width=38)
        email.pack(pady=(5, 15), ipady=5)
        email.insert(0, "hassan@gmail.com")

        ttk.Label(card, text="Password", style="CardText.TLabel").pack(anchor="w")
        password = ttk.Entry(card, width=38, show="*")
        password.pack(pady=(5, 20), ipady=5)
        password.insert(0, "1234")

        def do_login():
            entered_email = email.get().strip()
            entered_password = password.get()

            if entered_email == self.customer.email and entered_password == self.customer.password:
                self.login(self.customer)
            elif entered_email == self.admin.email and entered_password == self.admin.password:
                self.login(self.admin)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")

        ttk.Button(card, text="Login", command=do_login, style="Accent.TButton",
                   width=30).pack(fill="x", pady=(0, 15))

        ttk.Label(card, text="Demo Accounts", style="CardTitle.TLabel").pack(anchor="w", pady=(8, 8))
        ttk.Label(card, text="Customer: hassan@gmail.com / 1234", style="CardText.TLabel").pack(anchor="w")
        ttk.Label(card, text="Admin: admin@ecommerce.com / admin", style="CardText.TLabel").pack(anchor="w", pady=(3, 0))

        ttk.Button(outer, text="Exit", command=self.destroy).pack(pady=20)

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

    def header(self, title, subtitle=""):
        top = ttk.Frame(self, padding=(30, 22))
        top.pack(fill="x")
        left = ttk.Frame(top)
        left.pack(side="left")
        ttk.Label(left, text=title, style="Heading.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(left, text=subtitle, style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Button(top, text="Logout", command=self.logout).pack(side="right")

    def make_card(self, parent, title, description, command):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.pack_propagate(False)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=description, style="CardText.TLabel", wraplength=280).pack(anchor="w", pady=(8, 15))
        ttk.Button(card, text="Open", command=command).pack(anchor="w")
        return card

    def show_customer_dashboard(self):
        self.clear_window()
        self.header(f"Welcome, {self.customer.name}", "Customer Dashboard")

        body = ttk.Frame(self, padding=(30, 5, 30, 30))
        body.pack(fill="both", expand=True)

        cards = [
            ("Products", "Browse products and add items to your cart.", self.show_products),
            ("My Cart", "Review items, change quantities and checkout.", self.show_cart),
            ("My Orders", "View your orders and cancel eligible orders.", self.show_orders),
            ("My Profile", "View and update your customer information.", self.show_profile),
            ("Address", "Add or update your delivery address.", self.show_address),
            ("Reviews", "Create and view your product reviews.", self.show_reviews),
        ]
        for i, (title, desc, command) in enumerate(cards):
            row, col = divmod(i, 3)
            card = self.make_card(body, title, desc, command)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.pack_forget()
            card.grid_propagate(False)
            card.configure(width=300, height=145)
            body.columnconfigure(col, weight=1)
            body.rowconfigure(row, weight=1)

    def show_products(self):
        self.clear_window()
        self.header("Products", "Choose a product to add to your cart")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("id", "name", "description", "price", "stock", "sku"), show="headings")
        headings = [("id", "ID"), ("name", "Product"), ("description", "Description"),
                    ("price", "Price"), ("stock", "Stock"), ("sku", "SKU")]
        for col, text in headings:
            tree.heading(col, text=text)
        tree.column("id", width=55)
        tree.column("name", width=180)
        tree.column("description", width=260)
        tree.column("price", width=110)
        tree.column("stock", width=80)
        tree.column("sku", width=110)
        tree.pack(fill="both", expand=True)

        for product in self.products:
            tree.insert("", "end", iid=str(product.productId), values=(
                product.productId, product.name, product.description,
                f"{product.price:.2f}", product.stock, product.sku))

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
            self.refresh_cart_total()
            messagebox.showinfo("Cart", f"{product.name} added to cart.")

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add to Cart", command=add_selected, style="Accent.TButton").pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def refresh_cart_total(self):
        total = sum(item.calculateSubtotal() for item in self.customer.cart.items)
        self.customer.cart.totalAmount = total

    def show_cart(self):
        self.clear_window()
        self.header("My Cart", "Review your shopping cart")
        self.refresh_cart_total()
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("product", "quantity", "unit", "subtotal"), show="headings")
        for col, text in [("product", "Product"), ("quantity", "Quantity"), ("unit", "Unit Price"), ("subtotal", "Subtotal")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)

        for index, item in enumerate(self.customer.cart.items):
            product = getattr(item, "product", None)
            name = product.name if product else "Product"
            tree.insert("", "end", iid=str(index), values=(name, item.quantity,
                        f"{item.unitPrice:.2f}", f"{item.calculateSubtotal():.2f}"))

        ttk.Label(frame, text=f"Total: {self.customer.cart.getTotal():.2f}",
                  style="Heading.TLabel").pack(anchor="e", pady=12)

        controls = ttk.Frame(frame)
        controls.pack(fill="x")

        def selected_item():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Select Item", "Please select an item first.")
                return None
            return self.customer.cart.items[int(selection[0])]

        def remove_selected():
            item = selected_item()
            if item:
                self.customer.cart.removeItem(item)
                self.show_cart()

        def update_selected():
            item = selected_item()
            if not item:
                return
            quantity = simpledialog.askinteger("Quantity", "New quantity:", initialvalue=item.quantity, minvalue=1)
            if quantity is not None:
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
                order_item = OrderItem(item.quantity, item.unitPrice)
                order_item.calculateSubtotal()
                order_item.product = getattr(item, "product", None)
                order.items.append(order_item)
            order.total = self.customer.cart.getTotal()
            self.orders.append(order)
            self.customer.orders.append(order)
            payment = Payment(len(self.payments) + 1, order.total, str(date.today()), method="Cash")
            self.payments.append(payment)
            self.customer.cart.clearCart()
            messagebox.showinfo("Checkout", f"Order #{order.orderId} created successfully.")
            self.show_orders()

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
        for order in self.customer.orders:
            tree.insert("", "end", values=(order.orderId, order.orderDate, order.status, f"{order.total:.2f}"))

        def cancel_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Select Order", "Please select an order first.")
                return
            order_id = int(tree.item(selection[0], "values")[0])
            order = next(o for o in self.customer.orders if o.orderId == order_id)
            order.cancelOrder()
            self.show_orders()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Cancel Selected", command=cancel_selected).pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_customer_dashboard).pack(side="right")

    def show_profile(self):
        self.clear_window()
        self.header("My Profile", "Customer account information")
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        info = [
            ("Customer ID", self.customer.customerId),
            ("Name", self.customer.name),
            ("Email", self.customer.email),
            ("Phone", self.customer.phone),
            ("Loyalty Points", self.customer.loyaltyPoints),
        ]
        for label, value in info:
            ttk.Label(frame, text=f"{label}: {value}", style="CardTitle.TLabel").pack(anchor="w", pady=8)

        def update():
            name = simpledialog.askstring("Name", "New name:", initialvalue=self.customer.name)
            if name is None: return
            email = simpledialog.askstring("Email", "New email:", initialvalue=self.customer.email)
            if email is None: return
            phone = simpledialog.askstring("Phone", "New phone:", initialvalue=self.customer.phone)
            if phone is None: return
            self.customer.name, self.customer.email, self.customer.phone = name, email, phone
            self.show_profile()

        ttk.Button(frame, text="Update Profile", command=update, style="Accent.TButton").pack(anchor="w", pady=20)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(anchor="e")

    def show_address(self):
        self.clear_window()
        self.header("My Address", "Delivery address")
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        if self.addresses:
            address = self.addresses[0]
            ttk.Label(frame, text=f"{address.street}, {address.city}", style="CardTitle.TLabel").pack(anchor="w", pady=5)
            ttk.Label(frame, text=f"{address.governorate} - {address.postalCode}", style="CardText.TLabel").pack(anchor="w")
        else:
            ttk.Label(frame, text="No address saved.", style="CardText.TLabel").pack(anchor="w", pady=10)

        def save_address():
            values = []
            for title in ("Street", "City", "Governorate", "Postal Code"):
                value = simpledialog.askstring(title, f"Enter {title.lower()}:")
                if value is None: return
                values.append(value)
            if self.addresses:
                self.addresses[0].updateAddress(*values)
            else:
                self.addresses.append(Address(1, *values))
            self.show_address()

        ttk.Button(frame, text="Add / Update Address", command=save_address, style="Accent.TButton").pack(anchor="w", pady=20)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(anchor="e")

    def show_reviews(self):
        self.clear_window()
        self.header("Reviews", "Your product reviews")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "rating", "comment", "date"), show="headings")
        for col, text in [("id", "ID"), ("rating", "Rating"), ("comment", "Comment"), ("date", "Date")]:
            tree.heading(col, text=text)
        tree.pack(fill="both", expand=True)
        for review in self.reviews:
            tree.insert("", "end", values=(review.reviewId, review.rating, review.comment, review.reviewDate))

        def add_review():
            rating = simpledialog.askinteger("Rating", "Rating (1-5):", minvalue=1, maxvalue=5)
            if rating is None: return
            comment = simpledialog.askstring("Comment", "Your comment:")
            if comment is None: return
            review = Review(len(self.reviews) + 1, rating, comment, str(date.today()))
            self.reviews.append(review)
            review.addReview()
            self.show_reviews()

        ttk.Button(frame, text="Add Review", command=add_review, style="Accent.TButton").pack(side="left", pady=15)
        ttk.Button(frame, text="Back", command=self.show_customer_dashboard).pack(side="right", pady=15)

    def show_admin_dashboard(self):
        self.clear_window()
        self.header(f"Welcome, {self.admin.name}", "Administrator Dashboard")
        body = ttk.Frame(self, padding=30)
        body.pack(fill="both", expand=True)
        cards = [
            ("Manage Products", "Add, update and delete products.", self.admin_products),
            ("Manage Orders", "View orders and update their status.", self.admin_orders),
            ("Admin Profile", "View administrator account information.", self.admin_profile),
        ]
        for i, (title, desc, command) in enumerate(cards):
            card = self.make_card(body, title, desc, command)
            card.grid(row=0, column=i, padx=10, pady=25, sticky="nsew")
            card.pack_forget()
            card.grid_propagate(False)
            card.configure(width=320, height=160)
            body.columnconfigure(i, weight=1)

    def admin_products(self):
        self.clear_window()
        self.header("Manage Products", "Administrator controls")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "name", "price", "stock", "sku"), show="headings")
        for col, text in [("id", "ID"), ("name", "Product"), ("price", "Price"), ("stock", "Stock"), ("sku", "SKU")]:
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
            self.categories[0].addProduct(product)
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
            if messagebox.askyesno("Delete Product", f"Delete {product.name}?"):
                self.products.remove(product)
                self.categories[0].removeProduct(product)
                self.admin.deleteProduct(product)
                refresh()

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=15)
        ttk.Button(controls, text="Add Product", command=add_product, style="Accent.TButton").pack(side="left", padx=4)
        ttk.Button(controls, text="Update Product", command=update_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Delete Product", command=delete_product).pack(side="left", padx=4)
        ttk.Button(controls, text="Back", command=self.show_admin_dashboard).pack(side="right")

    def admin_orders(self):
        self.clear_window()
        self.header("Manage Orders", "Administrator order management")
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("id", "customer", "date", "status", "total"), show="headings")
        for col, text in [("id", "Order ID"), ("customer", "Customer"), ("date", "Date"), ("status", "Status"), ("total", "Total")]:
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
        ttk.Button(controls, text="Update Status", command=update_status, style="Accent.TButton").pack(side="left")
        ttk.Button(controls, text="Back", command=self.show_admin_dashboard).pack(side="right")

    def admin_profile(self):
        self.clear_window()
        self.header("Admin Profile", "Administrator account information")
        frame = ttk.Frame(self, padding=35)
        frame.pack(fill="both", expand=True)
        info = [
            ("Admin ID", self.admin.adminId),
            ("Name", self.admin.name),
            ("Email", self.admin.email),
            ("Phone", self.admin.phone),
            ("Role", self.admin.role),
        ]
        for label, value in info:
            ttk.Label(frame, text=f"{label}: {value}", style="CardTitle.TLabel").pack(anchor="w", pady=8)
        ttk.Button(frame, text="Back", command=self.show_admin_dashboard).pack(anchor="e", pady=20)


if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
