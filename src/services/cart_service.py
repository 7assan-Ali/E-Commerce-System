class CartService:
    @staticmethod
    def add_to_cart(cart, product, quantity=1):
        cart.add_item(product, quantity)

    @staticmethod
    def remove_from_cart(cart, product):
        cart.remove_item(product)

    @staticmethod
    def get_total(cart):
        return cart.get_total()
