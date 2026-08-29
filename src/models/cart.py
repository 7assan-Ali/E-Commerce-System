class Cart:
    def __init__(self, cartId: int, createdAt: str):
        self.cartId = cartId
        self.createdAt = createdAt
        self.totalAmount = 0.0
        self.items = []

    def addItem(self, item) -> None:
        if item not in self.items:
            self.items.append(item)
            print(f"The product {item} added to cart successfully")
        else:
            print(f"The product {item} already exists in the cart.")

    def removeItem(self, item) -> None:
        if item in self.items:
            self.items.remove(item)
            print(f"The product {item} removed from cart successfully")
        else:
            print(f"Product {item} not found in the cart.")

    def updateQuantity(self, item, quantity: int) -> None:
        if item not in self.items:
            print("Item not found in the cart.")
            return

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        item.quantity = quantity
        self.calculateTotal()

        print("Quantity updated successfully.")

    def calculateTotal(self):
        self.totalAmount = 0.0

        for item in self.items:
            self.totalAmount += item.getSubtotal()

    def getTotal(self):
        return self.totalAmount

    def clearCart(self):
        self.items.clear()
        self.totalAmount = 0.0
        print("Cart cleared successfully.")