class OrderItem:
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price
        self.subtotal = self.quantity * self.unit_price

    def calculate_subtotal(self) -> float:
        self.subtotal = self.quantity * self.unit_price
        return self.subtotal
