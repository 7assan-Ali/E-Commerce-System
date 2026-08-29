class Shipment:
    def __init__(self, shipment_id: int, status="Pending", tracking_number=None):
        self.shipment_id = shipment_id
        self.status = status
        self.tracking_number = tracking_number

    def update_status(self, status: str):
        self.status = status
