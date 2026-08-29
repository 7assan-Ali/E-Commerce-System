class Product:
    def __init__(self, product_id: int, name: str, description: str, price: float, stock: int, sku: str, category=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.sku = sku
        self.category = category

    def update_price(self, price: float):
        self.price = price

    def update_stock(self, quantity: int):
        self.stock = quantity

    def is_available(self) -> bool:
        return self.stock > 0
