class Shipment:
    def __init__(
        self,
        shipmentId: int,
        shippingAddress: str,
        shippingDate: str,
        status: str = "Pending"
    ):
        self.shipmentId = shipmentId
        self.shippingAddress = shippingAddress
        self.shippingDate = shippingDate
        self.status = status

    def shipOrder(self) -> None:
        self.status = "Shipped"
        print("Order shipped successfully.")

    def updateStatus(self, newStatus: str) -> None:
        validStatuses = ["Pending", "Shipped", "In Transit", "Delivered"]

        if newStatus not in validStatuses:
            print("Invalid shipment status.")
            return

        self.status = newStatus
        print(f"Shipment status updated to: {self.status}")

    def trackShipment(self) -> str:
        return self.status
