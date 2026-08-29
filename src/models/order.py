from .order_item import OrderItem


class Order:
    def __init__(self, order_id: int, cart=None, order_date=None, status="Pending"):
        self.order_id = order_id
        self.order_date = order_date
        self.status = status
        self.items = []
        self.address = None
        self.payment = None
        self.shipment = None

        if cart is not None:
            self.items = [OrderItem(item.product, item.quantity) for item in cart.items]

    @property
    def total(self) -> float:
        return sum(item.calculate_subtotal() for item in self.items)

    def cancel(self) -> bool:
        if self.status in {"Pending", "Processing"}:
            self.status = "Cancelled"
            return True
        return False

    def update_status(self, status: str):
        self.status = status
