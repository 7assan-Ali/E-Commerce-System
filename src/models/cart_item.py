class CartItem:
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price

    def subtotal(self) -> float:
        return self.quantity * self.unit_price
