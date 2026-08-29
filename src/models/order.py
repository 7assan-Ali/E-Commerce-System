class Order:
    def __init__(
        self,
        orderId: int,
        orderDate: str,
        status: str = "Pending"
    ):
        self.orderId = orderId
        self.orderDate = orderDate
        self.status = status
        self.items = []
        self.total = 0.0

    def cancelOrder(self) -> None:
        if self.status == "Cancelled":
            print("Order is already cancelled.")
            return

        if self.status == "Shipped" or self.status == "Delivered":
            print("Cannot cancel a shipped or delivered order.")
            return

        self.status = "Cancelled"
        print("Order cancelled successfully.")

    def updateStatus(self, newStatus: str) -> None:
        validStatuses = [
            "Pending",
            "Processing",
            "Shipped",
            "Delivered",
            "Cancelled"
        ]

        if newStatus not in validStatuses:
            print("Invalid order status.")
            return

        self.status = newStatus
        print(f"Order status updated to: {self.status}")

    def getTotal(self) -> float:
        return self.total
    
    
Order(1, "2026-08-30")