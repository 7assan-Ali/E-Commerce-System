from user import User
from product import Product

class Admin(User):
    def __init__(
        self,
        userID: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        adminId: int,
        role: str
    ):
        super().__init__(
            userID,
            name,
            email,
            password,
            phone
        )

        self.adminId = adminId
        self.role = role

    def displayAdminInfo(self) -> None:
        print("\nAdmin Information")
        print("-----------------")
        print(f"Admin ID: {self.adminId}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Role: {self.role}")

    def addProduct(self, product: Product) -> None:
        print(f"Product '{product.name}' added successfully.")

    def updateProduct(self, product: Product) -> None:
        print(f"Product '{product.name}' updated successfully.")

    def deleteProduct(self, product: Product) -> None:
        print(f"Product '{product.name}' removed successfully.")

    def manageOrders(self) -> None:
        print("Admin is managing orders.")