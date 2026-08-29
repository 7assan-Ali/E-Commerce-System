class Payment:
    def __init__(self, payment_id: int, amount: float, method: str, status="Pending"):
        self.payment_id = payment_id
        self.amount = amount
        self.method = method
        self.status = status

    def process(self) -> bool:
        self.status = "Paid"
        return True
