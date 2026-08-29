class OrderService:
    @staticmethod
    def place_order(customer):
        return customer.place_order()

    @staticmethod
    def cancel_order(order):
        return order.cancel()

    @staticmethod
    def update_status(order, status):
        order.update_status(status)
