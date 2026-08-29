from .cart_item import CartItem


class Cart:
    def __init__(self, cart_id: int):
        self.cart_id = cart_id
        self.created_at = None
        self.items = []

    @property
    def total(self) -> float:
        return self.get_total()

    def add_item(self, product, quantity=1):
        for item in self.items:
            if item.product is product:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def remove_item(self, product):
        self.items = [item for item in self.items if item.product is not product]

    def get_total(self) -> float:
        return sum(item.subtotal() for item in self.items)
