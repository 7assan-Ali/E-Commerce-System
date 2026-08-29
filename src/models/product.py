class Product:
    def __init__(
        self,
        productId: int,
        name: str,
        description: str,
        price: float,
        stock: int,
        sku: str
    ):
        self.productId = productId
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.sku = sku

    def updatePrice(self, newPrice: float) -> None:
        if newPrice < 0:
            print("The price must be positive.")
            return

        self.price = newPrice
        print(f"Price updated successfully.")
        print(f"New price: {self.price}")

    def updateStock(self, newStock: int) -> None:
        if newStock < 0:
            print("The stock must be positive.")
            return

        self.stock = newStock
        print(f"Stock updated successfully.")
        print(f"New stock: {self.stock}")

    def isAvailable(self) -> bool:
        return self.stock > 0