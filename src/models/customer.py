from .user import User


class Customer(User):
    def __init__(self, user_id: int, name: str, email: str, password: str, phone: str,
                 customer_id: int, loyalty_points: int = 0):
        super().__init__(user_id, name, email, password, phone)
        self.customer_id = customer_id
        self.loyalty_points = loyalty_points
        self.addresses = []
        self.cart = None
        self.orders = []
        self.reviews = []

    def browse_products(self, products):
        return products

    def add_to_cart(self, product, quantity=1):
        if self.cart is None:
            from .cart import Cart
            self.cart = Cart(self.customer_id)
        self.cart.add_item(product, quantity)

    def place_order(self):
        from .order import Order
        order = Order(len(self.orders) + 1, self.cart)
        self.orders.append(order)
        return order

    def cancel_order(self, order):
        return order.cancel()

    def review_product(self, product, rating, comment=""):
        from .review import Review
        review = Review(self.customer_id, product.product_id, rating, comment)
        self.reviews.append(review)
        return review
