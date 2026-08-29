from user import User


class Customer(User):
    def __init__(
        self,
        userID: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        customerId: int,
        loyaltyPoints: int = 0
    ):
        super().__init__(
            userID,
            name,
            email,
            password,
            phone
        )

        self.customerId = customerId
        self.loyaltyPoints = loyaltyPoints

        self.cart = None
        self.orders = []
        self.reviews = []

    def displayCustomerInfo(self) -> None:
        print("\nCustomer Information")
        print("--------------------")
        print(f"Customer ID: {self.customerId}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Loyalty Points: {self.loyaltyPoints}")

    def browseProducts(self) -> None:
        print("Customer is browsing products.")

    def addToCart(self, product) -> None:
        print(f"{product.name} added to cart.")

    def placeOrder(self) -> None:
        print("Order placed successfully.")

    def cancelOrder(self, orderId: int) -> None:
        print(f"Order {orderId} cancelled successfully.")

    def reviewProduct(
        self,
        product,
        rating: int,
        comment: str
    ) -> None:

        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return

        print(f"Review added for {product.name}.")