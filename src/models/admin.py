from .user import User


class Admin(User):
    def __init__(self, user_id: int, name: str, email: str, password: str, phone: str,
                 admin_id: int, role: str):
        super().__init__(user_id, name, email, password, phone)
        self.admin_id = admin_id
        self.role = role

    def add_product(self, product):
        return product

    def update_product(self, product, **changes):
        for key, value in changes.items():
            if hasattr(product, key):
                setattr(product, key, value)
        return product

    def delete_product(self, products, product):
        if product in products:
            products.remove(product)

    def manage_orders(self, order, status):
        return order.update_status(status)
