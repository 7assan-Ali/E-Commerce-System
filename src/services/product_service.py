class ProductService:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def delete_product(self, product):
        if product in self.products:
            self.products.remove(product)

    def get_products(self):
        return self.products
